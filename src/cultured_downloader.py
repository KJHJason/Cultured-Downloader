# import Python's standard libraries
import sys
if (sys.version_info[0] < 3 or sys.version_info[1] < 9):
    print("This program requires Python version 3.9 or higher!")
    input("Please press ENTER to exit...")
    sys.exit(1)
import asyncio
import webbrowser

# import local libraries
from utils import *
from utils import __version__, __author__, __license__

# import third-party libraries
from urllib3 import exceptions as urllib3_exceptions
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

def main_program(driver: webdriver.Chrome, configs: ConfigSchema) -> None:
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
        print_success("✓ Successfully loaded Fantia cookies.")

    if (not login_status.get("pixiv_fanbox", False)):
        pixiv_fanbox_login_result = login(
            current_driver=driver,
            website="pixiv_fanbox",
            login_status=login_status
        )
    else:
        print_success("✓ Successfully loaded Pixiv Fanbox cookies.")

    save_cookies(*[fantia_login_result, pixiv_fanbox_login_result])
    def download_process(website: str, creator_page: bool) -> None:
        """Download process for Fantia and Pixiv Fanbox."""
        try:
            asyncio.run(execute_download_process(
                website=website,
                creator_page=creator_page,
                download_path=configs.download_directory,
                driver=driver,
                login_status=login_status,
                drive_service=drive_service
            ))
        except (KeyboardInterrupt):
            return
        except (urllib3_exceptions.MaxRetryError):
            print_danger("Connection error, please try again later.")

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
            download_process(website="fantia", creator_page=False)

        elif (user_action == "2"):
            # Download all Fantia posts from creator(s)
            download_process(website="fantia", creator_page=True)

        elif (user_action == "3"):
            # Download images from pixiv Fanbox post(s)
            download_process(website="pixiv_fanbox", creator_page=False)

        elif (user_action == "4"):
            # Download all pixiv Fanbox posts from a creator(s)
            download_process(website="pixiv_fanbox", creator_page=True)

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
                print_success("Successfully removed your saved Google OAuth2 files.")

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
                delete_cookies("fantia")

            if (pixiv_fanbox_logged_in):
                logout(driver=driver, website="pixiv_fanbox", login_status=login_status)
                delete_cookies("pixiv_fanbox")

        else:
            # Report a bug
            opened_tab = webbrowser.open(C.ISSUE_PAGE, new=1)
            if (not opened_tab):
                print_warning(f"\nFailed to open web browser. Please visit the issue page manually and create an issue to report the bug at\n{C.ISSUE_PAGE}")
            else:
                print_success(f"\nA new tab has been opened in your web browser, please create an issue there to report the bug.")

def initialise() -> None:
    """Initialises the program and run the main program afterwards."""
    if (not C.DEBUG_MODE):
        sys.excepthook = exception_handler

    if (C.USER_PLATFORM == "Windows"):
        # escape ansi escape sequences on Windows terminal
        colorama_init(autoreset=False, convert=True)
        # A temporary fix for ProactorBasePipeTransport issues on
        # Windows OS Machines that may appear for older versions of Python
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
    with Spinner(
        message="Loading saved configs...",
        spinner_type="arc",
        colour="light_yellow",
        spinner_position="left",
        completion_msg="Successfully loaded saved configs!\n\n"
    ):
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
        main_program(driver=driver, configs=configs)

def main() -> None:
    """Main function that will run the program."""
    try:
        initialise()
        print_warning("\nThe program will now shutdown...")
        input("Please press ENTER to quit.")
    except (KeyboardInterrupt, EOFError):
        print_danger("\n\nProgram terminated by user.")
        input("Please press ENTER to quit.")

    delete_empty_and_old_logs()
    sys.exit(0)

if (__name__ == "__main__"):
    import httpx
    # check for latest version
    # if directly running this Python file.
    with httpx.Client(http2=True, headers=C.BASE_REQ_HEADERS) as client:
        for retry_counter in range(1, C.MAX_RETRIES + 1):
            try:
                response = client.get(
                    "https://cultureddownloader.com/api/v1/software/latest/version"
                )
                response.raise_for_status()
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError) as e:
                if (retry_counter == C.MAX_RETRIES):
                    print_danger("Failed to check for latest version.")
                    if (isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 403):
                        print_danger("You may have been blocked by Cloudflare due to a poor IP reputation.")
                    else:
                        print_danger("Please check your internet connection and try again.")

                    input("Please press ENTER to exit...")
                    sys.exit(1)

                time.sleep(C.RETRY_DELAY)
                continue
            else:
                software_info = response.json()
                latest_ver = software_info["version"]
                if (latest_ver != __version__):
                    print_warning(
                        f"New version {latest_ver} is available at {software_info['download_url']}\n"
                    )

    main()