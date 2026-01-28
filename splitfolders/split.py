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

from .grouping import resolve_grouping, setup_sibling_files
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


def ratio(
    input, output="output", seed=1337, ratio=(0.8, 0.1, 0.1),
    group_prefix=None, group=None, move=False, formats=None,
):
    if not round(sum(ratio), 5) == 1:  # round for floating imprecision
        raise ValueError("The sums of `ratio` is over 1.")
    if len(ratio) not in (2, 3):
        raise ValueError("`ratio` should")

    check_input_format(input)
    valid_extensions(formats)

    if use_tqdm:
        prog_bar = tqdm(desc="Copying files", unit=" files")

    if group == "sibling":
        split_sibling_dirs_ratio(input, output, ratio, seed, prog_bar if use_tqdm else None, move, formats)
    else:
        for class_dir in list_dirs(input):
            split_class_dir_ratio(
                class_dir, output, ratio, seed, prog_bar if use_tqdm else None, group_prefix, group, move, formats
            )

    if use_tqdm:
        prog_bar.close()


def fixed(
    input, output="output", seed=1337, fixed=(100, 100), oversample=False,
    group_prefix=None, group=None, move=False, formats=None,
):
    check_input_format(input)
    valid_extensions(formats)

    if group == "sibling" and oversample:
        raise ValueError("Cannot use `oversample=True` with `group='sibling'` (no classes to balance).")

    if fixed == "auto":
        if not oversample:
            raise ValueError(
                '`fixed="auto"` requires `oversample=True`. For non-oversampled splits, use `ratio` instead.'
            )
        # Count files per class and derive fixed from the smallest class
        classes_dirs = list_dirs(input)
        counts = []
        for class_dir in classes_dirs:
            files = list_files(class_dir, formats)
            files = resolve_grouping(files, group_prefix, group)
            counts.append(len(files))
        min_count = min(counts)
        fixed = [max(1, min_count // 5)]
    else:
        if isinstance(fixed, int):
            fixed = [fixed]

        if len(fixed) not in (1, 2, 3):
            raise ValueError("`fixed` should be an integer or a list of 2 or 3 integers")

        if len(fixed) == 3 and oversample:
            raise ValueError("Using fixed with 3 values together with oversampling is not implemented.")

    if use_tqdm:
        prog_bar = tqdm(desc="Copying files", unit=" files")

    if group == "sibling":
        split_sibling_dirs_fixed(input, output, fixed, seed, prog_bar if use_tqdm else None, move, formats)
        if use_tqdm:
            prog_bar.close()
        return

    classes_dirs = list_dirs(input)
    num_items = []
    for class_dir in classes_dirs:
        num_items.append(
            split_class_dir_fixed(
                class_dir, output, fixed, seed, prog_bar if use_tqdm else None, group_prefix, group, move, formats
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
        train_files = resolve_grouping(train_files, group_prefix, group)

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


def kfold(input, output="output", seed=1337, k=5, group_prefix=None, group=None, move="symlink", formats=None):
    if k < 2:
        raise ValueError("`k` must be 2 or greater.")

    check_input_format(input)
    valid_extensions(formats)

    if use_tqdm:
        prog_bar = tqdm(desc="Copying files", unit=" files")

    if group == "sibling":
        split_sibling_dirs_kfold(input, output, k, seed, prog_bar if use_tqdm else None, move, formats)
    else:
        for class_dir in list_dirs(input):
            split_class_dir_kfold(
                class_dir, output, k, seed, prog_bar if use_tqdm else None,
                group_prefix, group, move, formats,
            )

    if use_tqdm:
        prog_bar.close()


def split_class_dir_kfold(class_dir, output, k, seed, prog_bar, group_prefix, group, move, formats):
    """
    Splits a class folder into k folds for cross-validation.
    Each fold directory gets train/ and val/ subdirectories.
    """
    files = setup_files(class_dir, seed, group_prefix, group, formats)

    # Partition files into k roughly equal chunks
    fold_size = len(files) // k
    remainder = len(files) % k
    partitions = []
    idx = 0
    for i in range(k):
        size = fold_size + (1 if i < remainder else 0)
        partitions.append(files[idx : idx + size])
        idx += size

    # For each fold, val = partition i, train = all other partitions
    for i in range(k):
        val_files = partitions[i]
        train_files = [f for j, part in enumerate(partitions) if j != i for f in part]
        fold_output = str(Path(output) / f"fold_{i + 1}")
        li = [(train_files, "train"), (val_files, "val")]
        copy_files(li, class_dir, fold_output, prog_bar, move)


def setup_files(class_dir, seed, group_prefix=None, group=None, formats=None):
    """
    Returns shuffled list of filenames
    """
    random.seed(seed)  # make sure its reproducible

    files = list_files(class_dir, formats)
    files = resolve_grouping(files, group_prefix, group)

    files.sort()
    random.shuffle(files)
    return files


def split_class_dir_ratio(class_dir, output, ratio, seed, prog_bar, group_prefix, group, move, formats):
    """
    Splits a class folder
    """
    files = setup_files(class_dir, seed, group_prefix, group, formats)

    # the data was shuffled already
    split_train_idx = int(ratio[0] * len(files))
    split_val_idx = split_train_idx + int(ratio[1] * len(files))

    li = split_files(files, split_train_idx, split_val_idx, len(ratio) == 3)
    copy_files(li, class_dir, output, prog_bar, move)


def split_class_dir_fixed(class_dir, output, fixed, seed, prog_bar, group_prefix, group, move, formats):
    """
    Splits a class folder and returns the total number of files
    """
    files = setup_files(class_dir, seed, group_prefix, group, formats)

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


def copy_sibling_files(files_type, type_dir_names, output, prog_bar, move):
    """
    Copies files in sibling mode: each group is a tuple of files across type dirs.
    Output structure: output/split_name/type_dir_name/filename
    """
    copy_fn = _get_copy_fn(move)

    for files, folder_type in files_type:
        for group in files:
            if prog_bar is not None:
                prog_bar.update()
            for type_dir_name, f in zip(type_dir_names, group):
                full_path = Path(output) / folder_type / type_dir_name
                full_path.mkdir(parents=True, exist_ok=True)
                copy_fn(f, full_path)


def split_sibling_dirs_ratio(input_dir, output, ratio, seed, prog_bar, move, formats):
    type_dir_names, groups = setup_sibling_files(input_dir, seed, formats)

    split_train_idx = int(ratio[0] * len(groups))
    split_val_idx = split_train_idx + int(ratio[1] * len(groups))

    li = split_files(groups, split_train_idx, split_val_idx, len(ratio) == 3)
    copy_sibling_files(li, type_dir_names, output, prog_bar, move)


def split_sibling_dirs_fixed(input_dir, output, fixed, seed, prog_bar, move, formats):
    type_dir_names, groups = setup_sibling_files(input_dir, seed, formats)

    if not len(groups) >= sum(fixed):
        raise ValueError(
            f"Not enough file groups for the requested fixed split."
            f" There are only {len(groups)} groups but fixed={fixed} requires at least {sum(fixed)}."
        )

    if len(fixed) <= 2:
        split_train_idx = len(groups) - sum(fixed)
        split_val_idx = split_train_idx + fixed[0]
    else:
        split_train_idx = fixed[0]
        split_val_idx = fixed[0] + fixed[1]

    li = split_files(
        groups,
        split_train_idx,
        split_val_idx,
        len(fixed) >= 2,
        None if len(fixed) != 3 else fixed[2],
    )
    copy_sibling_files(li, type_dir_names, output, prog_bar, move)


def split_sibling_dirs_kfold(input_dir, output, k, seed, prog_bar, move, formats):
    type_dir_names, groups = setup_sibling_files(input_dir, seed, formats)

    fold_size = len(groups) // k
    remainder = len(groups) % k
    partitions = []
    idx = 0
    for i in range(k):
        size = fold_size + (1 if i < remainder else 0)
        partitions.append(groups[idx : idx + size])
        idx += size

    for i in range(k):
        val_files = partitions[i]
        train_files = [f for j, part in enumerate(partitions) if j != i for f in part]
        fold_output = str(Path(output) / f"fold_{i + 1}")
        li = [(train_files, "train"), (val_files, "val")]
        copy_sibling_files(li, type_dir_names, fold_output, prog_bar, move)
