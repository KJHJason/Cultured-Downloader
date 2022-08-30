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
    Additionally, this function will only download from the utils folder in
    CulturedDownloader github repository's src folder. The files downloaded will be 
    downloaded to the folder where the currently running Python file is located.

    Usage Example:
    >>> download_github_files(filename="utils.py")

    Args:
        filename (str): 
            The name of the file to download.

    Returns:
        None
    """
    file_path = FILE_PATH.joinpath("utils")
    if (not file_path.exists() and not file_path.is_dir()):
        file_path.mkdir()

    file_path = file_path.joinpath(filename)
    if (file_path.exists() and file_path.is_file()):
        return

    print(f"Missing {filename}, downloading from CulturedDownloader GitHub repository...")

    # TODO: change the url branch to main when the dev branch is merged to main
    code = urllib_request.urlopen(
        urllib_request.Request(f"https://raw.githubusercontent.com/KJHJason/Cultured-Downloader/dev/src/utils/{filename}"),
        timeout=10
    )

    with open(file_path, "w") as f:
        for line in code:
            f.write(line.decode("utf-8"))
    print(f"{filename} downloaded.\n")

try:
    from utils import *
except (ModuleNotFoundError, ImportError):
    pyFilesTuple = ("__init__.py", "crucial.py", "constants.py", "functional.py", "logger.py",
                    "download.py", "cryptography_operations.py", "cookie.py")
    for pyFile in pyFilesTuple:
        download_github_files(filename=pyFile)
from utils import *
from utils import __version__, __author__, __license__

# import third-party libraries
from colorama import Fore as F, init as colorama_init
from requests.exceptions import JSONDecodeError

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

    configs = load_configs()
    default_download_path = configs.get("download_directory")
    language = configs.get("language", "en")
    login_status = {}

    while (1):
        print_menu(login_status=login_status)
        user_action = get_input(
            "Enter command: ", regex=C.CMD_REGEX, 
            warning="Invalid command input, please enter a valid command from the menu above."
        )
        if (user_action == "x"):
            return
        elif (user_action == "1"):
            # Download images from Fantia post(s)
            pass
        elif (user_action == "2"):
            # Download all Fantia posts from creator(s)
            pass
        elif (user_action == "3"):
            # Download images from pixiv Fanbox post(s)
            pass
        elif (user_action == "4"):
            # Download all pixiv Fanbox posts from a creator(s)
            pass
        elif (user_action == "5"):
            # Change Default Download Folder
            pass
        elif (user_action == "6" and not (login_status.get("fantia") or login_status.get("pixiv"))):
            # Login
            pass
        else:
            # Report a bug
            opened_tab = webbrowser.open(C.ISSUE_PAGE, new=2)
            if (not opened_tab):
                print_warning(f"\nFailed to open web browser. Please visit the issue page manually and create an issue to report the bug at\n{C.ISSUE_PAGE}")
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