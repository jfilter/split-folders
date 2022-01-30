from pathlib import Path


def list_dirs(directory):
    """
    Returns all directories in a given directory
    """
    return [f for f in Path(directory).iterdir() if f.is_dir()]


def list_files(directory):
    """
    Returns all files in a given directory
    """
    return [
        f
        for f in Path(directory).iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]
