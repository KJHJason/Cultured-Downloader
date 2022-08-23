# import Python's standard libraries
import sys
import pathlib
import urllib.request as urllib_request

# import local libraries
FILE_PATH = pathlib.Path(__file__).parent.absolute()

def download_github_files(filename: str) -> None:
    """Download python files from CulturedDownloader github repository.

    This function does not use the requests library but urllib instead as
    it is one of Python's standard libraries.
    Additionally, this function will only download from the functions folder in
    CulturedDownloader github repository's src folder. The files downloaded will be 
    downloaded to the folder where the currently running Python file is located.

    Usage Example:
    >>> download_github_files(filename="functions.py")

    Args:
        filename (str): 
            The name of the file to download.

    Returns:
        None
    """
    print(f"Missing {filename}, downloading from CulturedDownloader GitHub repository...")
    code = urllib_request.urlopen(
        urllib_request.Request(f"https://raw.githubusercontent.com/KJHJason/Cultured-Downloader/main/src/functions/{filename}"),
        timeout=10
    )

    filePath = FILE_PATH.joinpath("functions")
    if (not filePath.exists() and not filePath.is_dir()):
        filePath.mkdir()

    with open(filePath.joinpath(filename), "w") as f:
        for line in code:
            f.write(line.decode("utf-8"))
    print(f"{filename} downloaded.\n")

try:
    from functions.crucial import *
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="crucial.py")
    from functions.crucial import *

try:
    from functions.download import *
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="functions.py")
    from functions.download import *

try:
    from functions.cookie import *
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="cookie.py")
    from functions.cookie import *

# import third-party libraries
try:
    from colorama import Style, Fore as F, init as colorama_init
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="colorama")
    from colorama import Style, Fore as F, init as colorama_init

def main() -> int:
    return 0

if (__name__ == "__main__"):
    exitCode = main()
    sys.exit(exitCode)