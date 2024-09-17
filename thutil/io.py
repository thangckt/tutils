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


def list_paths(paths: list[str], patterns: list[str], recursive=True) -> list[str]:
    """List all files/folders in given directories and their subdirectories that match the given patterns.

    Parameters
    ----------
    paths : list[str]
        The list of paths to search files/folders.
    patterns : list[str]
        The list of patterns to apply to the files. Each filter can be a file extension or a pattern.

    Returns:
    -------
    List[str]: A list of matching paths.

    Example:
    --------
    ```python
    folders = ["path1", "path2", "path3"]
    patterns = ["*.ext1", "*.ext2", "something*.ext3", "*folder/"]
    files = list_files_in_dirs(folders, patterns)
    ```

    Note:
    -----
    - glob() does not list hidden files by default. To include hidden files, use glob(".*", recursive=True).
    - When use recursive=True, must include `**` in the pattern to search subdirectories.
        - glob("*", recursive=True) will search all FILES & FOLDERS in the CURRENT directory.
        - glob("*/", recursive=True) will search all FOLDERS in the current CURRENT directory.
        - glob("**", recursive=True) will search all FILES & FOLDERS in the CURRENT & SUB subdirectories.
        - glob("**/", recursive=True) will search all FOLDERS in the current CURRENT & SUB subdirectories.
        - "**/*" is equivalent to "**".
        - "**/*/" is equivalent to "**/".
    - IMPORTANT: "**/**" will replicate the behavior of "**", then give unexpected results.

    """
    if not isinstance(paths, list):
        paths = [paths]

    result_paths = []
    for path in paths:
        for pattern in patterns:
            if recursive:
                result_paths.extend(glob(f"{path}/**/{pattern}", recursive=True))
            else:
                result_paths.extend(glob(f"{path}/**/{pattern}"))

    result_paths = list(set(result_paths))  # Remove duplicates
    paths = [Path(p).as_posix() for p in result_paths]
    return paths


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

    ### Detemine paths: dirs, files, and patterns
    files = [p for p in paths if Path(p).is_file()]
    dir_paths = [p for p in paths if Path(p).is_dir()]
    pattern_paths = [p for p in paths if "*" in p]

    ### Files from dir_paths
    search_files = list_paths(dir_paths, patterns, recursive=True)
    files.extend(search_files)

    ### Files from pattern_paths
    search_files = []
    for pattern_path in pattern_paths:
        search_files.extend(glob(pattern_path))

    files.extend(search_files)
    files = list(set(files))  # Remove duplicates
    files = [Path(p).as_posix() for p in files]
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
        jdata = read_yaml(filename)
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


def write_yaml(jdata: dict, filename: Union[str, Path]):
    """Write data to a YAML file."""
    with open(filename, "w") as f:
        yaml.safe_dump(jdata, f, default_flow_style=False, sort_keys=False)
    return


def read_yaml(filename: Union[str, Path]) -> dict:
    """Read data from a YAML file."""
    with open(filename) as f:
        jdata = yaml.safe_load(f)
    return jdata
