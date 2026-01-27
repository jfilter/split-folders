"""Splits a folder with the given format:
    class1/
        img1.jpg
        img2.jpg
        ...
    class2/
        imgWhatever.jpg
        ...
    ...

into this resulting format:
    train/
        class1/
            img1.jpg
            ...
        class2/
            imga.jpg
            ...
    val/
        class1/
            img2.jpg
            ...
        class2/
            imgb.jpg
            ...
    test/
        class1/
            img3.jpg
            ...
        class2/
            imgc.jpg
            ...
"""

import os
import random
import shutil
from pathlib import Path

from .utils import list_dirs, list_files

try:
    from tqdm import tqdm

    use_tqdm = True
except ImportError:
    use_tqdm = False


def check_input_format(input):
    p_input = Path(input)
    if not p_input.exists():
        err_msg = f'The provided input folder "{input}" does not exists.'
        if not p_input.is_absolute():
            err_msg += f' Your relative path cannot be found from the current working directory "{Path.cwd()}".'
        raise ValueError(err_msg)

    if not p_input.is_dir():
        raise ValueError(f'The provided input folder "{input}" is not a directory')

    dirs = list_dirs(input)
    if len(dirs) == 0:
        raise ValueError(
            f'The input data is not in a right format. Within your folder "{input}"'
            " there are no directories. Consult the documentation how to the folder"
            " structure should look like."
        )


def _get_copy_fn(move):
    """Return a function(src, dst_dir) that copies/moves/symlinks a file into dst_dir."""
    if move is True or move == "move":
        base_fn = shutil.move
    elif move is False or move == "copy":
        base_fn = shutil.copy2
    elif move == "symlink":
        base_fn = None  # handled below
    else:
        raise ValueError(f"Invalid value for move: {move!r}. Use True, False, or 'symlink'.")

    def copy_fn(src, dst_dir):
        src = Path(src)
        dst_dir = Path(dst_dir)
        if move == "symlink":
            dst = dst_dir / src.name
            try:
                os.symlink(src.resolve(), dst)
            except FileExistsError:
                pass
        else:
            base_fn(str(src), str(dst_dir))

    return copy_fn


def valid_extensions(formats):
    """
    Check if an extension starts with `.`
    """
    if formats is None:
        return
    invalid_ext = [s for s in formats if not s.startswith(".")]
    if invalid_ext:
        raise ValueError(f"Extensions must start with '.': {invalid_ext}")


def ratio(input, output="output", seed=1337, ratio=(0.8, 0.1, 0.1), group_prefix=None, move=False, formats=None):
    if not round(sum(ratio), 5) == 1:  # round for floating imprecision
        raise ValueError("The sums of `ratio` is over 1.")
    if len(ratio) not in (2, 3):
        raise ValueError("`ratio` should")

    check_input_format(input)
    valid_extensions(formats)

    if use_tqdm:
        prog_bar = tqdm(desc="Copying files", unit=" files")

    for class_dir in list_dirs(input):
        split_class_dir_ratio(
            class_dir, output, ratio, seed, prog_bar if use_tqdm else None, group_prefix, move, formats
        )

    if use_tqdm:
        prog_bar.close()


def fixed(
    input, output="output", seed=1337, fixed=(100, 100), oversample=False, group_prefix=None, move=False, formats=None
):
    if isinstance(fixed, int):
        fixed = [fixed]

    if len(fixed) not in (1, 2, 3):
        raise ValueError("`fixed` should be an integer or a list of 2 or 3 integers")

    if len(fixed) == 3 and oversample:
        raise ValueError("Using fixed with 3 values together with oversampling is not implemented.")

    check_input_format(input)
    valid_extensions(formats)

    if use_tqdm:
        prog_bar = tqdm(desc="Copying files", unit=" files")

    classes_dirs = list_dirs(input)
    num_items = []
    for class_dir in classes_dirs:
        num_items.append(
            split_class_dir_fixed(
                class_dir, output, fixed, seed, prog_bar if use_tqdm else None, group_prefix, move, formats
            )
        )

    if use_tqdm:
        prog_bar.close()

    if not oversample:
        return

    num_max_items = max(num_items)
    iteration = zip(num_items, classes_dirs)

    if use_tqdm:
        iteration = tqdm(iteration, desc="Oversampling", unit=" classes")

    for num_items, class_dir in iteration:
        class_name = Path(class_dir).name
        full_path = Path(output) / "train" / class_name
        train_files = list_files(full_path, formats)

        if group_prefix is not None:
            train_files = group_by_prefix(train_files, group_prefix)

        for i in range(num_max_items - num_items):
            f_chosen = random.choice(train_files)

            if not isinstance(f_chosen, tuple):
                f_chosen = (f_chosen,)

            for f_orig in f_chosen:
                new_name = f_orig.stem + "_" + str(i) + f_orig.suffix
                f_dest = f_orig.with_name(new_name)
                if move == "symlink":
                    try:
                        os.symlink(f_orig.resolve(), f_dest)
                    except FileExistsError:
                        pass
                elif move is True or move == "move":
                    shutil.move(str(f_orig), str(f_dest))
                else:
                    shutil.copy2(str(f_orig), str(f_dest))


def group_by_prefix(files, len_pairs):
    """
    Split files into groups of len `len_pairs` based on their prefix.
    """
    results = []
    results_set = set()  # for fast lookup, only file names
    for f in files:
        if f.name in results_set:
            continue
        f_sub = f.name
        for _ in range(len(f_sub)):
            matches = [x for x in files if x.name not in results_set and x.name.startswith(f_sub) and f.name != x.name]
            if len(matches) == len_pairs - 1:
                results.append((f, *matches))
                results_set.update((f.name, *[x.name for x in matches]))
                break
            elif len(matches) < len_pairs - 1:
                f_sub = f_sub[:-1]
            else:
                raise ValueError(
                    f"The length of pairs has to be equal. Coudn't find {len_pairs - 1}"
                    f" matches for {f}. Found {len(matches)} matches."
                )
        else:
            raise ValueError(f"No adequate matches found for {f}.")

    if len(results_set) != len(files):
        raise ValueError(f"Could not find enough matches ({len(results_set)}) for all files ({len(files)})")
    return results


def setup_files(class_dir, seed, group_prefix=None, formats=None):
    """
    Returns shuffeld list of filenames
    """
    random.seed(seed)  # make sure its reproducible

    files = list_files(class_dir, formats)

    if group_prefix is not None:
        files = group_by_prefix(files, group_prefix)

    files.sort()
    random.shuffle(files)
    return files


def split_class_dir_ratio(class_dir, output, ratio, seed, prog_bar, group_prefix, move, formats):
    """
    Splits a class folder
    """
    files = setup_files(class_dir, seed, group_prefix, formats)

    # the data was shuffled already
    split_train_idx = int(ratio[0] * len(files))
    split_val_idx = split_train_idx + int(ratio[1] * len(files))

    li = split_files(files, split_train_idx, split_val_idx, len(ratio) == 3)
    copy_files(li, class_dir, output, prog_bar, move)


def split_class_dir_fixed(class_dir, output, fixed, seed, prog_bar, group_prefix, move, formats):
    """
    Splits a class folder and returns the total number of files
    """
    files = setup_files(class_dir, seed, group_prefix, formats)

    if not len(files) >= sum(fixed):
        raise ValueError(
            f'The number of samples in class "{class_dir.stem}" are too few.'
            f" There are only {len(files)} samples available but your fixed parameter"
            f" {fixed} requires at least {sum(fixed)} files."
            " You may want to split your classes by ratio."
        )

    # the data was shuffeld already
    if len(fixed) <= 2:
        split_train_idx = len(files) - sum(fixed)
        split_val_idx = split_train_idx + fixed[0]
    else:
        split_train_idx = fixed[0]
        split_val_idx = fixed[0] + fixed[1]

    li = split_files(
        files,
        split_train_idx,
        split_val_idx,
        len(fixed) >= 2,
        None if len(fixed) != 3 else fixed[2],
    )
    copy_files(li, class_dir, output, prog_bar, move)
    return len(files)


def split_files(files, split_train_idx, split_val_idx, use_test, max_test=None):
    """
    Splits the files along the provided indices
    """
    files_train = files[:split_train_idx]
    files_val = files[split_train_idx:split_val_idx] if use_test else files[split_train_idx:]

    li = [(files_train, "train"), (files_val, "val")]

    # optional test folder
    if use_test:
        files_test = files[split_val_idx:]
        if max_test is not None:
            files_test = files_test[:max_test]

        li.append((files_test, "test"))
    return li


def copy_files(files_type, class_dir, output, prog_bar, move):
    """
    Copies the files from the input folder to the output folder
    """
    copy_fn = _get_copy_fn(move)

    class_name = Path(class_dir).name
    for files, folder_type in files_type:
        full_path = Path(output) / folder_type / class_name

        full_path.mkdir(parents=True, exist_ok=True)
        for f in files:
            if prog_bar is not None:
                prog_bar.update()
            if isinstance(f, tuple):
                for x in f:
                    copy_fn(x, full_path)
            else:
                copy_fn(f, full_path)
