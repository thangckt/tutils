import json
import warnings
from glob import glob
from pathlib import Path
from typing import Union

import yaml


def unpack_dict(nested_dict: dict) -> dict:
    """Unpack one level of nested dictionary."""
    # flat_dict = {
    #     key2: val2 for key1, val1 in nested_dict.items() for key2, val2 in val1.items()
    # }

    ### Use for loop to handle duplicate keys
    flat_dict = {}
    for key1, val1 in nested_dict.items():
        for key2, val2 in val1.items():
            if key2 not in flat_dict:
                flat_dict[key2] = val2
            else:
                raise ValueError(
                    f"Key `{key2}` is used multiple times in the same level of the nested dictionary. Please fix it before unpacking dict."
                )
    return flat_dict


### ANCHOR: Collect files


def list_files_in_dirs(folders: list[str], patterns: list[str]) -> list[str]:
    """List all files in given directories and their subdirectories that match the provided patterns.

    Parameters
    ----------
    folders : list[str]
        The list of folders to search for files.
    patterns : list[str]
        The list of patterns to apply to the files. Each filter can be a file extension or a pattern.

    Returns:
    -------
    List[str]: A list of matching file paths.

    Example:
    --------
    ```python
    folders = ["folder1", "folder2", "folder3"]
    patterns = [".ext1", ".ext2", "something*.ext3"]
    files = list_files_in_dirs(folders, patterns)
    ```
    """
    files = []
    for folder in folders:
        for pattern in patterns:
            files.extend(glob(f"{folder}/**/*{pattern}", recursive=True))

    files = list(set(files))  # Remove duplicates
    return files


def collect_files(paths: list[str], patterns: list[str]) -> list[str]:
    """Collect files from a list of paths (files/folders). Will search files in folders and their subdirectories.

    Parameters
    ----------
    paths : list[str]
        The list of paths to collect files from.
    patterns : list[str]
        The list of patterns to apply to the files. Each filter can be a file extension or a pattern.

    Returns:
    -------
    List[str]: A list of paths matching files.
    """
    if not isinstance(paths, list):
        paths = [paths]

    ### Detemine dirs vs. files
    files = [p for p in paths if Path(p).is_file()]
    dirs = [p for p in paths if Path(p).is_dir()]

    search_files = list_files_in_dirs(dirs, patterns)
    files.extend(search_files)
    files = list(set(files))

    if not files:
        warnings.warn(f"The file list is empty. Check the paths {paths}.")
    return files


### ANCHOR: Load data from file


def combine_text_files(files: list[str], output_file: str):
    """Combine text files into a single file."""
    text = ""
    for file in files:
        with open(file) as f:
            text += f.read()

    with open(output_file, "w") as f:
        f.write(text)
    return


def load_setting_file(filename: Union[str, Path]) -> dict:
    """Load data from a JSON or YAML file.

    Parameters
    ----------
    filename : str or os.PathLike
        The filename to load data from, whose suffix should be .json, .yaml, or .yml

    Returns
    -------
    dict
        jdata: (dict) The data loaded from the file

    Raises
    ------
    ValueError
        If the file format is not supported
    """
    if Path(filename).suffix in [".json", ".jsonc"]:
        jdata = load_jsonc(filename)
    elif Path(filename).suffix in [".yaml", ".yml"]:
        with open(filename) as f:
            jdata = yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    return jdata


def load_jsonc(filename: Union[str, Path]) -> dict:
    """Load data from a JSON file that allow comments."""
    with open(filename) as f:
        lines = f.readlines()
    cleaned_lines = [line.strip().split("//", 1)[0] for line in lines if line.strip()]
    text = "\n".join(cleaned_lines)
    jdata = json.loads(text)
    return jdata
