import os
import pathlib
import shutil

import pytest

from splitfolders import fixed, kfold, ratio


def test_second_package():
    pass


def test_wrong_input():
    input_dir = os.path.join(os.path.dirname(__file__), "imgsxx")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError):
        fixed(input_dir, output_dir)

    with pytest.raises(ValueError):
        fixed("peterpan", output_dir)


def test_split_ratio():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_ratio_path():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(pathlib.Path(input_dir), pathlib.Path(output_dir))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def rm_tree(pth):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def test_split_ratio_path_move():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    input_dir2 = os.path.join(os.path.dirname(__file__), "imgs_move")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    if pathlib.Path(input_dir2).exists():
        rm_tree(pathlib.Path(input_dir2))

    shutil.copytree(input_dir, input_dir2)
    # shutil.copytree(input_dir, input_dir2, dirs_exist_ok=True)
    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(
        pathlib.Path(input_dir2),
        output=pathlib.Path(output_dir),
        seed=1337,
        ratio=(
            0.8,
            0.2,
        ),
        group_prefix=None,
        move=True,
    )

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


def test_split_fixed_simple():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2,))

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_split_fixed_simple_2():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=2)

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


def test_split_fixed_limit_test():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(3, 2, 2), oversample=False)

    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert b == 14


def test_split_ratio_prefix():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group_prefix=2)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b
    # ensure the number of texts is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a == b


def test_split_fixed_prefix():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), oversample=False, group_prefix=2)

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    # ensure the number of texts is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a == b


def test_split_fixed_oversample_prefix():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), oversample=True, group_prefix=2)

    # ensure the number of pics is not the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a != b

    # ensure the number of texts is not the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a != b


def test_split_ratio_symlink():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, move="symlink")

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    # ensure all output files are symlinks
    for f in pathlib.Path(output_dir).rglob("*.jpg"):
        assert f.is_symlink()


def test_split_fixed_symlink():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2, 2), move="symlink")

    # ensure the number of pics is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    # ensure all output files are symlinks
    for f in pathlib.Path(output_dir).rglob("*.jpg"):
        assert f.is_symlink()


def test_split_ratio_formats():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, formats=[".jpg"])

    # only jpg files should be in output
    jpg_count = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    txt_count = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert jpg_count > 0
    assert txt_count == 0


def test_split_fixed_formats():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), formats=[".txt"])

    # only txt files should be in output
    jpg_count = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    txt_count = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert txt_count > 0
    assert jpg_count == 0


def test_split_ratio_formats_multiple():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, formats=[".jpg", ".txt"])

    # both jpg and txt files should be in output
    jpg_count = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    txt_count = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert jpg_count > 0
    assert txt_count > 0


def test_invalid_formats():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError):
        ratio(input_dir, output_dir, formats=["jpg"])


def test_split_ratio_prefix_error_1():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts_error_1")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError):
        ratio(input_dir, output_dir, group_prefix=2)


def test_split_ratio_prefix_error_2():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts_error_2")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError):
        ratio(input_dir, output_dir, group_prefix=2)


def test_kfold_basic():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=5, move=False)

    # verify 5 fold directories created
    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 5

    input_count = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))

    for fold_dir in fold_dirs:
        # each fold should have train/ and val/
        assert (fold_dir / "train").is_dir()
        assert (fold_dir / "val").is_dir()

        # train + val should equal input count
        train_count = len(list((fold_dir / "train").rglob("*.jpg")))
        val_count = len(list((fold_dir / "val").rglob("*.jpg")))
        assert train_count + val_count == input_count

        # no overlap between train and val
        train_files = {f.name for f in (fold_dir / "train").rglob("*.jpg")}
        val_files = {f.name for f in (fold_dir / "val").rglob("*.jpg")}
        assert train_files.isdisjoint(val_files)


def test_kfold_3():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, move=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3


def test_kfold_symlink():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3)

    # default is symlink
    for f in pathlib.Path(output_dir).rglob("*.jpg"):
        assert f.is_symlink()


def test_kfold_copy():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, move=False)

    # move=False means real copies, not symlinks
    for f in pathlib.Path(output_dir).rglob("*.jpg"):
        assert not f.is_symlink()


def test_kfold_formats():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, move=False, formats=[".jpg"])

    jpg_count = len(list(pathlib.Path(output_dir).rglob("*.jpg")))
    txt_count = len(list(pathlib.Path(output_dir).rglob("*.txt")))
    assert jpg_count > 0
    assert txt_count == 0


def test_kfold_invalid():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError):
        kfold(input_dir, output_dir, k=1)
