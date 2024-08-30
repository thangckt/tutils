
# import logging
# logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO)
import subprocess, sys


def check_installation(package_name: str,
                       git_repo: str = None,
                       auto_install: bool = False,
                       extra_commands: list[str] = None) -> None:
    """
    Check if the required packages are installed
    """
    try:
        __import__(package_name)
    except ImportError:
        if auto_install:
            _install_package(package_name, git_repo)
            if extra_commands:
                for command in extra_commands:
                    subprocess.run(command, check=True)
        else:
            raise ImportError(f"Required package `{package_name}` is not installed. Please install the package.")
    return


def _install_package(package_name: str,
                     git_repo: str = None) -> None:
    """
    Install the required package

    Args:
        package_name (str): package name
        git_repo (str): git path for the package
    """
    from .general_utils import create_logger
    logger = create_logger()

    try:
        logger.info(f"Installing the required packages: `{package_name}` ...")
        if git_repo:
            command = f"pip install -U git+{git_repo}"
        else:
            command = f"pip install -U {package_name}"

        subprocess.run(command, check = True)

        logger.info("Installation successful!")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while installing the package: {e}")

    return
