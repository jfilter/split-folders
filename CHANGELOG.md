# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] - 2026-01-28

### Added

- Flat directory support — input folders without class subdirectories are auto-detected and split directly ([#47]).
- `group` parameter with `"stem"`, `"sibling"`, and callable support for flexible file grouping ([#39], [#41], [#51]).
- `group="sibling"` mode for splitting parallel directories (e.g. `images/` + `annotations/`) in lockstep ([#51]).
- `shuffle` parameter (`True` by default) to disable shuffling for time series data ([#44]).
- `--group`, `--no-shuffle`, and `--kfold` CLI flags.
- k-fold cross-validation split via `kfold()` ([#50]).
- `fixed="auto"` to auto-compute validation size from the smallest class ([#40]).
- File format filtering via `formats` parameter and `--formats` CLI flag ([#38]).
- Symlink support via `move="symlink"` and `--symlink` CLI flag ([#48]).
- Migrated `pyproject.toml` to PEP 621 for Poetry 2.x.
- Replaced `black`/`isort` with `ruff` for linting.

### Fixed

- `group_prefix` no longer mismatches filenames with shared prefixes (e.g. `image_130` vs `image_1300`) — now matches by `Path.stem` instead of `startswith` ([#39]).
- Error message in `split_class_dir_fixed` ([#35]).
- Typo: "get get" → "get" ([#33]).
- Removed stray debugging `print` statement.

## [0.5.1] - 2022-02-03

### Fixed

- `shutil.move` compatibility for Python <= 3.8 ([#32]).

### Added

- Tests for `pathlib.Path` inputs.

## [0.5.0] - 2022-01-30

### Added

- Warn users if the input folder is not in the expected format ([#13]).
- `fixed` now accepts 3 values to limit the number of training samples ([#24]).
- `move` flag to move files instead of copying ([#28]).

### Fixed

- Missing items for oversampling with groups.

### Changed

- Switched CI from Travis to GitHub Actions.
- Dropped Python 3.6, added Python 3.10 support.
- `tqdm` moved to optional extras (`pip install split-folders[full]`).

## [0.4.3] - 2020-11-01

### Fixed

- Integer `fixed` parameter handling.
- Documentation about `--ratio` CLI usage.

## [0.4.2] - 2020-08-05

### Fixed

- Oversampling documentation and typos.

## [0.4.1] - 2020-08-05

### Changed

- Renamed `shared_prefix` to `group_prefix`.

## [0.4.0] - 2020-08-04

### Added

- `group_prefix` option to group files by shared filename prefix.
- `__version__` attribute.

### Changed

- Switched build system to Poetry.
- CLI command is now `splitfolders` (with `split_folders` and `split-folders` as aliases).
- Input folder is now a positional CLI argument.

## [0.3.1] - 2019-07-30

### Changed

- Require Python 3.6+.

## [0.3.0] - 2019-07-30

### Added

- Optional progress bar via `tqdm` ([#10]).

### Fixed

- Graceful handling when `tqdm` is not installed.

## [0.2.3] - 2019-07-05

### Fixed

- Assertion error due to floating-point imprecision in ratio calculations.

## [0.2.2] - 2019-05-12

### Fixed

- Improved error message when there are not enough files for `fixed`.

## [0.2.1] - 2018-11-09

### Fixed

- One file going missing in certain split configurations ([#1]).

## [0.2.0] - 2018-10-18

### Added

- Randomized oversampling for imbalanced datasets.
- Ignore dotfiles during splitting.

## [0.1.0] - 2018-10-04

### Added

- Initial release.
- Split folders into train, validation, and test sets.
- `ratio` and `fixed` split modes.
- Seed for reproducible splits.
- CLI interface.

[Unreleased]: https://github.com/jfilter/split-folders/compare/0.6.0...HEAD
[0.6.0]: https://github.com/jfilter/split-folders/compare/0.5.1...0.6.0
[0.5.1]: https://github.com/jfilter/split-folders/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/jfilter/split-folders/compare/0.4.3...0.5.0
[0.4.3]: https://github.com/jfilter/split-folders/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/jfilter/split-folders/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/jfilter/split-folders/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/jfilter/split-folders/compare/0.3.1...0.4.0
[0.3.1]: https://github.com/jfilter/split-folders/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/jfilter/split-folders/compare/0.2.3...0.3.0
[0.2.3]: https://github.com/jfilter/split-folders/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/jfilter/split-folders/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/jfilter/split-folders/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/jfilter/split-folders/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/jfilter/split-folders/releases/tag/0.1.0

[#1]: https://github.com/jfilter/split-folders/pull/1
[#10]: https://github.com/jfilter/split-folders/pull/10
[#13]: https://github.com/jfilter/split-folders/issues/13
[#24]: https://github.com/jfilter/split-folders/issues/24
[#28]: https://github.com/jfilter/split-folders/issues/28
[#32]: https://github.com/jfilter/split-folders/issues/32
[#33]: https://github.com/jfilter/split-folders/pull/33
[#35]: https://github.com/jfilter/split-folders/pull/35
[#38]: https://github.com/jfilter/split-folders/pull/38
[#39]: https://github.com/jfilter/split-folders/issues/39
[#40]: https://github.com/jfilter/split-folders/issues/40
[#41]: https://github.com/jfilter/split-folders/issues/41
[#44]: https://github.com/jfilter/split-folders/issues/44
[#47]: https://github.com/jfilter/split-folders/issues/47
[#48]: https://github.com/jfilter/split-folders/pull/48
[#50]: https://github.com/jfilter/split-folders/issues/50
[#51]: https://github.com/jfilter/split-folders/issues/51
