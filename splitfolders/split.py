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

from pathlib import Path
import random
import shutil
from os import path

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
            f'The input data is not in a right format. Within your folder "{input}" there are no directories. Consult the documentation how to the folder structure should look like.'
        )


def ratio(
    input,
    output="output",
    seed=1337,
    ratio=(0.8, 0.1, 0.1),
    group_prefix=None,
    move=False,
):
    if not round(sum(ratio), 5) == 1:  # round for floating imprecision
        raise ValueError("The sums of `ratio` is over 1.")
    if not len(ratio) in (2, 3):
        raise ValueError("`ratio` should")

    check_input_format(input)

    if use_tqdm:
        prog_bar = tqdm(desc=f"Copying files", unit=" files")

    for class_dir in list_dirs(input):
        split_class_dir_ratio(
            class_dir,
            output,
            ratio,
            seed,
            prog_bar if use_tqdm else None,
            group_prefix,
            move,
        )

    if use_tqdm:
        prog_bar.close()


def fixed(
    input,
    output="output",
    seed=1337,
    fixed=(100, 100),
    oversample=False,
    group_prefix=None,
    move=False,
):
    if isinstance(fixed, int):
        fixed = [fixed]

    if not len(fixed) in (1, 2, 3):
        raise ValueError("`fixed` should be an integer or a list of 2 or 3 integers")

    if len(fixed) == 3 and oversample:
        raise ValueError(
            "Using fixed with 3 values together with oversampling is not implemented."
        )

    check_input_format(input)

    if use_tqdm:
        prog_bar = tqdm(desc=f"Copying files", unit=" files")

    classes_dirs = list_dirs(input)
    num_items = []
    for class_dir in classes_dirs:
        num_items.append(
            split_class_dir_fixed(
                class_dir,
                output,
                fixed,
                seed,
                prog_bar if use_tqdm else None,
                group_prefix,
                move,
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

    copy_fun = shutil.move if move else shutil.copy2

    for num_items, class_dir in iteration:
        class_name = path.split(class_dir)[1]
        full_path = path.join(output, "train", class_name)
        train_files = list_files(full_path)

        if group_prefix is not None:
            train_files = group_by_prefix(train_files, group_prefix)

        for i in range(num_max_items - num_items):
            f_chosen = random.choice(train_files)

            if not type(f_chosen) is tuple:
                f_chosen = (f_chosen,)

            for f_orig in f_chosen:
                new_name = f_orig.stem + "_" + str(i) + f_orig.suffix
                f_dest = f_orig.with_name(new_name)
                copy_fun(str(f_orig), str(f_dest))


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
            matches = [
                x
                for x in files
                if x.name not in results_set
                and x.name.startswith(f_sub)
                and f.name != x.name
            ]
            if len(matches) == len_pairs - 1:
                results.append((f, *matches))
                results_set.update((f.name, *[x.name for x in matches]))
                break
            elif len(matches) < len_pairs - 1:
                f_sub = f_sub[:-1]
            else:
                raise ValueError(
                    f"The length of pairs has to be equal. Coudn't find {len_pairs - 1} matches for {f}. Found {len(matches)} matches."
                )
        else:
            raise ValueError(f"No adequate matches found for {f}.")

    if len(results_set) != len(files):
        raise ValueError(
            f"Could not find enough matches ({len(results_set)}) for all files ({len(files)})"
        )
    return results


def setup_files(class_dir, seed, group_prefix=None):
    """
    Returns shuffeld list of filenames
    """
    random.seed(seed)  # make sure its reproducible

    files = list_files(class_dir)

    if group_prefix is not None:
        files = group_by_prefix(files, group_prefix)

    files.sort()
    random.shuffle(files)
    return files


def split_class_dir_ratio(class_dir, output, ratio, seed, prog_bar, group_prefix, move):
    """
    Splits a class folder
    """
    files = setup_files(class_dir, seed, group_prefix)

    # the data was shuffled already
    split_train_idx = int(ratio[0] * len(files))
    split_val_idx = split_train_idx + int(ratio[1] * len(files))

    li = split_files(files, split_train_idx, split_val_idx, len(ratio) == 3)
    copy_files(li, class_dir, output, prog_bar, move)


def split_class_dir_fixed(class_dir, output, fixed, seed, prog_bar, group_prefix, move):
    """
    Splits a class folder and returns the total number of files
    """
    files = setup_files(class_dir, seed, group_prefix)

    if not len(files) > sum(fixed):
        raise ValueError(
            f'The number of samples in class "{class_dir.stem}" are too few. There are only {len(files)} samples available but your fixed parameter {fixed} requires at least {sum(fixed)} files. You may want to split your classes by ratio.'
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
    files_val = (
        files[split_train_idx:split_val_idx] if use_test else files[split_train_idx:]
    )

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

    copy_fun = shutil.move if move else shutil.copy2

    # get the last part within the file
    class_name = path.split(class_dir)[1]
    for (files, folder_type) in files_type:
        full_path = path.join(output, folder_type, class_name)

        Path(full_path).mkdir(parents=True, exist_ok=True)
        for f in files:
            if not prog_bar is None:
                prog_bar.update()
            if type(f) == tuple:
                for x in f:
                    copy_fun(str(x), str(full_path))
            else:
                copy_fun(str(f), str(full_path))
