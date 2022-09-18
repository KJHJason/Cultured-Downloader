# import Python's standard libraries
import sys
# Check user's Python version
if (sys.version_info[0] < 3 or sys.version_info[1] < 9):
    print("This program requires Python version 3.9 or higher!")
    input("Please press ENTER to exit...")
    sys.exit(1)
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
    if (not folder.exists() or not folder.is_dir()):
        folder.mkdir(parents=True)

    file_path = folder.joinpath(filename)
    if (file_path.exists() and file_path.is_file()):
        return

    print(f"Missing {filename}, downloading from CulturedDownloader GitHub repository...")

    # TODO: change the url branch to main when the dev branch is merged to main
    try:
        code = urllib_request.urlopen(
            urllib_request.Request(
                f"https://raw.githubusercontent.com/KJHJason/Cultured-Downloader/dev/src/{folder_name}/{filename}"
            ),
            timeout=10
        )
    except (urllib_request.HTTPError) as e:
        print(f"Error downloading {filename} from CulturedDownloader GitHub repository:\n{e}")
        print("Please check your internet connection and try again.")
        input("Press ENTER to exit...")
        sys.exit(1)
    except (urllib_request.URLError) as e:
        print(f"Error downloading {filename} from CulturedDownloader GitHub repository:\n{e}")
        print("Please check your internet connection and try again.")
        input("Press ENTER to exit...")
        sys.exit(1)
    else:
        with open(file_path, "w") as f:
            for line in code:
                f.write(line.decode("utf-8"))
        print(f"{filename} downloaded.\n")

try:
    from utils import *
except (ModuleNotFoundError, ImportError):
    py_files = ("__init__.py", "constants.py", "crucial.py", "cryptography_operations.py", "download.py",
                "errors.py", "functional.py", "logger.py", "spinner.py", "user_data.py", "web_driver.py", "google_client.py")
    schemas_files = ("__init__.py", "api_response.py", "config.py", "cookies.py")
    json_files = ("spinners.json",)
    helper_programs = ("google_oauth.py",)

    files_arr = [py_files, schemas_files, json_files, helper_programs]
    for filenames, folder_name in zip(files_arr, ["utils", "utils/schemas", "json", "helper"], strict=True):
        folder_path = FILE_PATH.joinpath(*folder_name.split(sep="/"))
        for filename in filenames:
            download_github_files(filename=filename, folder=folder_path, folder_name=folder_name)

from utils import *
from utils import __version__, __author__, __license__

# import third-party libraries
from colorama import Fore as F, init as colorama_init

def print_menu(login_status: dict[str, bool], drive_service: Union[GoogleDrive, None]) -> None:
    """Print the menu for the user to read and enter their desired action.

    Args:
        login_status (dict[str, bool]):
            The login status of the user,
            E.g. {"pixiv_fanbox": False, "fantia": True}
        drive_service (Any | None):
            The Google Drive API Service Object if it exists, None otherwise.

    Returns:
        None
    """
    fantia_status = login_status.get("fantia")
    pixiv_status = login_status.get("pixiv_fanbox")
    print(f"""{F.LIGHTYELLOW_EX}
> Login Status...
> Fantia: {'Logged In' if (fantia_status) else 'Guest (Not logged in)'}
> Pixiv: {'Logged In' if (pixiv_status) else 'Guest (Not logged in)'}
{C.END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{C.END} --------------------
      {F.GREEN}1. Download images from Fantia post(s){C.END}
      {F.GREEN}2. Download all Fantia posts from creator(s){C.END}
      {F.LIGHTCYAN_EX}3. Download images from pixiv Fanbox post(s){C.END}
      {F.LIGHTCYAN_EX}4. Download all pixiv Fanbox posts from a creator(s){C.END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{C.END} ----------------------
      {F.LIGHTBLUE_EX}5. Change Default Download Folder{C.END}""")

    if (drive_service is None):
        print(f"""      {F.LIGHTBLUE_EX}6. Configure Google OAuth2 for Google Drive API{C.END}""")
    else:
        print(f"""      {F.LIGHTBLUE_EX}6. Remove Saved Google OAuth2 files{C.END}""")

    if (not fantia_status or not pixiv_status):
        print(f"      {F.LIGHTBLUE_EX}7. Login{C.END}")
    if (fantia_status or pixiv_status):
        print(f"      {F.LIGHTBLUE_EX}8. Logout{C.END}")

    print(f"\n---------------------- {F.LIGHTYELLOW_EX}Other Options{C.END} ----------------------")
    print(f"      {F.LIGHTRED_EX}Y. Report a bug{C.END}")
    print(f"      {F.RED}X. Shutdown the program{C.END}")
    print()

async def main(driver: webdriver.Chrome, configs: ConfigSchema) -> None:
    """Main program function."""
    login_status = {}
    drive_service = get_gdrive_service()

    if (user_has_saved_cookies()):
        load_cookies = get_input(
            input_msg="Do you want to load in saved cookies to the current webdriver instance? (Y/n): ",
            inputs=("y", "n"),
            default="y"
        )
        if (load_cookies == "y"):
            load_cookies_to_webdriver(driver=driver, login_status=login_status)

    fantia_login_result = pixiv_fanbox_login_result = None
    if (not login_status.get("fantia", False)):
        fantia_login_result = login(
            current_driver=driver,
            website="fantia",
            login_status=login_status
        )
    else:
        print_success("Successfully loaded Fantia cookies.")

    if (not login_status.get("pixiv_fanbox", False)):
        pixiv_fanbox_login_result = login(
            current_driver=driver,
            website="pixiv_fanbox",
            login_status=login_status
        )
    else:
        print_success("Successfully loaded Pixiv Fanbox cookies.")

    save_cookies(*[fantia_login_result, pixiv_fanbox_login_result])
    while (True):
        print_menu(login_status=login_status, drive_service=drive_service)
        user_action = get_input(
            "Enter command: ", regex=C.CMD_REGEX, 
            warning="Invalid command input, please enter a valid command from the menu above."
        )
        if (user_action == "x"):
            return

        elif (user_action == "1"):
            # Download images from Fantia post(s)
            try:
                await execute_download_process(
                    website="fantia",
                    creator_page=False,
                    download_path=configs.download_directory,
                    driver=driver,
                    login_status=login_status,
                    drive_service=drive_service
                )
            except (KeyboardInterrupt):
                continue

        elif (user_action == "2"):
            # Download all Fantia posts from creator(s)
            try:
                await execute_download_process(
                    website="fantia",
                    creator_page=True,
                    download_path=configs.download_directory,
                    driver=driver,
                    login_status=login_status,
                    drive_service=drive_service
                )
            except (KeyboardInterrupt):
                continue

        elif (user_action == "3"):
            # Download images from pixiv Fanbox post(s)
            try:
                await execute_download_process(
                    website="pixiv_fanbox",
                    creator_page=False,
                    download_path=configs.download_directory,
                    driver=driver,
                    login_status=login_status,
                    drive_service=drive_service
                )
            except (KeyboardInterrupt):
                continue

        elif (user_action == "4"):
            # Download all pixiv Fanbox posts from a creator(s)
            try:
                await execute_download_process(
                    website="pixiv_fanbox",
                    creator_page=True,
                    download_path=configs.download_directory,
                    driver=driver,
                    login_status=login_status,
                    drive_service=drive_service
                )
            except (KeyboardInterrupt):
                continue

        elif (user_action == "5"):
            # Change Default Download Folder
            change_download_directory(configs=configs, print_message=True)
            configs = load_configs()

        elif (user_action == "6"):
            # Google OAuth2 Configurations
            if (drive_service is None):
                # Setup Google OAuth2
                drive_service = start_google_oauth2_flow()
                if (drive_service is not None):
                    print_success("Successfully set up Google OAuth2 and saved the JSON files.")
            else:
                # Remove Saved Google OAuth2 files
                confirm = get_input(
                    input_msg="Are you sure you want to remove your saved Google OAuth2 files? (y/N): ",
                    inputs=("y", "n"),
                    default="n"
                )
                if (confirm == "n"):
                    continue

                C.GOOGLE_OAUTH_CLIENT_SECRET.unlink(missing_ok=True)
                C.GOOGLE_OAUTH_CLIENT_TOKEN.unlink(missing_ok=True)
                drive_service = None
                print_success("Successfully removed saved Google OAuth2 files.")

        elif (user_action == "7"):
            # Login
            fantia_logged_in = login_status.get("fantia", False)
            pixiv_fanbox_logged_in = login_status.get("pixiv_fanbox", False)
            if (fantia_logged_in and pixiv_fanbox_logged_in):
                print_warning("You are already logged in to both Fantia and Pixiv Fanbox.")
                continue

            if (not fantia_logged_in):
                fantia_login_result = login(
                    current_driver=driver,
                    website="fantia",
                    login_status=login_status
                )
            if (not pixiv_fanbox_logged_in):
                pixiv_fanbox_login_result = login(
                    current_driver=driver,
                    website="pixiv_fanbox",
                    login_status=login_status
                )
            save_cookies(*[fantia_login_result, pixiv_fanbox_login_result])

        elif (user_action == "8"):
            # logout
            fantia_logged_in = login_status.get("fantia", False)
            pixiv_fanbox_logged_in = login_status.get("pixiv_fanbox", False)
            if (not fantia_logged_in and not pixiv_fanbox_logged_in):
                print_warning("You are not logged in to either Fantia or Pixiv Fanbox.")
                continue

            if (fantia_logged_in):
                logout(driver=driver, website="fantia", login_status=login_status)

            if (pixiv_fanbox_logged_in):
                logout(driver=driver, website="pixiv_fanbox", login_status=login_status)

        else:
            # Report a bug
            opened_tab = webbrowser.open(C.ISSUE_PAGE, new=2)
            if (not opened_tab):
                print_warning(f"\nFailed to open web browser. Please visit the issue page manually and create an issue to report the bug at\n{C.ISSUE_PAGE}")
            else:
                print_success(f"\nA new tab has been opened in your web browser, please create an issue there to report the bug.")

async def initialise() -> None:
    """Initialises the program and runs the main function."""
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

    # Ask before initialising the webdriver since
    # a change in the webdriver download path will
    # require the user to re-run the program.
    change_download_directory(configs=configs)

    # Check if the user has an active internet connection
    # before initialising the webdriver.
    if (not check_internet_connection()):
        print_danger("No internet connection detected. Please check your internet connection and try again.")
        return

    with get_driver(download_path=configs.download_directory) as driver:
        await main(driver=driver, configs=configs)

if (__name__ == "__main__"):
    # sys.excepthook = exception_handler
    if (C.USER_PLATFORM == "Windows"):
        # escape ansi escape sequences on Windows cmd
        colorama_init(autoreset=False, convert=True)

        # A temporary fix for ProactorBasePipeTransport issues on Windows OS Machines
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(initialise())
    except (KeyboardInterrupt, EOFError):
        print_danger("\n\nProgram terminated by user.")
        input("Please press ENTER to quit.")

    delete_empty_and_old_logs()
    sys.exit(0)