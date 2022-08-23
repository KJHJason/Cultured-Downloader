# import Python's standard libraries
import sys
import subprocess
import platform
import pathlib
from typing import NoReturn, Union, Optional

# define important constants
USER_PLATFORM = platform.system()

def install_dependency(dep: str) -> Union[None, NoReturn]:
    """Install a dependency using pip install using the subprocess module.

    Args:
        dep (str): 
            The name of the dependency to install.

    Usage example:
    >>> install_dependency(dep="cryptography")
    >>> install_dependency(dep="requests>2.8.0")
    >>> install_dependency(dep="aiohttp>=3.0.0,<4.0.0")

    Returns:
        None if the dependency is installed successfully, otherwise sys.exit(1) will be called.
    """
    print(f"{dep} module not found, CulturedDownloader will install it for you...")

    pipCmd = ["python3", "-m", "pip", "install", dep]
    if (USER_PLATFORM == "Windows"):
        pipCmd[0] = "python"

    try:
        subprocess.run(pipCmd, stdout=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError):
        print(f"{dep} module installation failed, please check your internet connection or pip install it manually.")
        sys.exit(1)
    else:
        print(f"{dep} module has been installed.\n")