# import Python's standard libraries
import sys
import pathlib
import asyncio
import urllib.request as urllib_request
import webbrowser

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

    # TODO: change the url branch to main when the dev branch is merged to main
    code = urllib_request.urlopen(
        urllib_request.Request(f"https://raw.githubusercontent.com/KJHJason/Cultured-Downloader/dev/src/functions/{filename}"),
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
    from functions.crucial import __version__, __author__, __license__
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="crucial.py")
    from functions.crucial import __version__, __author__, __license__

try:
    from functions.constants import CONSTANTS as C
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="constants.py")
    from functions.constants import CONSTANTS as C

try:
    from functions.functional import *
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="functional.py")
    from functions.functional import *

try:
    from functions.logger import exception_handler
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="logger.py")
    from functions.logger import exception_handler

try:
    from functions.download import *
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="download.py")
    from functions.download import *

try:
    from functions.cookie import *
except (ModuleNotFoundError, ImportError):
    download_github_files(filename="cookie.py")
    from functions.cookie import *

# import third-party libraries
from colorama import Fore as F, init as colorama_init

def main() -> None:
    """Main function where the program starts."""
    print(f"""
=========================================== {F.LIGHTBLUE_EX}CULTURED DOWNLOADER v{__version__ }{C.END} ===========================================
================================ {F.LIGHTBLUE_EX}https://github.com/KJHJason/Cultured-Downloader{C.END} =================================
======================================== {F.LIGHTBLUE_EX}Author: {__author__}, aka Dratornic{C.END} =========================================
=============================================== {F.LIGHTBLUE_EX}License: {__license__}{C.END} =================================================
{F.LIGHTYELLOW_EX}
Purpose: Allows you to download multiple images from Fantia or Pixiv Fanbox automatically.

Note:    Requires the user to login via this program for images that requires a membership.
         This program is not affiliated with Pixiv or Fantia.{C.END}
{F.RED}
Warning:
Please read the term of use at https://github.com/KJHJason/Cultured-Downloader before using this program.{C.END}
""")

    loginStatus = {}

    while (1):
        print_menu(loginStatus=loginStatus)
        userAction = get_input(
            "Enter command: ", regex=C.CMD_REGEX, 
            warning="Invalid command input, please enter a valid command from the menu above."
        )
        if (userAction == "x"):
            return
        elif (userAction == "1"):
            # Download images from Fantia post(s)
            pass
        elif (userAction == "2"):
            # Download all Fantia posts from creator(s)
            pass
        elif (userAction == "3"):
            # Download images from pixiv Fanbox post(s)
            pass
        elif (userAction == "4"):
            # Download all pixiv Fanbox posts from a creator(s)
            pass
        elif (userAction == "5"):
            # Change Default Download Folder
            pass
        elif (userAction == "6" and not (loginStatus.get("fantia") or loginStatus.get("pixiv"))):
            # Login
            pass
        else:
            # Report a bug
            openedTab = webbrowser.open(C.ISSUE_PAGE, new=2)
            if (not openedTab):
                print_warning(f"\nFailed to open web browser. Please visit the issue page manually at\n{C.ISSUE_PAGE}")
            else:
                print_success(f"\nA new tab has been opened in your web browser, please create an issue there to report the bug.")

if (__name__ == "__main__"):
    # sys.excepthook = exception_handler

    if (C.USER_PLATFORM == "Windows"):
        # escape ansi escape sequences on Windows cmd
        colorama_init(autoreset=False, convert=True)

        # A temporary fix for ProactorBasePipeTransport issues 
        # on Windows OS Machines caused by aiohttp
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print_warning("\nProgram terminated by user.")
        input("Please press ENTER to quit.")

    sys.exit(0)