import argparse

from .split import fixed, ratio


def run():
    parser = argparse.ArgumentParser(
        description="Split folders with files (e.g. images) into training, validation and test(dataset) folders."
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
        type=int,
        help="set the absolute number of items per validation/test set. The remaining items get to the training. e.g. for train/val/test `100 100` or for train/val `100`. Set 3 values, e.g. `300 100 100`, to limit the number of training values.",
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
        "--move",
        action="store_true",
        help="move the files instead of copying",
    )
    parser.add_argument(
        "input",
        help="directory with the input data. The directory needs to have the labels as sub-directories. In those sub-directories are then the actual files that gets split.",
    )

    args = parser.parse_args()

    if args.ratio:
        ratio(
            args.input, args.output, args.seed, args.ratio, args.group_prefix, args.move
        )
    else:
        if args.fixed:
            fixed(
                args.input,
                args.output,
                args.seed,
                args.fixed,
                args.oversample,
                args.group_prefix,
                args.move,
            )
        else:
            print(
                "Please specify either your `--ratio` or your `--fixed` number of items for the split. see -h for more help."
            )
