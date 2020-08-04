import os
import pathlib
import shutil

import pytest

from splitfolders import ratio, fixed


def test_second_package():
    from split_folders import ratio, fixed


def test_split_ratio():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_ratio_2():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, ratio=(0.7, 0.2, 0.1))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_ratio_no_test():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, ratio=(0.8, 0.2))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2, 2))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed_oversample():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2, 2), oversample=True)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a != b


def test_split_fixed_oversample_unbalanced():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError):
        fixed(input_dir, output_dir, fixed=(9, 1), oversample=True)


def test_split_ratio_prefix():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, shared_prefix=2)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed_prefix():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), oversample=False, shared_prefix=2)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed_oversample_prefix():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), oversample=True, shared_prefix=2)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a != b


def test_split_ratio_prefix_error_1():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts_error_1")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError):
        ratio(input_dir, output_dir, shared_prefix=2)


def test_split_ratio_prefix_error_2():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts_error_2")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError):
        ratio(input_dir, output_dir, shared_prefix=2)
