# `split-folders` [![Build Status](https://img.shields.io/github/actions/workflow/status/jfilter/split-folders/test.yml)](https://github.com/jfilter/split-folders/actions/workflows/test.yml) [![PyPI](https://img.shields.io/pypi/v/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/split-folders)](https://pypistats.org/packages/split-folders)

Split folders with files (e.g. images) into **train**, **validation** and **test** (dataset) folders.

The input folder should have the following format (with class subdirectories):

```
input/
    class1/
        img1.jpg
        img2.jpg
        ...
    class2/
        imgWhatever.jpg
        ...
    ...
```

Or a **flat directory** without class subdirectories:

```
input/
    file1.jpg
    file2.jpg
    ...
```

In order to give you this:

```
output/
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
```

This should get you started to do some serious deep learning on your data. [Read here](https://stats.stackexchange.com/questions/19048/what-is-the-difference-between-test-set-and-validation-set) why it's a good idea to split your data intro three different sets.

-   Split files into a training set and a validation set (and optionally a test set).
-   Works on any file types.
-   Supports both class-based directory structures and flat directories.
-   The files get shuffled (can be disabled for time series data).
-   A [seed](https://docs.python.org/3/library/random.html#random.seed) makes splits reproducible.
-   Allows randomized [oversampling](https://en.wikipedia.org/wiki/Oversampling_and_undersampling_in_data_analysis) for imbalanced datasets.
-   Optionally group files by prefix or by stem.
-   Optionally split files by file format(s).
-   Split parallel directories (e.g. `images/` + `annotations/`) in lockstep.
-   Custom grouping via callable.
-   (Should) work on all operating systems.

## Install

This package is Python only and there are no external dependencies.

```bash
pip install split-folders
```

Optionally, you may install [tqdm](https://github.com/tqdm/tqdm) to get a progress bar when moving files.

```bash
pip install split-folders[full]
```

## Usage

You can use `split-folders` as Python module or as a Command Line Interface (CLI).

If your datasets is balanced (each class has the same number of samples), choose `ratio` otherwise `fixed`.
NB: oversampling is turned off by default.
Oversampling is only applied to the _train_ folder since having duplicates in _val_ or _test_ would be considered cheating.

### Module

```python
import splitfolders

# Split with a ratio.
# To only split into training and validation set, set a tuple to `ratio`, i.e, `(.8, .2)`.
splitfolders.ratio("input_folder", output="output",
    seed=1337, ratio=(.8, .1, .1), group_prefix=None, group=None,
    formats=None, move=False, shuffle=True) # default values

# Split val/test with a fixed number of items, e.g. `(100, 100)`, for each set.
# To only split into training and validation set, use a single number to `fixed`, i.e., `10`.
# Set 3 values, e.g. `(300, 100, 100)`, to limit the number of training values.
splitfolders.fixed("input_folder", output="output",
    seed=1337, fixed=(100, 100), oversample=False, group_prefix=None, group=None,
    formats=None, move=False, shuffle=True) # default values

# Use `fixed="auto"` with oversampling to auto-compute the val size from the smallest class.
# Allocates ~20% of the smallest class to validation, rest to training.
splitfolders.fixed("input_folder", output="output",
    seed=1337, fixed="auto", oversample=True)

# Split into k folds for cross-validation.
# Each fold directory contains train/ and val/ subdirectories.
# Uses symlinks by default to avoid k× disk usage.
splitfolders.kfold("input_folder", output="output",
    seed=1337, k=5, group_prefix=None, group=None,
    formats=None, move="symlink", shuffle=True) # default values

# Split without shuffling (e.g. for time series data).
splitfolders.ratio("input_folder", output="output",
    ratio=(.8, .1, .1), shuffle=False)
```

### Flat directories

If your input folder contains files directly (no class subdirectories), `splitfolders` auto-detects this and splits files into `train/`, `val/`, `test/` without creating class subfolders:

```python
# input_folder/ contains file1.jpg, file2.jpg, ... (no subdirs)
splitfolders.ratio("input_folder", output="output", ratio=(.8, .1, .1))
```

Output:
```
output/
    train/
        file1.jpg
        ...
    val/
        file5.jpg
        ...
```

> **Note:** Oversampling is not available with flat directories (there are no classes to balance).

### Grouping files

When your data has multiple files per sample (e.g. an image and its annotation), you need to keep them together during the split. There are several ways to do this.

#### Group by prefix (`group_prefix`)

The legacy approach. Set `group_prefix` to the number of files per group (e.g. `2` for image + annotation pairs). Files are grouped by their filename stem (the part before the extension). All stems must have exactly `group_prefix` files.

```
input/cats/
    img1.jpg   img1.txt
    img2.jpg   img2.txt
```

```python
splitfolders.ratio("input", output="output", group_prefix=2)
```

#### Group by stem (`group="stem"`)

A simpler alternative to `group_prefix`. Automatically groups files that share the same stem and discovers the group size. No need to specify how many files per group — it just requires every stem to have the same count.

```python
splitfolders.ratio("input", output="output", group="stem")
```

If every stem has only one file (e.g. a folder of just `.jpg` files), `group="stem"` behaves identically to no grouping.

#### Group by sibling directories (`group="sibling"`)

For datasets where file types live in **parallel directories** rather than alongside each other:

```
data/
    images/
        im_1.jpg
        im_2.jpg
    annotations/
        im_1.xml
        im_2.xml
```

Use `group="sibling"` to split all directories in lockstep, matching files across directories by stem:

```python
splitfolders.ratio("data", output="output", group="sibling")
```

This produces:

```
output/
    train/
        images/im_1.jpg
        annotations/im_1.xml
    val/
        images/im_2.jpg
        annotations/im_2.xml
```

Requirements:
- The input must have at least 2 subdirectories.
- Every stem must exist in every subdirectory.
- Cannot be combined with `oversample=True`.

#### Custom grouping (`group=callable`)

For advanced use cases, pass any callable that takes a list of `Path` objects and returns a list of tuples:

```python
def my_grouping(files):
    # Custom logic to group files
    # Return: list of tuples of Path objects
    ...

splitfolders.ratio("input", output="output", group=my_grouping)
```

This also covers **manifest-based splitting** (#41). For example, if you have a CSV that defines train/test assignments:

```python
def group_from_manifest(files):
    manifest = load_my_csv("split_manifest.csv")
    # return list of tuples grouped according to manifest
    ...

splitfolders.ratio("input", output="output", group=group_from_manifest)
```

> **Note:** `group_prefix` and `group` are mutually exclusive — setting both raises a `ValueError`.

### File formats

There might be some instances when you have multiple file formats in these folders. Provide one or multiple extension(s) to `formats` for splitting only certain files (e.g. `formats=['.jpeg', '.png']`).

### Move options

Set
- `move=True` or `move='move'` if you want to move the files instead of copying.
- `move=False` or `move='copy'` if you want to copy the files. (default behavior)
- `move='symlink'` if you want to symlink (i.e. create shortcuts `ln -s`) instead of copying.

### CLI

```
Usage:
    splitfolders [--output] [--ratio] [--fixed] [--kfold] [--seed] [--oversample] [--group_prefix] [--group] [--formats] [--move] [--no-shuffle] folder_with_images
Options:
    --output        path to the output folder. defaults to `output`. Get created if non-existent.
    --ratio         the ratio to split. e.g. for train/val/test `.8 .1 .1 --` or for train/val `.8 .2 --`.
    --fixed         set the absolute number of items per validation/test set. The remaining items constitute
                    the training set. e.g. for train/val/test `100 100` or for train/val `100`.
                    Set 3 values, e.g. `300 100 100`, to limit the number of training values.
                    Use `auto` to auto-compute from the smallest class (requires --oversample).
    --kfold         split into k folds for cross-validation. e.g. `5` for 5-fold CV. Uses symlinks by default.
    --seed          set seed value for shuffling the items. defaults to 1337.
    --oversample    enable oversampling of imbalanced datasets, works only with --fixed.
    --group_prefix  split files into equally-sized groups based on their prefix
    --group         grouping strategy: 'stem' or 'sibling' (mutually exclusive with --group_prefix)
    --formats       split the files based on specified extension(s)
    --move          move the files instead of copying
    --symlink       symlink(create shortcut) the files instead of copying
    --no-shuffle    do not shuffle files before splitting (useful for time series data)
Example:
    splitfolders --ratio .8 .1 .1 -- folder_with_images
    splitfolders --kfold 5 folder_with_images
    splitfolders --group stem --ratio .8 .1 .1 -- folder_with_images
    splitfolders --group sibling --ratio .8 .1 .1 -- data_with_parallel_dirs
```

Because of some [Python quirks](https://github.com/jfilter/split-folders/issues/19) you have to prepend ` --` after using `--ratio`.

Instead of the command `splitfolders` you can also use `split_folders` or `split-folders`.

## Development

Install and use [poetry](https://python-poetry.org/).

## Contributing

If you have a **question**, found a **bug** or want to propose a new **feature**, have a look at the [issues page](https://github.com/jfilter/split-folders/issues).

**Pull requests** are especially welcomed when they fix bugs or improve the code quality.

## License

MIT
