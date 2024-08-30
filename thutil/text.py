import json
import os
from typing import Union


def load_jsonc(filename: Union[str, os.PathLike]) -> dict:
    """Load data from a JSON file that allow comments."""
    with open(filename) as f:
        lines = f.readlines()

    cleaned_lines = [line.strip().split("//", 1)[0] for line in lines if line.strip()]
    text = "\n".join(cleaned_lines)
    jdata = json.loads(text)
    return jdata
