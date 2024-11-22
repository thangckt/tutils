import json
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


### ANCHOR: Load data from file
def combine_text_files(files: list[str], output_file: str):
    """Combine text files into a single file."""
    ### Create parent folder if not exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    ### combine text files
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


def download_rawtext(url: str, outfile: str = None) -> str:
    """Download raw text from a URL."""
    import requests

    res = requests.get(url)
    text = res.text
    if outfile is not None:
        with open(outfile, "w") as f:
            f.write(text)
    return text
