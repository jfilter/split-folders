from pathlib import Path


def list_dirs(directory):
    """
    Returns all directories in a given directory
    """
    return [f for f in Path(directory).iterdir() if f.is_dir()]


def list_files(directory, formats):
    """
    Returns all files in a given directory based on the given file formats
    """
    if formats:
        return [
            f
            for f in Path(directory).iterdir()
            if f.is_file() and not f.name.startswith(".") and f.name.endswith(tuple(formats))
        ]
    else:
        return [
            f
            for f in Path(directory).iterdir()
            if f.is_file() and not f.name.startswith(".")
        ]
