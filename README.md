# `split-folders` [![Build Status](https://img.shields.io/github/workflow/status/jfilter/split-folders/Test)](https://github.com/jfilter/split-folders/actions/workflows/test.yml) [![PyPI](https://img.shields.io/pypi/v/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/split-folders)](https://pypistats.org/packages/split-folders)

Split folders with files (e.g. images) into **train**, **validation** and **test** (dataset) folders.

The input folder should have the following format:

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
-   The files get shuffled.
-   A [seed](https://docs.python.org/3/library/random.html#random.seed) makes splits reproducible.
-   Allows randomized [oversampling](https://en.wikipedia.org/wiki/Oversampling_and_undersampling_in_data_analysis) for imbalanced datasets.
-   Optionally group files by prefix.
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
    seed=1337, ratio=(.8, .1, .1), group_prefix=None, move=False) # default values

# Split val/test with a fixed number of items, e.g. `(100, 100)`, for each set.
# To only split into training and validation set, use a single number to `fixed`, i.e., `10`.
# Set 3 values, e.g. `(300, 100, 100)`, to limit the number of training values.
splitfolders.fixed("input_folder", output="output",
    seed=1337, fixed=(100, 100), oversample=False, group_prefix=None, move=False) # default values
```

Occasionally, you may have things that comprise more than a single file (e.g. picture (.png) + annotation (.txt)).
`splitfolders` lets you split files into equally-sized groups based on their prefix.
Set `group_prefix` to the length of the group (e.g. `2`).
But now _all_ files should be part of groups.

Set  
- `move=True` or `move='move'` if you want to move the files instead of copying.
- `move=False` or `move='copy'` if you want to copy the files. (default behavior)
- `move='symlink'` if you want to symlink(i.e create shortcuts `ln -s`) instead of copying
### CLI

```
Usage:
    splitfolders [--output] [--ratio] [--fixed] [--seed] [--oversample] [--group_prefix] [--move] folder_with_images
Options:
    --output        path to the output folder. defaults to `output`. Get created if non-existent.
    --ratio         the ratio to split. e.g. for train/val/test `.8 .1 .1 --` or for train/val `.8 .2 --`.
    --fixed         set the absolute number of items per validation/test set. The remaining items constitute
                    the training set. e.g. for train/val/test `100 100` or for train/val `100`.
                    Set 3 values, e.g. `300 100 100`, to limit the number of training values.
    --seed          set seed value for shuffling the items. defaults to 1337.
    --oversample    enable oversampling of imbalanced datasets, works only with --fixed.
    --group_prefix  split files into equally-sized groups based on their prefix
    --move          move the files instead of copying
    --symlink       symlink(create shortcut) the files instead of copying
Example:
    splitfolders --ratio .8 .1 .1 -- folder_with_images
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
