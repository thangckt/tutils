from pathlib import Path


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


def download_rawtext(url: str, outfile: str = None) -> str:
    """Download raw text from a URL."""
    import requests

    res = requests.get(url)
    text = res.text
    if outfile is not None:
        with open(outfile, "w") as f:
            f.write(text)
    return text
