# import Python's standard libraries
import sys
import json
import pathlib
from typing import NoReturn
import urllib.request as urllib_request

# import local libraries
try:
    from utils.crucial import __version__
except (ModuleNotFoundError, ImportError):
    __version__ = "0.0.0"

# import local libraries
FILE_PATH = pathlib.Path(__file__).parent.absolute()

def print_failed_download_messages(error_msg: str) -> NoReturn:
    """Print failed download messages in the terminal.

    Args:
        error_msg (str):
            The error message to print.

    Raises:
        SystemExit as sys.exit(1) will be called at the end of the function.
    """
    print(error_msg)
    print("Please check your internet connection and try again.")
    input("Press ENTER to exit...")
    sys.exit(1)

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

    try:
        code = urllib_request.urlopen(
            urllib_request.Request(
                f"https://raw.githubusercontent.com/KJHJason/Cultured-Downloader/main/src/{folder_name}/{filename}"
            ),
            timeout=10
        )
    except (urllib_request.HTTPError) as e:
        print_failed_download_messages(
            f"Error downloading {filename} from CulturedDownloader GitHub repository:\n{e}"
        )
    except (urllib_request.URLError) as e:
        print_failed_download_messages(
            f"Error downloading {filename} from CulturedDownloader GitHub repository:\n{e}"
        )
    else:
        with open(file_path, "w") as f:
            for line in code:
                f.write(line.decode("utf-8"))
        print(f"{filename} downloaded.\n")

if (__name__ == "__main__"):
    try:
        release_info = urllib_request.urlopen(
                urllib_request.Request("https://api.github.com/repos/KJHJason/Cultured-Downloader/releases/latest"),
                timeout=10
            )
    except (urllib_request.URLError, urllib_request.HTTPError):
        print_failed_download_messages(
            "Failed to fetch release information from GitHub."
        )

    latest_ver = json.loads(release_info.read().decode("utf-8"))["tag_name"]
    if (latest_ver != __version__):
        print(f"Your CulturedDownloader is outdated, updating to {latest_ver}...")
        py_files = ("__init__.py", "constants.py", "crucial.py", "cryptography_operations.py", "download.py",
                "errors.py", "functional.py", "google_client.py", "logger.py", "spinner.py", "user_data.py", "web_driver.py")
        schemas_files = ("__init__.py", "api_response.py", "config.py", "cookies.py", "google_oauth2_client.py", "key_id_token.py")
        json_files = ("spinners.json",)
        helper_programs = ("google_oauth.py",)

        files_arr = [py_files, schemas_files, json_files, helper_programs]
        for filenames, folder_name in zip(files_arr, ["utils", "utils/schemas", "json", "helper"], strict=True):
            folder_path = FILE_PATH.joinpath(*folder_name.split(sep="/"))
            for filename in filenames:
                download_github_files(filename=filename, folder=folder_path, folder_name=folder_name)

        print("Update completed...\n")

    from utils.crucial import __version__
    from cultured_downloader import main as cultured_downloader_main
    print(f"Launching CulturedDownloader {__version__}...\n")
    cultured_downloader_main()