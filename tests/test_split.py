import os
import pathlib
import shutil

import pytest

import split_folders


def test_split_ratio():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    split_folders.ratio(input_dir, output_dir)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_ratio_2():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    split_folders.ratio(input_dir, output_dir, ratio=(0.7, 0.2, 0.1))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_ratio_no_test():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    split_folders.ratio(input_dir, output_dir, ratio=(0.8, 0.2))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    split_folders.fixed(input_dir, output_dir, fixed=(2, 2))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed_sample():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    split_folders.fixed(input_dir, output_dir, fixed=(2, 2), oversample=True)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a != b


def test_split_fixed_sample_unbalanced():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError):
        split_folders.fixed(input_dir, output_dir, fixed=(9, 1), oversample=True)

