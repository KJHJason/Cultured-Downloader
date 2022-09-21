# import Python's standard libraries
import sys
import time
import json
import shutil
import pathlib
import zipfile
from typing import NoReturn, Any
import urllib.request as urllib_request
from argparse import ArgumentParser, BooleanOptionalAction

# import local libraries
try:
    from cultured_downloader import __version__
except (ModuleNotFoundError, ImportError):
    __version__ = "0.0.0"

MAX_REQUEST_RETRIES = 5
RETRY_DELAY = 1.5
OUTDATED_LAUNCHER_MSG = "\nPlease try again, or" \
                        "check for a newer launcher on Cultured Downloader's GitHub Repository.\n" \
                        "You may also raise an issue on Cultured Downloader's GitHub Repository if you are unable to resolve this issue."

def handle_shutdown(error_msg: str) -> NoReturn:
    """Print the supplied error message in the terminal and exit the application.

    Args:
        error_msg (str):
            The error message to print.

    Raises:
        SystemExit as sys.exit(1) will be called at the end of the function.
    """
    print(error_msg)
    input("Press ENTER to exit...")
    sys.exit(1)

def fetch(url: str) -> Any:
    """Make a request to the given URL and return the response.

    This function does not use the requests library but urllib instead as
    it is one of Python's standard libraries.

    Usage Example:
    >>> fetch("https://www.google.com")

    Args:
        url (str):
            The URL to make a request to.

    Returns:
        Any:
            The response from the request.
    """
    for retry_counter in range(1, MAX_REQUEST_RETRIES + 1):
        try:
            request = urllib_request.Request(url)
            response = urllib_request.urlopen(request, timeout=10)
        except (urllib_request.HTTPError, urllib_request.URLError) as e:
            if (retry_counter == MAX_REQUEST_RETRIES):
                error_msg = f"Failed to fetch {url} after {MAX_REQUEST_RETRIES} retries due to {e}"
                if (isinstance(e, urllib_request.HTTPError)):
                    if (e.code == 403):
                        error_msg += "\nAdditionally, you might be rate limited by GitHub's API in which you can try again later in an hour time."
                        error_msg += "\nAlternatively, you can skip the update check by running the program with the --skip-update or -s flag."
                else:
                    error_msg += "\nPlease check your internet connection or try again."

                handle_shutdown(error_msg)
            time.sleep(RETRY_DELAY)
        else:
            return response

if (__name__ == "__main__"):
    parser = ArgumentParser(
        description="A program to launch the main program, Cultured Downloader.\n" \
                    "By running this program, the latest version of Cultured Downloader will " \
                    "be automatically downloaded if it is not already up-to-date."
    )
    parser.add_argument(
        "-s", "--skip-update",
        action=BooleanOptionalAction,
        default=False,
        required=False,
        help="Skip the update check and launch the main program directly."
    )
    args = parser.parse_args()

    if (not args.skip_update):
        release_info = fetch("https://api.github.com/repos/KJHJason/Cultured-Downloader/releases/latest")
        release_info: dict = json.loads(release_info.read().decode("utf-8"))
        latest_version = release_info["tag_name"]
        if (latest_version != __version__):
            is_updating = (__version__ != "0.0.0")
            if (is_updating):
                print(f"Cultured Downloader is outdated, updating to {latest_version}...")
            else:
                print(f"Cultured Downloader is missing some files, downloading {latest_version}...")

            folder = pathlib.Path(__file__).parent.absolute()
            folder.mkdir(parents=True, exist_ok=True)
            # remove any contents in the folder path except for the launcher and any compiled bytecodes
            for file in folder.iterdir():
                if (file.name != "launcher.py"):
                    if (file.is_dir()):
                        shutil.rmtree(file)
                    else:
                        file.unlink()

            # download the latest release
            zipfile_path = folder.joinpath("cultured_downloader.zip")
            downloaded_file: bytes = fetch(release_info["zipball_url"]).read()
            with open(zipfile_path, "wb") as f:
                f.write(downloaded_file)

            with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
                zip_ref.extractall(folder)
            zipfile_path.unlink()

            # Look for the folder that was extracted from the zip file
            extracted_folder_path = None
            for path in folder.iterdir():
                if (path.is_dir() and path.name.startswith("KJHJason-Cultured-Downloader-")):
                    extracted_folder_path = path
                    break
            else:
                handle_shutdown("Failed to find the extracted folder." + OUTDATED_LAUNCHER_MSG)

            # Look for the src folder after finding the extracted folder
            src_folder_path = None
            for github_path in extracted_folder_path.iterdir():
                if (github_path.is_dir() and github_path.name == "src"):
                    src_folder_path = github_path
                    break
            else:
                handle_shutdown("Failed to find the src folder." + OUTDATED_LAUNCHER_MSG)

            # Move the contents of the src folder to the main folder
            # where the launcher is located and being run from
            for src_path in src_folder_path.iterdir():
                if (src_path.is_file() and src_path.name == "launcher.py"):
                    continue
                shutil.move(src_path, folder)

            shutil.rmtree(extracted_folder_path)
            if (is_updating):
                print("Update completed...")
            else:
                print("Download completed...")
    else:
        print("Skipping update check...")

    try:
        from cultured_downloader import main as cultured_downloader_main, __version__
    except (ModuleNotFoundError, ImportError):
        if (not args.skip_update):
            handle_shutdown("Failed to import Cultured Downloader." + OUTDATED_LAUNCHER_MSG)
        else:
            handle_shutdown(
                "Failed to import Cultured Downloader, please try again or " \
                "run the launcher without the --skip-update or -s flag."
            )

    print(f"Launching Cultured Downloader {__version__}...")
    cultured_downloader_main()