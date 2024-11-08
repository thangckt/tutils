import shutil
from pathlib import Path


def make_dir(path: str, backup: bool = True):
    """Create a directory with a backup option."""
    path = Path(path)
    ### Create a backup path with a counter suffix
    if path.is_dir() and backup:
        counter = 0
        while True:
            bk_path = path.with_name(f"{path.name}_bk{counter:03d}")
            if not bk_path.exists():
                shutil.move(str(path), str(bk_path))
                break
            counter += 1
    ### Create the new directory
    path.mkdir(parents=True, exist_ok=True)
    return


def copy_file(src_path: str, dest_path: str):
    """
    Copy a file/folder from the source path to the destination path.
    """
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    new_path = shutil.copy2(src_path, dest_path)
    return new_path
