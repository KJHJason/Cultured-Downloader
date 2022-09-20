# import Python's standard libraries
import sys
import time
import json
import shutil
import pathlib
import zipfile
import platform
from typing import NoReturn, Any
import urllib.request as urllib_request

# import local libraries
try:
    from cultured_downloader import __version__
except (ModuleNotFoundError, ImportError):
    __version__ = "0.0.0"

MAX_REQUEST_RETRIES = 5
RETRY_DELAY = 1.5
CHROME_USER_AGENT = " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
OS_USER_AGENTS = {
    "Windows":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Linux":
        "Mozilla/5.0 (X11; Linux x86_64)",
    "Darwin":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6)"
}
USER_PLATFORM = platform.system()

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
            request.add_header("User-Agent", OS_USER_AGENTS[USER_PLATFORM] + CHROME_USER_AGENT)
            response = urllib_request.urlopen(request, timeout=10)
        except (urllib_request.HTTPError, urllib_request.URLError) as e:
            if (retry_counter == MAX_REQUEST_RETRIES):
                error_msg = f"Failed to fetch {url} due to {e}\n" \
                            "Please check your internet connection or try again."
                if (isinstance(e, urllib_request.HTTPError) and e.code == 403):
                    error_msg += "\nAdditionally, Cloudflare may be blocking your request due to a poor IP reputation."

                handle_shutdown(error_msg)
            time.sleep(RETRY_DELAY)
        else:
            return response

if (__name__ == "__main__"):
    release_info = fetch("https://cultureddownloader.com/api/v1/software/latest/version")
    release_info: dict = json.loads(release_info.read().decode("utf-8"))
    latest_version = release_info["version"]
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

        zipfile_path = folder.joinpath("cultured_downloader.zip")
        downloaded_file: bytes = fetch(release_info["download_url"]).read()
        with open(zipfile_path, "wb") as f:
            f.write(downloaded_file)

        with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
            zip_ref.extractall(folder)
        zipfile_path.unlink()

        if (is_updating):
            print("\nUpdate completed...")
        else:
            print("\nDownload completed...")

    try:
        from cultured_downloader import main as cultured_downloader_main, __version__
    except (ModuleNotFoundError, ImportError):
        handle_shutdown(
            "Failed to import Cultured Downloader, please try again or raise an issue on GitHub."
        )

    print(f"Launching Cultured Downloader {__version__}...\n")
    cultured_downloader_main()