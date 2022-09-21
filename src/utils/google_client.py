# import third-party libraries
import httpx
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# import Python's standard libraries
import sys
import json
import time
import asyncio
import pathlib
import webbrowser
import subprocess
from typing import Optional, Union

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from spinner import Spinner
    from logger import logger
    from user_data import save_google_oauth_json, load_google_oauth_json
    from functional import get_input, print_danger, validate_schema, print_success, print_warning
    from schemas.google_oauth2_client import ClientSecret, GOOGLE_OAUTH_SCOPE
else:
    from .constants import CONSTANTS as C
    from .spinner import Spinner
    from .logger import logger
    from .user_data import save_google_oauth_json, load_google_oauth_json
    from .functional import get_input, print_danger, validate_schema, print_success, print_warning
    from .schemas.google_oauth2_client import ClientSecret, GOOGLE_OAUTH_SCOPE

class GoogleOAuth2:
    """Creates the base Google API service object that can be used for creating
    authenticated API calls to other Google APIs that requires Google OAuth2 authentication

    Attributes:
        __CREDENTIALS (google.oauth2.credentials.Credentials):
                The credentials object that can be used to build other
                authenticated Google API objects via the googleapiclient.discovery.build function
    """
    def __init__(self, credentials: Optional[dict] = None) -> None:
        if (credentials is None):
            self.__CREDENTIALS = None
        else:
            self.__CREDENTIALS = Credentials.from_authorized_user_info(
                info=credentials, 
                scopes=GOOGLE_OAUTH_SCOPE
            )

            # check if the credentials is valid.
            # if it is invalid, program will stop
            # due to RefreshError being raised.
            self.get_oauth_access_token()

    def get_oauth_access_token(self) -> Union[str, None]:
        """Sends a request to Google and retrieve a short-lived 30 mins to 1 hour token"""
        if (self.__CREDENTIALS):
            if (self.__CREDENTIALS.expired and self.__CREDENTIALS.refresh_token):
                for retry_counter in range(1, C.MAX_RETRIES + 1):
                    try:
                        self.__CREDENTIALS.refresh(Request())
                    except (RefreshError):
                        if (retry_counter == C.MAX_RETRIES):
                            raise
                        time.sleep(C.RETRY_DELAY)
                    else:
                        return self.__CREDENTIALS.token
            else:
                return self.__CREDENTIALS.token

    @property
    def CREDENTIALS(self) -> Union[Credentials, None]:
        """Returns the credentials object that can be used to build other 
        authenticated Google API objects via the googleapiclient.discovery.build function"""
        return self.__CREDENTIALS

class GoogleDrive(GoogleOAuth2):
    """Creates an authenticated Google Drive Client that can be used 
    for communicating with Google Drive API v3 with async capabilities.

    Attributes:
        __SERVICE (googleapiclient.discovery.Resource):
            The Google Drive API service object that can be used for creating
            authenticated API calls to other Google APIs that requires Google OAuth2 authentication
    """
    def __init__(self, credentials: Optional[dict] = None, timeout: Optional[int] = 15) -> None:
        """Constructor for the GoogleDrive class

        Args:
            credentials (Optional[dict], optional):
                The credentials object that can be used to build other
                authenticated Google API objects via the googleapiclient.discovery.build function.
                Defaults to None.
            timeout (Optional[int], optional):
                The timeout value for the httpx.AsyncClient object.
        """
        if (credentials.get("scopes") != GOOGLE_OAUTH_SCOPE):
            raise ValueError("The provided credentials does not have the required scopes")

        super().__init__(credentials)
        self.timeout = timeout
        self.__SERVICE = build(
            serviceName="drive",
            version="v3",
            credentials=self.CREDENTIALS,
            static_discovery=False,
        )

    async def get_folder_contents(self, folder_id: str, gdrive_info: tuple[str, pathlib.Path], failed_requests_arr: list, headers: Optional[dict] = None) -> Union[tuple[str, tuple[str, pathlib.Path]], tuple[None, None]]:
        """Sends a request to the Google Drive API to get the 
        json representation of the folder's directory structure.

        Args:
            folder_id (str): 
                The ID of the Google Drive URL.
            gdrive_info (tuple[str, pathlib.Path]):
                The Google Drive info that contains the gdrive URL and the post folder path.
            failed_downloads_arr (list):
                The array that will be appended with the failed requests.
            headers (dict | None, optional):
                The headers to be used for the request. Defaults to None.

        Returns:
            tuple[str, tuple[str, pathlib.Path]] | tuple[None, None]]:
                The Google Drive API JSON response together with the supplied gdrive_info.
                A tuple of None if the request failed.
        """
        if (headers is None):
            headers = C.BASE_REQ_HEADERS.copy()
            headers["Authorization"] = f"Bearer {self.get_oauth_access_token()}"

        files, page_token = [], None
        query = f"'{folder_id}' in parents"
        async with httpx.AsyncClient(headers=headers, http2=True, timeout=self.timeout) as client:
            while (True):
                url = f"https://www.googleapis.com/drive/v3/files?q={query}&fields=nextPageToken,files(id,name,mimeType)"
                if (page_token is not None):
                    url += f"&pageToken={page_token}"

                for retry_counter in range(1, C.MAX_RETRIES + 1):
                    try:
                        response = await client.get(url=url)
                        response.raise_for_status()
                        json_response = response.json()
                    except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError) as e:
                        if (retry_counter == C.MAX_RETRIES):
                            logger.error(f"Failed to get gdrive folder content for {folder_id}: {e}")
                            failed_requests_arr.append((folder_id, gdrive_info[1], "folder", str(e)))
                            return (None, None)
                        await asyncio.sleep(C.RETRY_DELAY)
                    else:
                        break

                for file in json_response.get("files", []):
                    files.append(file)

                page_token = json_response.get("nextPageToken", None)
                if (page_token is None):
                    break

        return (files, gdrive_info)

    async def get_file_details(self, file_id: str, gdrive_info: tuple[str, pathlib.Path], failed_requests_arr: list, headers: Optional[dict] = None) -> Union[tuple[str, tuple[str, pathlib.Path]], tuple[None, None]]:
        """Sends a request to the Google Drive API to
        get the json representation of the file details.
        For async capability, a HTTP request will be sent instead of using
        the in-built Google Drive API, service.files().get(file_id=file_id).execute().
        Args:
            file_id (str): 
                The ID of the Google Drive file
            gdrive_info (tuple[str, pathlib.Path]):
                The Google Drive info that contains the gdrive URL and the post folder path.
            failed_downloads_arr (list):
                The array that will be appended with the failed requests.
            headers (dict | None, optional):
                The headers to be used for the request. Defaults to None.
        Returns:
            tuple[str, tuple[str, pathlib.Path]] | tuple[None, None]]:
                The Google Drive API JSON response together with the supplied gdrive_info.
                A tuple of None if the request failed.
        """
        if (headers is None):
            headers = C.BASE_REQ_HEADERS.copy()
            headers["Authorization"] = f"Bearer {self.get_oauth_access_token()}"

        async with httpx.AsyncClient(headers=headers, http2=True, timeout=self.timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    response = await client.get(
                        url=f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=id,name"
                    )
                    if (response.status_code == 404):
                        failed_requests_arr.append((file_id, gdrive_info[1], "file", str(e)))
                        return (None, None)

                    response.raise_for_status()
                    file_info = response.json()
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError) as e:
                    if (retry_counter == C.MAX_RETRIES):
                        logger.error(f"Failed to get gdrive file details for {file_id}: {e}")
                        failed_requests_arr.append((file_id, gdrive_info[1], "file", str(e)))
                        return (None, None)
                    await asyncio.sleep(C.RETRY_DELAY)
                else:
                    break

        return (file_info, gdrive_info)

    def download_file_id(self, file_id: str, file_name: str, folder_path: pathlib.Path, failed_downloads_arr: list) -> None:
        """Downloads the file from the Google Drive API service object using the file ID.

        Args:
            file_id (str): 
                The ID of the file to be downloaded.
            file_name (str):
                The name of the file to be downloaded.
            folder_path (pathlib.Path):
                The folder path where the file will be downloaded to.
            failed_downloads_arr (list):
                The array that will be appended with the failed requests.

        Returns:
            None
        """
        file_path = folder_path.joinpath(file_name)
        spinner_base_msg = f"Downloading a gdrive file from the post, {folder_path.name}: " + \
                            "{progress}% downloaded..."
        with Spinner(
            message=spinner_base_msg.format(progress=0),
            spinner_type="aesthetic",
            spinner_position="left",
            colour="light_yellow",
            completion_msg=f"Downloaded a gdrive file from the post, {folder_path.name}\n",
            cancelled_msg=f"Cancelled downloading a gdrive file from the post, {folder_path.name}\n"
        ) as spinner:
            if (file_path.exists() and file_path.is_file()):
                return

            try:
                with open(file_path, mode="wb") as file:
                    request = self.__SERVICE.files().get_media(fileId=file_id)
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    while (done is False):
                        status, done = downloader.next_chunk(num_retries=C.MAX_RETRIES)
                        progress = int(status.progress() * 100)
                        spinner.message = spinner_base_msg.format(
                            progress=progress if (progress > 0) else "?"
                        )
            except (HttpError) as e:
                file_path.unlink(missing_ok=True)
                logger.error(f"Failed to download gdrive file {file_id}: {e}")
                error_message = f"Failed to download a gdrive file from the post, {folder_path.name}!\n" \
                                f"GDrive URL: https://drive.google.com/file/d/{file_id}/view?usp=sharing\n" \
                                f"Error: {e}\n"
                failed_downloads_arr.append(
                    (folder_path, error_message)
                )
            except (KeyboardInterrupt):
                file_path.unlink(missing_ok=True)
                raise

def start_google_oauth2_flow() -> Union[GoogleDrive, None]:
    """Starts the Google OAuth2 flow and returns the GoogleDrive object if successful, else None."""
    google_token, google_client = load_google_oauth_json()
    if (google_token is not None):
        try:
            return Credentials.from_authorized_user_info(google_token, GOOGLE_OAUTH_SCOPE)
        except (ValueError):
            pass

    if (C.USER_PLATFORM != "Windows"):
        formatted_scopes = "' '".join(GOOGLE_OAUTH_SCOPE)
        suggested_action =  "you can manually set up the OAuth2 flow " \
                            "by running the google_oauth.py file with the required flags.\n" \
                            "Suggested flags:\n" \
                            f"-cp '{pathlib.Path.cwd()}/client_secret.json' " \
                            "<-- change this to the path where you saved your client secret JSON!\n" \
                            f"-s '{formatted_scopes}'\n" \
                            f"-tp '{C.TEMP_SAVED_TOKEN_JSON_PATH}'\n" \
                            f"-p 8080 <-- Defaults to port 8080 if not specified\n" \
                            "OAuth2 Helper program documentations: https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/google_oauth_helper_program.md\n"
        if (C.USER_PLATFORM == "Linux"):
            import distro # type: ignore *Only available on Linux
            if (distro.id() != "ubuntu"):
                print_danger(
                    "Disclaimer: If you run into any error, " \
                    "it is because this program uses the gnome terminal and has only been tested on Ubuntu 22.04\n" \
                    f"If you are facing any issues but wishes to enable GDrive downloads,\n{suggested_action}"
                )
        else:
            print_danger(
                "Since, you are not using Windows or Linux, this feature is not supported for your platform.\n" \
                f"Therefore, if you still want to enable GDrive downloads,\n{suggested_action}"
            )
            return

    if (getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")):
        # If running the PyInstaller executable
        helper_file_path = pathlib.Path(sys._MEIPASS).joinpath("google_oauth.py")
    else:
        helper_file_path = C.ROOT_PY_FILE_PATH.joinpath("helper", "google_oauth.py")

    if (google_client is None):
        google_client_initially_none = True
        if (not helper_file_path.exists() or not helper_file_path.is_file()):
            print_danger(
                "Could not find the Google OAuth2 helper Python file at\n" \
                f"{helper_file_path}\n" \
            )
            print_danger(
                "Please download the Google OAuth2 helper Python file from\n" \
                "https://github.com/KJHJason/Cultured-Downloader/blob/main/src/helper/google_oauth.py\n"
                "and place it in a helper folder in the same directory as Cultured Downloader.\n"
            )
            return

        print_warning(
            "Note: You will need to create a Google Cloud Platform project and " \
            "enable the Google Drive API for it.\n" \
            "If you are unsure on the steps to do so, please enter -h."
        )
        while (True):
            user_json = input("\nEnter the client secret JSON (X to cancel, -h for help): ").strip()
            if (user_json in ("X", "x")):
                return

            if (user_json == "-h"):
                opened_browser = webbrowser.open(
                    url=C.OAUTH2_GUIDE_PAGE,
                    new=1
                )
                if (opened_browser):
                    print_success("Please refer to the newly opened tab that contains the Google OAuth2 guide in your browser.")
                else:
                    print_danger("Failed to open the Google OAuth2 guide in your browser!")
                    print_danger(f"Please visit the following link manually:\n{C.OAUTH2_GUIDE_PAGE}")
                continue

            if (validate_schema(schema=ClientSecret, data=user_json, log_failure=False)):
                google_client = user_json
                break
            else:
                print_danger(f"User Error: Invalid JSON, please try again.")
    else:
        google_client_initially_none = False
        google_client = json.dumps(google_client)

    temp_saved_client_json = C.APP_FOLDER_PATH.joinpath("google-oauth2-client.json")
    with open(temp_saved_client_json, "w") as f:
        f.write(google_client)

    # Construct the command for the subprocess
    cmd = "python" if (C.USER_PLATFORM == "Windows") else "python3"
    commands = [
        cmd, str(helper_file_path),
        "-cp", str(temp_saved_client_json),
        "-s", " ".join(GOOGLE_OAUTH_SCOPE), 
        "-tp", str(C.TEMP_SAVED_TOKEN_JSON_PATH),
        "-p", "8080" # if changing port, the client secret JSON redirect URIs must be changed as well
    ]

    def delete_temp_files():
        temp_saved_client_json.unlink(missing_ok=True)
        C.TEMP_SAVED_TOKEN_JSON_PATH.unlink(missing_ok=True)

    while (True):
        # Open a new terminal window and start the OAuth2 flow
        # as the user would be stuck unless they close the terminal if they wish to cancel
        if (C.USER_PLATFORM == "Windows"):
            subprocess.call(commands, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # Tested on Ubuntu 22.04 but may not work on other distros
            subprocess.call(f"gnome-terminal --disable-factory -- {' '.join(commands)}", shell=True)

        # Check if the flow was successful by checking if the token JSON file exists
        if (not C.TEMP_SAVED_TOKEN_JSON_PATH.exists() or not C.TEMP_SAVED_TOKEN_JSON_PATH.is_file()):
            print_danger("Google OAuth2 flow was not successful, please try again.\n")
            retry = get_input(
                input_msg="Do you want to retry the OAuth2 flow? (Y/n): ",
                inputs=("y", "n"),
                default="y"
            )
            if (retry == "n"):
                delete_temp_files()
                return
            else:
                continue

        # Clear any text from the terminal
        # to the top of the terminal screen
        print("\x1b[2J\x1b[H", end="")

        # Load the generated token JSON file
        with open(C.TEMP_SAVED_TOKEN_JSON_PATH, "r") as f:
            token_json = f.read()

        delete_temp_files()

        to_save = [(token_json, True)]
        if (google_client_initially_none):
            to_save.append((google_client, False))

        save_google_oauth_json(*to_save)
        return GoogleDrive(json.loads(token_json))

def get_gdrive_service() -> Union[GoogleDrive, None]:
    """Returns the Google Drive service object if possible."""
    google_token = load_google_oauth_json(get_client=False)
    if (google_token is None):
        return None

    try:
        drive_service = GoogleDrive(google_token)
    except (RefreshError):
        drive_service = None
        print_danger("✗ Google OAuth2 token is no longer valid, please re-run the Google OAuth2 flow.")
    except (ValueError):
        drive_service = None
        print_danger("✗ Google OAuth2 token is invalid possibly due to missing GDrive scopes. Please re-run the Google OAuth2 flow")
    else:
        print_success("✓ Successfully loaded Google OAuth2 token!")
    return drive_service

# test codes below
if (__name__ == "__main__"):
    start_google_oauth2_flow()