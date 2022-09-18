# import third-party libraries
import httpx
import pydantic
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# import Python's standard libraries
import json
import time
import asyncio
import pathlib
import subprocess
from typing import Optional, Union

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from user_data import save_google_oauth_json, load_google_oauth_json
    from functional import get_input, print_danger
    from schemas.google_oauth2_client import ClientSecret, GOOGLE_OAUTH_SCOPE
else:
    from .constants import CONSTANTS as C
    from .user_data import save_google_oauth_json, load_google_oauth_json
    from .functional import get_input, print_danger
    from .schemas.google_oauth2_client import ClientSecret, GOOGLE_OAUTH_SCOPE

class GoogleOAuth2:
    """Creates the base Google API service object that can be used for creating
    authenticated API calls to other Google APIs that requires Google OAuth2 authentication"""
    def __init__(self, credentials: Optional[dict] = None) -> None:
        if (credentials is None):
            self.__CREDENTIALS = None
        else:
            self.__CREDENTIALS = Credentials.from_authorized_user_info(
                info=credentials, 
                scopes=GOOGLE_OAUTH_SCOPE
            )

    def get_oauth_access_token(self) -> Union[str, None]:
        """Sends a request to Google and retrieve a short-lived 30 mins to 1 hour token"""
        if (self.__CREDENTIALS and self.CREDENTIALS.expired and self.CREDENTIALS.refresh_token):
            for _ in range(C.MAX_RETRIES):
                try:
                    self.CREDENTIALS.refresh(Request())
                except (RefreshError):
                    time.sleep(C.RETRY_DELAY)
                else:
                    return self.CREDENTIALS.token
            else:
                raise RefreshError("Failed to refresh the Google OAuth2 token.")

    @property
    def CREDENTIALS(self) -> Union[Credentials, None]:
        """Returns the credentials object that can be used to build other 
        authenticated Google API objects via the googleapiclient.discovery.build function"""
        return self.__CREDENTIALS

class GoogleDrive(GoogleOAuth2):
    """Creates an authenticated Google Drive Client that can be used 
    for communicating with Google Drive API v3 with async capabilities."""
    def __init__(self, credentials: Optional[dict] = None) -> None:
        super().__init__(credentials)
        self.__SERVICE = build(
            serviceName="drive",
            version="v3",
            credentials=self.CREDENTIALS
        )

    async def get_folder_contents(self, folder_id: str, gdrive_info: tuple[str, pathlib.Path], failed_requests_arr: list, headers: dict | None = None) -> list:
        """Sends a request to the Google Drive API to get the 
        json representation of the folder URL's directory structure

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
            dict:
                The json representation of the gdrive URL's directory structure
        """
        if (headers is None):
            headers = C.BASE_REQ_HEADERS.copy()
            headers["Authorization"] = f"Bearer {self.get_oauth_access_token()}"

        files, page_token = [], None
        async with httpx.AsyncClient(headers=headers, http2=True, timeout=10) as client:
            while (True):
                query = " ".join((f"'{folder_id}' in parents"))
                url = f"https://www.googleapis.com/drive/v3/files?q={query}&fields=nextPageToken,files(kind, id, name, mimeType)"
                if (page_token is not None):
                    url += f"&pageToken={page_token}"

                for _ in range(C.MAX_RETRIES):
                    try:
                        response = await client.get(url=url)
                        response.raise_for_status()
                    except (httpx.RequestError, httpx.HTTPStatusError, httpx.HTTPError):
                        await asyncio.sleep(C.RETRY_DELAY)
                    else:
                        break
                else:
                    failed_requests_arr.append(gdrive_info)
                    return

                response = response.json()
                for file in response.get("files", []):
                    files.append(file)

                page_token = response.get("nextPageToken", None)
                if (page_token is None):
                    break

        return {"id": folder_id, "directory": files}

    async def get_file_details(self, file_id: str, gdrive_info: tuple[str, pathlib.Path], failed_requests_arr: list, headers: dict | None = None) -> dict:
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
            dict:
                The json representation of the file's details
        """
        if (headers is None):
            headers = C.BASE_REQ_HEADERS.copy()
            headers["Authorization"] = f"Bearer {self.get_oauth_access_token()}"

        async with httpx.AsyncClient(headers=headers, http2=True, timeout=10) as client:
            for _ in range(C.MAX_RETRIES):
                try:
                    response = await client.get(
                        url=f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=kind, id, name, mimeType, owners, permissions"
                    )
                    response.raise_for_status()
                except (httpx.RequestError, httpx.HTTPStatusError, httpx.HTTPError):
                    await asyncio.sleep(C.RETRY_DELAY)
                else:
                    break
            else:
                failed_requests_arr.append(gdrive_info)
                return

        return {"id": file_id, "file": response.json()}

def start_google_oauth2_flow() -> Union[GoogleDrive, None]:
    """Starts the Google OAuth2 flow and returns the GoogleDrive object if successful, else None."""
    loaded_json = load_google_oauth_json()
    google_token = google_client = None
    for thread in loaded_json:
        if (thread.is_token and thread.result):
            google_token = thread.result
        elif (not thread.is_token and thread.result):
            google_client = thread.result

    if (google_token is not None):
        try:
            return Credentials.from_authorized_user_info(google_token, GOOGLE_OAUTH_SCOPE)
        except (ValueError):
            pass

    if (google_client is None):
        google_client_initially_none = True
        while (True):
            # TODO: Add an instructional guide link for the user to follow
            user_json = input("Enter the client secret JSON (X to cancel): ").strip()
            if (user_json in ("X", "x")):
                return

            try:
                ClientSecret.parse_raw(user_json)
            except (pydantic.ValidationError) as e:
                print_danger(f"User Error:\n{e}\n\nInvalid JSON, please try again.")
                continue
            else:
                google_client = user_json
                break
    else:
        google_client_initially_none = False
        google_client = json.dumps(google_client)

    # Construct the command for the subprocess
    cmd = "python" if (C.USER_PLATFORM == "Windows") else "python3"
    temp_saved_token_json = C.APP_FOLDER_PATH.joinpath("google-oauth2-token.json")
    commands = [
        cmd, str(C.ROOT_PY_FILE_PATH.joinpath("helper", "google_oauth.py")),
        "-j", google_client,
        "-s", " ".join(GOOGLE_OAUTH_SCOPE), 
        "-tp", str(temp_saved_token_json)
    ]

    while (True):
        # Open a new terminal window and start the OAuth2 flow
        # as the user would be stuck unless they close the terminal if they wish to cancel
        subprocess.call(commands, creationflags=subprocess.CREATE_NEW_CONSOLE)

        # Check if the flow was successful by checking if the token JSON file exists
        if (not temp_saved_token_json.exists() or not temp_saved_token_json.is_file()):
            print_danger("Google OAuth2 flow was not successful, please try again.\n")
            retry = get_input(
                input_msg="Do you want to retry the OAuth2 flow? (Y/n): ",
                inputs=("y", "n"),
                default="y"
            )
            if (retry == "n"):
                return
            else:
                continue

        with open(temp_saved_token_json, "r") as f:
            token_json = f.read()
        temp_saved_token_json.unlink()

        to_save = [(token_json, True)]
        if (google_client_initially_none):
            to_save.append((google_client, False))

        save_google_oauth_json(*to_save)
        return GoogleDrive(token_json)

def get_gdrive_service() -> Union[GoogleDrive, None]:
    """Returns the Google Drive service object if possible."""
    google_token = load_google_oauth_json(get_client=False)
    if (google_token is None):
        return None

    return GoogleDrive(google_token)

# test codes below
if (__name__ == "__main__"):
    start_google_oauth2_flow()