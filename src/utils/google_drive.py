# import third-party libraries
import httpx
import aiofiles

# import Python's standard libraries
import json
import asyncio
import pathlib
from typing import Optional, Union

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from spinner import Spinner, format_error_msg
    from logger import logger
    from user_data import load_gdrive_api_key
    from functional import  print_danger, async_file_exists, async_mkdir, \
                            async_remove_file, check_download_tasks, log_critical_details_for_post
else:
    from .constants import CONSTANTS as C
    from .spinner import Spinner, format_error_msg
    from .logger import logger
    from .user_data import load_gdrive_api_key
    from .functional import print_danger, async_file_exists, async_mkdir, \
                            async_remove_file, check_download_tasks, log_critical_details_for_post

class GoogleDrive:
    """Creates an authenticated Google Drive Client that can be used 
    for communicating with Google Drive API v3 with async capabilities.

    Attributes:
        __API_KEY (str):
            The API key that will be used to authenticate the Google Drive Client.
    """
    def __init__(self, api_key: str, 
                 timeout: Optional[int] = 60, max_concurrent_downloads: Optional[int] = 4) -> None:
        """Constructor for the GoogleDrive class

        Args:
            api_key (str):
                The API key that will be used to authenticate the Google Drive Client.
            timeout (int, optional):
                The timeout value for the httpx.AsyncClient object. Defaults to 60 seconds.
            max_concurrent_downloads (int, optional):
                The maximum number of concurrent downloads that can be performed at any given time.
                Defaults to 4 concurrent downloads.
        """
        self.__BASE_API_URL = "https://www.googleapis.com/drive/v3/files"
        self.__API_KEY = self.__check_api_key(api_key)
        self.timeout = timeout
        self.max_concurrent_downloads = max_concurrent_downloads

    def __check_api_key(self, api_key: str) -> str:
        """Checks if the API key is valid.

        Args:
            api_key (str):
                The API key to be checked.

        Returns:
            str:
                The API key if it is valid.

        Raises:
            ValueError: 
                If the API key is invalid.
            ConnectionError:
                When the API key could not verified due to connection errors from the client or the server.
        """
        headers = C.BASE_REQ_HEADERS.copy()
        for retry_counter in range(1, C.MAX_RETRIES + 1):
            try:
                response = httpx.get(f"{self.__BASE_API_URL}?key={api_key}", headers=headers)
                if (response.status_code == 400):
                    raise ValueError("Invalid API key.")
                return api_key # Although the API key is valid, Google Drive API will return a 403 Forbidden error.
            except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
                if (retry_counter == C.MAX_RETRIES):
                    raise ConnectionError("Could not verify API key due to connection errors.")

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

        files, page_token = [], None
        query = f"'{folder_id}' in parents"
        async with httpx.AsyncClient(headers=headers, http2=True, timeout=self.timeout) as client:
            while (True):
                url = f"{self.__BASE_API_URL}?key={self.__API_KEY}&q={query}&fields=nextPageToken,files(id,name,mimeType)"
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

        async with httpx.AsyncClient(headers=headers, http2=True, timeout=self.timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    response = await client.get(
                        url=f"{self.__BASE_API_URL}/{file_id}?key={self.__API_KEY}&fields=id,name,mimeType"
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

    async def download_file_id(self, file_id: str, file_name: str, folder_path: pathlib.Path, 
                               failed_downloads_arr: list, headers: Optional[dict] = None) -> None:
        """Downloads the file from the Google Drive v3 API asynchronously using the file ID.

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
        file_path = folder_path.joinpath("gdrive", file_name.strip()).resolve()
        if (await async_file_exists(file_path)):
            return

        if (headers is None):
            headers = C.BASE_REQ_HEADERS.copy()

        # Construct the API URL and add the API key and 
        # alt=media to tell Google that we would like to download the file
        url = f"{self.__BASE_API_URL}/{file_id}?key={self.__API_KEY}&alt=media"
        await async_mkdir(file_path.parent, parents=True, exist_ok=True)
        async with httpx.AsyncClient(
            headers=headers, 
            http2=True, 
            timeout=60
        ) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    async with client.stream(method="GET", url=url) as response:
                        response.raise_for_status()
                        async with aiofiles.open(file_path, "wb") as f:
                            async for chunk in response.aiter_bytes(chunk_size=C.CHUNK_SIZE):
                                await f.write(chunk)
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, httpx.StreamError) as e:
                    await async_remove_file(file_path)
                    if (retry_counter == C.MAX_RETRIES):
                        error_message = f"Failed to download a gdrive file from the post, {folder_path.name}!\n" \
                                f"GDrive URL: https://drive.google.com/file/d/{file_id}/view?usp=sharing\n" \
                                f"Error: {e}\n"
                        failed_downloads_arr.append(
                            (folder_path, error_message)
                        )
                        return
                    await asyncio.sleep(C.RETRY_DELAY)
                except (asyncio.CancelledError):
                    await async_remove_file(file_path)
                    raise
                else:
                    break

    async def download_multiple_files(self, file_arr: list[tuple[str, str, str, tuple[str, pathlib.Path]]]) -> None:
        """Download multiple files asynchronously.

        Args:
            file_arr (list[tuple[str, str, str, tuple[str, pathlib.Path]]]):
                A list of tuples containing the file ID(s), file name, and mimetype and
                a tuple of the original gdrive URL and the post folder that the gdrive URL was found in.

        Returns:
            None
        """
        allowed_for_downloads_arr = []
        not_allowed_for_downloads_arr = []
        for file in file_arr:
            mimetype = file[2]
            if ("application/vnd.google-apps" in mimetype):
                not_allowed_for_downloads_arr.append(file)
            else:
                allowed_for_downloads_arr.append(file)

        if (len(allowed_for_downloads_arr) > 0):
            base_spinner_msg = "Downloaded {progress} out of " + \
                            f"{len(allowed_for_downloads_arr)} gdrive files..."
            with Spinner(
                message=base_spinner_msg.format(progress=0),
                colour="light_yellow",
                spinner_position="left",
                spinner_type="material",
                completion_msg=f"Finished downloading all {len(allowed_for_downloads_arr)} gdrive URL(s)!\n",
                cancelled_msg=f"GDrive download process has been cancelled!\n"
            ) as spinner:
                finished_downloads = 0
                download_tasks = set()
                failed_downloads_arr = []
                not_allowed_for_downloads_arr = []
                headers = C.BASE_REQ_HEADERS.copy()
                for file in file_arr:
                    file_id, file_name, mimetype, gdrive_info = file
                    if ("application/vnd.google-apps" in mimetype):
                        not_allowed_for_downloads_arr.append(file)
                        continue

                    if (len(download_tasks) >= self.max_concurrent_downloads):
                        done, download_tasks = await check_download_tasks(
                            download_tasks,
                            all_completed=False
                        )
                        finished_downloads += len(done)
                        spinner.message = base_spinner_msg.format(
                            progress=finished_downloads
                        )

                    download_tasks.add(
                        asyncio.create_task(
                            self.download_file_id(
                                file_id=file_id,
                                file_name=file_name,
                                folder_path=gdrive_info[1],
                                failed_downloads_arr=failed_downloads_arr,
                                headers=headers,
                            )
                        )
                    )

                # Wait for any remaining downloads to finish
                done, _ = await check_download_tasks(
                    download_tasks,
                    all_completed=True
                )

            if (len(failed_downloads_arr) > 0):
                for folder_path, error_msg in failed_downloads_arr:
                    log_critical_details_for_post(
                        post_folder=folder_path,
                        message=error_msg,
                        log_filename="gdrive_download.log"
                    )

        if (len(not_allowed_for_downloads_arr) > 0):
            for file in not_allowed_for_downloads_arr:
                file_id, file_name, mimetype, gdrive_info = file
                log_critical_details_for_post(
                    post_folder=gdrive_info[1],
                    message=f"The gdrive file, {file_name}, is not allowed for downloads!\n" \
                            f"File ID: {file_id}\n" \
                            f"File name: {file_name}\n" \
                            f"Mimetype: {mimetype}\n",
                    log_filename="gdrive_download.log"
                )

def validate_gdrive_api_key(gdrive_api_key: str, print_error: Optional[bool] = False) -> Union[GoogleDrive, None]:
    """Validate the Google Drive API key.

    Args:
        api_key (str): 
            The Google Drive API key to validate.

    Returns:
        Union[GoogleDrive, None]: 
            The GoogleDrive object if the API key is valid, None otherwise.
    """
    try:
        temp_gdrive_service = GoogleDrive(gdrive_api_key)
    except (ValueError):
        if (print_error):
            print_danger(
                "Invalid Google Drive API key. Please enter a working Google Drive API key.\n"
            )
        return
    except (ConnectionError):
        if (print_error):
            print_danger(
                "Connection error when trying to validate the given API key, please try again later.\n"
            )
        return
    else:
        return temp_gdrive_service

def get_gdrive_service() -> Union[GoogleDrive, None]:
    """Returns the Google Drive service object if possible."""
    with Spinner(
        message="Loading Google Drive API key...",
        colour="light_yellow",
        spinner_position="left",
        spinner_type="arc",
        completion_msg="Finished loading Google Drive API key!\n"
    ) as spinner:
        gdrive_api_key = load_gdrive_api_key()
        if (gdrive_api_key is False):
            spinner.completion_msg = ""
            return
        if (gdrive_api_key is None):
            spinner.completion_msg = format_error_msg(
                "Could not load Google Drive API Key either due to connection error or decryption issues.\n"
            )
            return

        drive_service = validate_gdrive_api_key(gdrive_api_key)
        if (drive_service is None):
            spinner.completion_msg = format_error_msg(
                "Failed to validate Google Drive API key.\n"
            )
            return
        return drive_service