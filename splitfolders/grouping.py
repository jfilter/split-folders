from collections import defaultdict


def group_by_prefix(files, len_pairs):
    """Groups files by Path.stem, validates each group has len_pairs members."""
    stem_groups = defaultdict(list)
    for f in files:
        stem_groups[f.stem].append(f)
    for stem, group in stem_groups.items():
        if len(group) != len_pairs:
            raise ValueError(f"Expected {len_pairs} files with stem '{stem}', found {len(group)}")
    return [tuple(sorted(g)) for g in sorted(stem_groups.values(), key=lambda g: g[0])]


def resolve_grouping(files, group_prefix=None, group=None):
    """Central dispatcher. Validates mutual exclusivity, routes to the right strategy."""
    if group_prefix is not None and group is not None:
        raise ValueError("Cannot use both `group_prefix` and `group`.")
    if group_prefix is not None:
        return group_by_prefix(files, group_prefix)
    if group is None:
        return files
    if group == "stem":
        return group_by_stem(files)
    if callable(group):
        return group(files)
    if group == "sibling":
        return files  # sibling handled at orchestration level, not here
    raise ValueError(f"Unknown group value: {group!r}.")


def group_by_stem(files):
    """Groups files by stem. Auto-discovers group size. Validates all groups same size.
    If group size is 1 (no actual grouping), returns flat list of Paths."""
    stem_groups = defaultdict(list)
    for f in files:
        stem_groups[f.stem].append(f)

    sizes = {len(g) for g in stem_groups.values()}
    if len(sizes) != 1:
        size_details = {stem: len(g) for stem, g in stem_groups.items()}
        raise ValueError(f"All stems must have the same number of files. Found sizes: {size_details}")

    group_size = sizes.pop()
    if group_size == 1:
        return sorted(files)

    return [tuple(sorted(g)) for g in sorted(stem_groups.values(), key=lambda g: g[0])]


def setup_sibling_files(input_dir, seed, formats=None, shuffle=True):
    """Lists type dirs, groups files by stem across all dirs.
    Validates every stem exists in every dir. Returns (type_dir_names, groups)."""
    from .utils import list_dirs, list_files

    type_dirs = sorted(list_dirs(input_dir))
    if len(type_dirs) < 2:
        raise ValueError(f"group='sibling' requires at least 2 subdirectories, found {len(type_dirs)}.")

    type_dir_names = [d.name for d in type_dirs]

    # Collect stems per type dir
    stems_per_dir = {}
    files_per_dir = {}
    for td in type_dirs:
        dir_files = list_files(td, formats)
        files_per_dir[td.name] = {f.stem: f for f in dir_files}
        stems_per_dir[td.name] = set(files_per_dir[td.name].keys())

    # Validate: every stem must exist in every dir
    all_stems = set()
    for s in stems_per_dir.values():
        all_stems |= s

    for stem in sorted(all_stems):
        for dir_name, stems in stems_per_dir.items():
            if stem not in stems:
                raise ValueError(
                    f"Stem '{stem}' missing in directory '{dir_name}'. "
                    "All stems must exist in every subdirectory for group='sibling'."
                )

    # Build groups: each group is a tuple mapping type_dir_name -> Path
    import random

    random.seed(seed)
    sorted_stems = sorted(all_stems)
    if shuffle:
        random.shuffle(sorted_stems)

    groups = []
    for stem in sorted_stems:
        group = tuple(files_per_dir[dn][stem] for dn in type_dir_names)
        groups.append(group)

    return type_dir_names, groups
