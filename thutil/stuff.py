from typing import Generator


def chunk_list(input_list: list, n: int) -> Generator:
    """Yield successive n-sized chunks from `input_list`."""
    for i in range(0, len(input_list), n):
        yield input_list[i : i + n]
