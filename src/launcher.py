# import Python's standard libraries
import sys
import time
import json
import shutil
import pathlib
import zipfile
from typing import NoReturn, Any
import urllib.request as urllib_request

# import local libraries
try:
    from cultured_downloader.utils.crucial import __version__
except (ModuleNotFoundError, ImportError):
    __version__ = "0.0.0"

MAX_REQUEST_RETRIES = 5
RETRY_DELAY = 1.5

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
            response = urllib_request.urlopen(urllib_request.Request(url), timeout=10)
        except (urllib_request.HTTPError, urllib_request.URLError) as e:
            if (retry_counter == MAX_REQUEST_RETRIES):
                handle_shutdown(
                    f"Failed to fetch {url} due to {e}\n"
                    "Please check your internet connection and try again."
                )
            time.sleep(RETRY_DELAY)
        else:
            return response

if (__name__ == "__main__"):
    release_info = fetch("https://cultureddownloader.com/api/v1/software/latest/version")
    release_info: dict = json.loads(release_info.read().decode("utf-8"))
    latest_version = release_info["version"]
    if (latest_version != __version__):
        print(f"Your CulturedDownloader is outdated, updating to {latest_version}...")

        folder = pathlib.Path(__file__).parent.absolute()
        folder.mkdir(parents=True, exist_ok=True)
        # remove any contents in the cultured_downloader folder
        cultured_downloader_folder = folder.joinpath("cultured_downloader")
        if (cultured_downloader_folder.exists() and cultured_downloader_folder.is_dir()):
            shutil.rmtree(cultured_downloader_folder)

        zipfile_path = folder.joinpath("cultured_downloader.zip")
        downloaded_file: bytes = fetch(release_info["download_url"]).read()
        with open(zipfile_path, "wb") as f:
            f.write(downloaded_file)

        with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
            zip_ref.extractall(folder)
        zipfile_path.unlink()

        print("\nUpdate completed...")

    try:
        from cultured_downloader.utils.crucial import __version__
        from cultured_downloader.cultured_downloader import main as cultured_downloader_main
    except (ModuleNotFoundError, ImportError):
        handle_shutdown(
            "Failed to import Cultured Downloader, please try again or raise an issue on GitHub."
        )

    print(f"Launching Cultured Downloader {__version__}...\n")
    cultured_downloader_main()