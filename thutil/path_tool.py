import shutil
import warnings
from glob import glob
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


def scan_paths(
    paths: list[str],
    with_files: list[str],
    without_files: list[str] = [],
) -> list[str]:
    """Check if the paths contains and not contains some files.

    Args:
        paths (list[str]): The paths of dirs to scan.
        with_files (list[str]): The files that should exist in the path.
        without_files (list[str], optional): The files that should not exist in the work_path. Defaults to [].

    Returns:
        list[str]: The paths that meet the conditions.
    """
    found_paths = [
        p for p in paths if all(Path(f"{p}/{f}").exists() for f in with_files)
    ]
    found_paths = [
        p
        for p in found_paths
        if all(not Path(f"{p}/{f}").exists() for f in without_files)
    ]
    return found_paths


def remove_files_in_paths(files: list, paths: list) -> None:
    """Remove files in the `files` list in the `paths` list."""
    _ = [Path(f"{p}/{f}").unlink() for p in paths for f in files]
    return
