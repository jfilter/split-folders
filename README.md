# Split Folders [![Build Status](https://travis-ci.com/jfilter/split-folders.svg?branch=master)](https://travis-ci.com/jfilter/split-folders) [![PyPI](https://img.shields.io/pypi/v/split-folders.svg)](https://pypi.org/project/split-folders/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/split-folders.svg)](https://pypi.org/project/split-folders/)

Split folders with files (e.g. images) into train, validation and test (dataset) folders.

The input folder shoud have the following format:

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

-   You may only split into a training and validation set.
-   The data gets split before it gets shuffled.
-   A [seed](https://docs.python.org/3/library/random.html#random.seed) lets you reproduce the splits.
-   Works on any file types.
-   (Should) work on all operating systems.

## Install

```bash
pip install split-folders
```

## Usage

You you can use `split_folders` as Python module or as a Command Line Interface (CLI).

### Module

```python
import split_folders

# split with a ratio. To only split into training and validation set, set a tuple, e.g. (.8, .2)
split_folders.ratio('input_folder', output="output", seed=1337, ratio=(.8, .1, .1)) # default values

# split val/test with a fixed number of items e.g. 100 for each set. To only split into training and validation set, a single number.
split_folders.fixed('input_folder', output="output", seed=1337, fixed=(100, 100)) # default values
```

### CLI

```
Usage:
    split_folders folder_with_images [--output] [--ratio] [--fixed] [--seed]
Options:
    --output    path to the output folder. defaults to `output`. Get created if non-existent.
    --ratio     the ratio to split. e.g. for train/val/test `.8 .1 .1` or for train/val `.8 .2`
    --fixed     set the absolute number of items per validation/test set. The remaining items constitute the training set.
                e.g. for train/val/test `100 100` or for train/val `100`
    --seed      set seed value for shuffling the items. defaults to 1337.
Example:
    split_folders imgs --ratio .8 .1 .1
```

## License

MIT.
