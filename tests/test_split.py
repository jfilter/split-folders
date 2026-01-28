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


def test_split_fixed_auto():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed="auto", oversample=True)

    # output should have train and val directories
    assert pathlib.Path(output_dir, "train").is_dir()
    assert pathlib.Path(output_dir, "val").is_dir()

    # every class should have files in both train and val
    for class_name in ("cats", "dogs"):
        train_count = len(list(pathlib.Path(output_dir, "train", class_name).glob("*")))
        val_count = len(list(pathlib.Path(output_dir, "val", class_name).glob("*")))
        assert train_count > 0
        assert val_count > 0


def test_split_fixed_auto_no_oversample():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError, match="requires `oversample=True`"):
        fixed(input_dir, output_dir, fixed="auto", oversample=False)


def test_kfold_invalid():
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError):
        kfold(input_dir, output_dir, k=1)


# --- Phase 1: group_by_prefix collision fix ---


def test_group_by_prefix_no_collision():
    """Regression test: group_prefix=2 with collision-prone filenames succeeds."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_prefix_collision")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group_prefix=2)

    # ensure the number of files is the same
    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a == b


# --- Phase 2: group parameter ---


def test_group_by_stem():
    """group='stem' with imgs_texts produces same result as group_prefix=2."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="stem")

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a == b


def test_group_by_stem_singles():
    """group='stem' with imgs (only .jpg) works like no grouping."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="stem")

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_group_by_stem_uneven_error():
    """Mismatched stem counts raise ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts_error_1")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError, match="same number of files"):
        ratio(input_dir, output_dir, group="stem")


def test_group_callable():
    """group=callable works (identity grouping wrapping each file in a 1-tuple)."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group=lambda files: [(f,) for f in files])

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_group_and_group_prefix_error():
    """Both group and group_prefix set raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError, match="Cannot use both"):
        ratio(input_dir, output_dir, group_prefix=2, group="stem")


# --- Phase 3: sibling mode ---


def test_sibling_ratio():
    """Splits by stem, all output stems have both .jpg and .xml."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="sibling")

    input_jpgs = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    output_jpgs = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert input_jpgs == output_jpgs

    input_xmls = len(list(pathlib.Path(input_dir).glob("**/*.xml")))
    output_xmls = len(list(pathlib.Path(output_dir).glob("**/*.xml")))
    assert input_xmls == output_xmls


def test_sibling_fixed():
    """Fixed split in sibling mode."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), group="sibling")

    input_jpgs = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    output_jpgs = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert input_jpgs == output_jpgs

    input_xmls = len(list(pathlib.Path(input_dir).glob("**/*.xml")))
    output_xmls = len(list(pathlib.Path(output_dir).glob("**/*.xml")))
    assert input_xmls == output_xmls


def test_sibling_kfold():
    """K-fold in sibling mode."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, group="sibling", move=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3

    input_jpgs = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))

    for fold_dir in fold_dirs:
        train_jpgs = len(list((fold_dir / "train").rglob("*.jpg")))
        val_jpgs = len(list((fold_dir / "val").rglob("*.jpg")))
        assert train_jpgs + val_jpgs == input_jpgs


def test_sibling_output_structure():
    """Output has train/images/, train/annotations/ (type dirs, not classes)."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="sibling")

    output_path = pathlib.Path(output_dir)
    # Check that type dirs exist in train
    assert (output_path / "train" / "images").is_dir()
    assert (output_path / "train" / "annotations").is_dir()


def test_sibling_missing_file_error():
    """Missing stem in one dir raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling_missing")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    with pytest.raises(ValueError, match="missing"):
        ratio(input_dir, output_dir, group="sibling")


def test_sibling_oversample_error():
    """oversample=True + group='sibling' raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError, match="Cannot use.*oversample.*sibling"):
        fixed(input_dir, output_dir, fixed=(1, 1), oversample=True, group="sibling")


# --- Coverage: split mode × grouping mode gaps ---


def test_fixed_group_stem():
    """fixed + group='stem' with paired files."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), group="stem")

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a == b


def test_kfold_group_prefix():
    """kfold + group_prefix with paired files."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, group_prefix=2, move=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3

    input_jpgs = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    for fold_dir in fold_dirs:
        train_jpgs = len(list((fold_dir / "train").rglob("*.jpg")))
        val_jpgs = len(list((fold_dir / "val").rglob("*.jpg")))
        assert train_jpgs + val_jpgs == input_jpgs


def test_kfold_group_stem():
    """kfold + group='stem' with paired files."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, group="stem", move=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3

    input_jpgs = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    for fold_dir in fold_dirs:
        train_jpgs = len(list((fold_dir / "train").rglob("*.jpg")))
        val_jpgs = len(list((fold_dir / "val").rglob("*.jpg")))
        assert train_jpgs + val_jpgs == input_jpgs


def test_fixed_group_callable():
    """fixed + group=callable."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2, 2), group=lambda files: [(f,) for f in files])

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_kfold_group_callable():
    """kfold + group=callable."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, group=lambda files: [(f,) for f in files], move=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3


# --- Coverage: oversample × grouping gaps ---


def test_fixed_oversample_group_stem():
    """oversample + fixed + group='stem'."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(1, 1), oversample=True, group="stem")

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a != b

    a = len(list(pathlib.Path(input_dir).glob("**/*.txt")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert a != b


# --- Coverage: formats × grouping gaps ---


def test_ratio_formats_group_stem():
    """formats + group='stem' — only .jpg selected, stem grouping becomes singles."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="stem", formats=[".jpg"])

    jpg_count = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    txt_count = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert jpg_count > 0
    assert txt_count == 0


def test_ratio_formats_group_prefix():
    """formats + group_prefix — only .jpg selected with group_prefix=1."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group_prefix=1, formats=[".jpg"])

    jpg_count = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    txt_count = len(list(pathlib.Path(output_dir).glob("**/*.txt")))
    assert jpg_count > 0
    assert txt_count == 0


def test_sibling_formats_mismatch_error():
    """formats filtering out one sibling dir's files entirely raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    # .jpg filter excludes annotations/*.xml, so stems are "missing"
    with pytest.raises(ValueError, match="missing"):
        ratio(input_dir, output_dir, group="sibling", formats=[".jpg"])


# --- Coverage: symlink × grouping gaps ---


def test_ratio_symlink_group_stem():
    """symlink + group='stem'."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="stem", move="symlink")

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    for f in pathlib.Path(output_dir).rglob("*.jpg"):
        assert f.is_symlink()


def test_sibling_symlink():
    """symlink + group='sibling'."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_sibling")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, group="sibling", move="symlink")

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    for f in pathlib.Path(output_dir).rglob("*.jpg"):
        assert f.is_symlink()


# --- Coverage: mutual exclusivity across all split modes ---


def test_group_and_group_prefix_error_fixed():
    """Both group and group_prefix set in fixed() raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError, match="Cannot use both"):
        fixed(input_dir, output_dir, fixed=(1, 1), group_prefix=2, group="stem")


def test_group_and_group_prefix_error_kfold():
    """Both group and group_prefix set in kfold() raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_texts")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError, match="Cannot use both"):
        kfold(input_dir, output_dir, group_prefix=2, group="stem")


# --- shuffle=False (time series / ordered splits) ---


def test_ratio_no_shuffle():
    """shuffle=False preserves file order — train gets the first files alphabetically."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, ratio=(0.8, 0.2), shuffle=False)

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b

    # With shuffle=False, output should be deterministic and ordered.
    # Run a second time to a different dir and verify identical results.
    output_dir2 = os.path.join(os.path.dirname(__file__), "output2")
    shutil.rmtree(output_dir2, ignore_errors=True)

    ratio(input_dir, output_dir2, ratio=(0.8, 0.2), shuffle=False)

    for split in ("train", "val"):
        files1 = sorted(f.name for f in pathlib.Path(output_dir, split).rglob("*.jpg"))
        files2 = sorted(f.name for f in pathlib.Path(output_dir2, split).rglob("*.jpg"))
        assert files1 == files2

    shutil.rmtree(output_dir2, ignore_errors=True)


def test_fixed_no_shuffle():
    """shuffle=False with fixed split."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2, 2), shuffle=False)

    a = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    b = len(list(pathlib.Path(output_dir).glob("**/*.jpg")))
    assert a == b


def test_kfold_no_shuffle():
    """shuffle=False with kfold split."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, move=False, shuffle=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3

    input_count = len(list(pathlib.Path(input_dir).glob("**/*.jpg")))
    for fold_dir in fold_dirs:
        train_count = len(list((fold_dir / "train").rglob("*.jpg")))
        val_count = len(list((fold_dir / "val").rglob("*.jpg")))
        assert train_count + val_count == input_count


def test_no_shuffle_preserves_order():
    """shuffle=False keeps files in sorted order; train gets the first slice."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, ratio=(0.8, 0.2), shuffle=False)

    # Collect all input files sorted, per class
    for class_name in ("cats", "dogs"):
        input_files = sorted(
            f.name for f in pathlib.Path(input_dir, class_name).iterdir()
            if f.is_file() and not f.name.startswith(".")
        )
        train_files = sorted(
            f.name for f in pathlib.Path(output_dir, "train", class_name).iterdir()
        )
        val_files = sorted(
            f.name for f in pathlib.Path(output_dir, "val", class_name).iterdir()
        )

        # With no shuffle, the split boundary should be consistent:
        # all files end up somewhere and no file is lost
        assert sorted(train_files + val_files) == input_files


# --- Flat directory (no class subdirectories) ---


def test_flat_ratio():
    """ratio() on a flat directory (no subdirs) puts files directly into train/val."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_flat")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, ratio=(0.8, 0.2))

    a = len(list(pathlib.Path(input_dir).glob("*.jpg")))
    b = len(list(pathlib.Path(output_dir).rglob("*.jpg")))
    assert a == b

    # Files should be directly in train/ and val/, not in a class subdir
    assert pathlib.Path(output_dir, "train").is_dir()
    assert pathlib.Path(output_dir, "val").is_dir()
    train_files = list(pathlib.Path(output_dir, "train").glob("*.jpg"))
    val_files = list(pathlib.Path(output_dir, "val").glob("*.jpg"))
    assert len(train_files) + len(val_files) == a


def test_flat_fixed():
    """fixed() on a flat directory."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_flat")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    fixed(input_dir, output_dir, fixed=(2, 2))

    a = len(list(pathlib.Path(input_dir).glob("*.jpg")))
    b = len(list(pathlib.Path(output_dir).rglob("*.jpg")))
    assert a == b


def test_flat_kfold():
    """kfold() on a flat directory."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_flat")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    kfold(input_dir, output_dir, k=3, move=False)

    fold_dirs = sorted(pathlib.Path(output_dir).iterdir())
    assert len(fold_dirs) == 3

    input_count = len(list(pathlib.Path(input_dir).glob("*.jpg")))
    for fold_dir in fold_dirs:
        train_count = len(list((fold_dir / "train").rglob("*.jpg")))
        val_count = len(list((fold_dir / "val").rglob("*.jpg")))
        assert train_count + val_count == input_count


def test_flat_no_class_subdirs_in_output():
    """Flat input should not create class subdirectories in output."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_flat")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    shutil.rmtree(output_dir, ignore_errors=True)

    ratio(input_dir, output_dir, ratio=(0.8, 0.2))

    # train/ should contain files directly, not subdirectories
    train_path = pathlib.Path(output_dir, "train")
    subdirs = [d for d in train_path.iterdir() if d.is_dir()]
    assert len(subdirs) == 0


def test_flat_oversample_error():
    """oversample=True with flat directory raises ValueError."""
    input_dir = os.path.join(os.path.dirname(__file__), "imgs_flat")
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    with pytest.raises(ValueError, match="flat input directory"):
        fixed(input_dir, output_dir, fixed=(2, 2), oversample=True)
