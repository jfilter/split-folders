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

import pathlib
import random
import shutil
from os import path

try:
    from tqdm import tqdm

    tqdm_is_installed = True
except ImportError:
    tqdm_is_installed = False


def list_dirs(directory):
    """Returns all directories in a given directory
    """
    return [f for f in pathlib.Path(directory).iterdir() if f.is_dir()]


def list_files(directory):
    """Returns all files in a given directory
    """
    return [
        f
        for f in pathlib.Path(directory).iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]


def ratio(
    input, output="output", seed=1337, ratio=(0.8, 0.1, 0.1), shared_prefix=None
):
    # make up for some impression
    assert round(sum(ratio), 5) == 1
    assert len(ratio) in (2, 3)

    if tqdm_is_installed:
        prog_bar = tqdm(desc=f"Copying files", unit=" files")

    for class_dir in list_dirs(input):
        split_class_dir_ratio(
            class_dir,
            output,
            ratio,
            seed,
            prog_bar if tqdm_is_installed else None,
            shared_prefix,
        )

    if tqdm_is_installed:
        prog_bar.close()


def fixed(
    input,
    output="output",
    seed=1337,
    fixed=(100, 100),
    oversample=False,
    shared_prefix=None,
):
    # make sure its reproducible
    if isinstance(fixed, int):
        fixed = fixed

    assert len(fixed) in (1, 2)

    if tqdm_is_installed:
        prog_bar = tqdm(desc=f"Copying files", unit=" files")

    dirs = list_dirs(input)
    lens = []
    for class_dir in dirs:
        lens.append(
            split_class_dir_fixed(
                class_dir,
                output,
                fixed,
                seed,
                prog_bar if tqdm_is_installed else None,
                shared_prefix,
            )
        )

    if tqdm_is_installed:
        prog_bar.close()

    if not oversample:
        return

    max_len = max(lens)

    iteration = zip(lens, dirs)

    if tqdm_is_installed:
        iteration = tqdm(iteration, desc="Oversampling", unit=" classes")

    for length, class_dir in iteration:
        class_name = path.split(class_dir)[1]
        full_path = path.join(output, "train", class_name)
        train_files = list_files(full_path)

        for i in range(max_len - length):
            f_orig = random.choice(train_files)
            new_name = f_orig.stem + "_" + str(i) + f_orig.suffix
            f_dest = f_orig.with_name(new_name)
            shutil.copy2(f_orig, f_dest)


def group_by_prefix(files, len_pairs):
    """Split files into groups of len `len_pairs` based on their prefix.
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


def setup_files(class_dir, seed, shared_prefix=None):
    """Returns shuffled files
    """
    # make sure its reproducible
    random.seed(seed)

    files = list_files(class_dir)

    if shared_prefix is not None:
        files = group_by_prefix(files, shared_prefix)

    files.sort()
    random.shuffle(files)
    return files


def split_class_dir_ratio(class_dir, output, ratio, seed, prog_bar, shared_prefix):
    """Splits one very class folder
    """
    files = setup_files(class_dir, seed, shared_prefix)

    # the data was shuffeld already
    split_train_idx = int(ratio[0] * len(files))
    split_val_idx = split_train_idx + int(ratio[1] * len(files))

    li = split_files(files, split_train_idx, split_val_idx, len(ratio) == 3)
    copy_files(li, class_dir, output, prog_bar)


def split_class_dir_fixed(class_dir, output, fixed, seed, prog_bar, shared_prefix):
    """Splits one very class folder
    """
    files = setup_files(class_dir, seed, shared_prefix)

    if not len(files) > sum(fixed):
        raise ValueError(
            f'The number of samples in class "{class_dir.stem}" are too few. There are only {len(files)} samples available but your fixed parameter {fixed} requires at least {sum(fixed)} files. You may want to split your classes by ratio.'
        )

    # the data was shuffeld already
    split_train_idx = len(files) - sum(fixed)
    split_val_idx = split_train_idx + fixed[0]

    li = split_files(files, split_train_idx, split_val_idx, len(fixed) == 2)
    copy_files(li, class_dir, output, prog_bar)
    return len(files)


def split_files(files, split_train_idx, split_val_idx, use_test):
    """Splits the files along the provided indices
    """
    files_train = files[:split_train_idx]
    files_val = (
        files[split_train_idx:split_val_idx] if use_test else files[split_train_idx:]
    )

    li = [(files_train, "train"), (files_val, "val")]

    # optional test folder
    if use_test:
        files_test = files[split_val_idx:]
        li.append((files_test, "test"))
    return li


def copy_files(files_type, class_dir, output, prog_bar):
    """Copies the files from the input folder to the output folder
    """
    # get the last part within the file
    class_name = path.split(class_dir)[1]
    for (files, folder_type) in files_type:
        full_path = path.join(output, folder_type, class_name)

        pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)
        for f in files:
            if not prog_bar is None:
                prog_bar.update()
            if type(f) == tuple:
                for x in f:
                    shutil.copy2(x, full_path)
            else:
                shutil.copy2(f, full_path)
