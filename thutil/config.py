import json
from pathlib import Path
from typing import Union

import yaml


### ANCHOR: YAML config
def validate_config(config_file, schema_file, allow_unknown=False, require_all=False):
    """Validate the config file with the schema file.

    Args:
        config_file (str): path to the YAML config file
        schema_file (str): path to the YAML schema file
        allow_unknown (bool, optional): whether to allow unknown fields in the config file. Defaults to False.
        require_all (bool, optional): whether to require all fields in the schema file to be present in the config file. Defaults to False.

    Raises:
        ValueError: if the config file does not match the schema
    """
    from cerberus import Validator

    document = yaml.safe_load(open(config_file))
    schema = yaml.safe_load(open(schema_file))

    v = Validator(allow_unknown=allow_unknown, require_all=require_all)
    res = v.validate(document, schema)
    if not res:
        raise ValueError(f"Error in config file: {config_file} \n{v.errors}")
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


def load_jsonc(filename: str) -> dict:
    """Load data from a JSON file that allow comments."""
    with open(filename) as f:
        lines = f.readlines()
    cleaned_lines = [line.strip().split("//", 1)[0] for line in lines if line.strip()]
    text = "\n".join(cleaned_lines)
    jdata = json.loads(text)
    return jdata


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
