import argparse

from .split import fixed, kfold, ratio


def run():
    parser = argparse.ArgumentParser(
        description=(
            "Split folders with files (e.g. images) by copying them"
            " into training, validation and test (dataset) folders."
        )
    )
    parser.add_argument(
        "--output",
        default="output",
        help="directory where to write the resulting split folders, defaults to `output`",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default="1337",
        help="a seed value to make your split reproducible",
    )
    parser.add_argument(
        "--ratio",
        nargs="+",
        type=float,
        help="the ratio to split. e.g. for train/val/test `.8 .1 .1` or for train/val `.8 .2`",
    )
    parser.add_argument(
        "--fixed",
        nargs="+",
        type=str,
        help=(
            "set the absolute number of items per validation/test set."
            " The remaining items get to the training."
            " e.g. for train/val/test `100 100` or for train/val `100`."
            " Set 3 values, e.g. `300 100 100`, to limit the number of training values."
            " Use `auto` to auto-compute from the smallest class (requires --oversample)."
        ),
    )
    parser.add_argument(
        "--kfold",
        type=int,
        default=None,
        help="split into k folds for cross-validation. e.g. `5` for 5-fold CV. Each fold has train/ and val/ subdirs.",
    )
    parser.add_argument(
        "--oversample",
        action="store_true",
        help="enable oversampling of imbalanced datasets",
    )
    parser.add_argument(
        "--group_prefix",
        type=int,
        default=None,
        help="split files into equally-sized groups based on their prefix",
    )
    parser.add_argument(
        "--group",
        type=str,
        default=None,
        help="grouping strategy: 'stem' or 'sibling'",
    )
    move_group = parser.add_mutually_exclusive_group()
    move_group.add_argument(
        "--move",
        action="store_true",
        help="move the files instead of copying",
    )
    move_group.add_argument(
        "--symlink",
        action="store_true",
        help="symlink(create shortcut) the files instead of copying",
    )
    parser.add_argument(
        "input",
        help=(
            "directory with the input data. The directory needs to have the labels"
            " as sub-directories. In those sub-directories are then the actual files"
            " that gets split."
        ),
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        type=str,
        default=None,
        help="specify the file format(s) which should be considered for spliting the data e.g. `.png .jpeg .jpg`",
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        default=False,
        help="do not shuffle files before splitting (useful for time series data)",
    )

    args = parser.parse_args()

    if args.group_prefix is not None and args.group is not None:
        parser.error("--group_prefix and --group are mutually exclusive.")

    if args.symlink:
        args.move = "symlink"

    shuffle = not args.no_shuffle

    if args.ratio:
        ratio(
            args.input,
            args.output,
            args.seed,
            args.ratio,
            args.group_prefix,
            args.group,
            args.move,
            args.formats,
            shuffle,
        )
    elif args.fixed:
        if args.fixed == ["auto"]:
            fixed_value = "auto"
        else:
            fixed_value = [int(x) for x in args.fixed]
        fixed(
            args.input,
            args.output,
            args.seed,
            fixed_value,
            args.oversample,
            args.group_prefix,
            args.group,
            args.move,
            args.formats,
            shuffle,
        )
    elif args.kfold:
        kfold(
            args.input,
            args.output,
            args.seed,
            args.kfold,
            args.group_prefix,
            args.group,
            args.move if args.move else "symlink",
            args.formats,
            shuffle,
        )
    else:
        print("Please specify either your `--ratio`, `--fixed`, or `--kfold` for the split. see -h for more help.")
