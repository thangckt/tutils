import json
from glob import glob
from pathlib import Path
from typing import Union


def list_files_in_dirs(folders: list[str], extensions: list[str]) -> list[str]:
    """Ex: folders = ["folder1", "folder2", "folder3"], extensions = [".ext1", ".ext2"]"""
    files = []
    for folder in folders:
        for ext in extensions:
            files.extend(glob(f"{folder}/**/*{ext}", recursive=True))
    return files


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


### ANCHOR: Load data from file
def load_setting_file(filename: Union[str, Path]) -> dict:
    """Load data from a JSON or YAML file.

    Parameters
    ----------
    filename : str or os.PathLike
        The filename to load data from, whose suffix should be .json, .yaml, or .yml

    Returns
    -------
    dict
        The data loaded from the file

    Raises
    ------
    ValueError
        If the file format is not supported
    """
    if Path(filename).suffix in [".json", ".jsonc"]:
        data = load_jsonc(filename)
    elif Path(filename).suffix in [".yaml", ".yml"]:
        from ruamel.yaml import YAML

        yaml = YAML(typ="safe", pure=True)
        with Path(filename).open() as fo:
            data = yaml.load(fo)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    return data


def load_jsonc(filename: Union[str, Path]) -> dict:
    """Load data from a JSON file that allow comments."""
    with Path(filename).open() as fo:
        lines = fo.readlines()
    cleaned_lines = [line.strip().split("//", 1)[0] for line in lines if line.strip()]
    text = "\n".join(cleaned_lines)
    jdata = json.loads(text)
    return jdata
