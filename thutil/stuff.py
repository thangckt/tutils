from typing import Generator


def chunk_list(input_list: list, n: int) -> Generator:
    """Yield successive n-sized chunks from `input_list`."""
    for i in range(0, len(input_list), n):
        yield input_list[i : i + n]


### ANCHOR: string modifier
def fill_text_center(input_text="example", fill="-", max_length=60):
    """Create a line with centered text."""
    text = " " + input_text + " "
    return text.center(max_length, fill)


def fill_text_left(input_text="example", left_margin=20, fill="-", max_length=60):
    """Create a line with left-aligned text."""
    text = (fill * left_margin) + " " + input_text + " "
    return text.ljust(max_length, fill)


def fill_text_box(input_text="", fill=" ", sp="|", max_length=60):
    """Put the string at the center of |  |."""
    strs = input_text.center(max_length, fill)
    box_text = sp + strs[1 : len(strs) - 1 :] + sp
    return box_text
