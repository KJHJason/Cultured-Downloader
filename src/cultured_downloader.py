# import Python's standard libraries
import sys
import pathlib
import asyncio
import urllib.request as urllib_request
import webbrowser

# import local libraries
FILE_PATH = pathlib.Path(__file__).parent.absolute()

def download_github_files(filename: str, folder: pathlib.Path, folder_name: str) -> None:
    """Download python files from CulturedDownloader github repository.

    This function does not use the requests library but urllib instead as
    it is one of Python's standard libraries.
    Additionally, this function will only download from the utils folder in
    CulturedDownloader github repository's src folder. The files downloaded will be 
    downloaded to the folder where the currently running Python file is located.

    Usage Example:
    >>> download_github_files(filename="__init__.py", folder=pathlib.Path("."), folder_name="utils")

    Args:
        filename (str): 
            The name of the file to download.
        folder (pathlib.Path):
            The folder to download the file to.
        folder_name (str):
            The name of the folder to download from in the CulturedDownloader github repository.

    Returns:
        None
    """
    if (not folder.exists() and not folder.is_dir()):
        folder.mkdir()

    file_path = folder.joinpath(filename)
    if (file_path.exists() and file_path.is_file()):
        return

    print(f"Missing {filename}, downloading from CulturedDownloader GitHub repository...")

    # TODO: change the url branch to main when the dev branch is merged to main
    code = urllib_request.urlopen(
        urllib_request.Request(
            f"https://raw.githubusercontent.com/KJHJason/Cultured-Downloader/dev/src/{folder_name}/{filename}"
        ),
        timeout=10
    )

    with open(file_path, "w") as f:
        for line in code:
            f.write(line.decode("utf-8"))
    print(f"{filename} downloaded.\n")

try:
    from utils import *
except (ModuleNotFoundError, ImportError):
    py_files = ("__init__.py", "constants.py", "crucial.py", "cryptography_operations.py", "download.py",
                "errors.py", "functional.py", "logger.py", "spinner.py", "user_data.py", "web_driver.py")
    schemas_files = ("__init__.py", "api_response.py", "config.py", "cookies.py")
    json_files = ("spinners.json",)

    for filenames, folder_name in zip([py_files, schemas_files, json_files], ["utils", "utils/schemas", "utils/json"]):
        folder_path = FILE_PATH.joinpath(*folder_name.split(sep="/"))
        for filename in filenames:
            download_github_files(filename=filename, folder=folder_path, folder_name=folder_name)

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

    configs: ConfigSchema = load_configs()
    default_download_path = configs.download_directory
    # language = configs.get("language", "en")
    login_status = {}

    with get_driver(".") as driver:
        with Spinner(
            message="Loading cookies if any...",
            colour="light_yellow",
            spinner_position="left",
            spinner_type="arc"
        ):
            load_tasks = [
                ("fantia", C.FANTIA_WEBSITE_URL, C.FANTIA_VERIFY_LOGIN_URL, load_cookie("fantia")), 
                ("pixiv", C.PIXIV_FANBOX_WEBSITE_URL, C.PIXIV_FANBOX_VERIFY_LOGIN_URL, load_cookie("pixiv"))
            ]
            for tasks in load_tasks:
                thread = tasks[-1]
                if (thread is not None):
                    tasks[-1].join()

            for website, website_url, verify_url, task in load_tasks:
                if (task is None):
                    continue

                driver.get(website_url)
                cookies = task.result
                if (cookies is not None and isinstance(cookies, dict)):
                    # Add cookies to the driver
                    login_status[website] = True
                    time.sleep(3)
                    driver.delete_all_cookies()
                    driver.add_cookie(cookies)

                    # verify if the cookies are valid
                    driver.get(verify_url)
                    time.sleep(3)
                    if (driver.current_url != verify_url):
                        login_status[website] = False
                        driver.delete_all_cookies()
                    else:
                        login_status[website] = True

        fantia_result = pixiv_result = None
        if (not login_status.get("fantia", False)):
            fantia_result = login(current_driver=driver, website="fantia")
            if (fantia_result is not None):
                login_status["fantia"] = True
        else:
            print_success("Successfully loaded Fantia cookies.")

        if (not login_status.get("pixiv", False)):
            pixiv_result = login(current_driver=driver, website="pixiv")
            if (pixiv_result is not None):
                login_status["pixiv"] = True
        else:
            print_success("Successfully loaded Pixiv Fanbox cookies.")

        save_fantia_cookie = isinstance(fantia_result, tuple)
        save_pixiv_cookie = isinstance(pixiv_result, tuple)
        if (save_fantia_cookie or save_pixiv_cookie):
            threads_arr = []
            with Spinner(
                message="Saving cookies...",
                colour="light_yellow",
                spinner_position="left",
                spinner_type="arc"
            ):
                if (fantia_result is not None and save_fantia_cookie):
                    fantia_thread = SaveCookieThread(cookie=fantia_result[0], website="fantia", save_locally=fantia_result[1])
                    fantia_thread.start()
                    threads_arr.append(fantia_thread)

                if (pixiv_result is not None and save_pixiv_cookie):
                    pixiv_thread = SaveCookieThread(cookie=pixiv_result[0], website="pixiv", save_locally=pixiv_result[1])
                    pixiv_thread.start()
                    threads_arr.append(pixiv_thread)

                for thread in threads_arr:
                    thread.join()

            for thread in threads_arr:
                if (not thread.result):
                    print_danger(f"Failed to save {thread.website} cookie.")

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
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print_warning("\nProgram terminated by user.")
        input("Please press ENTER to quit.")

    sys.exit(0)