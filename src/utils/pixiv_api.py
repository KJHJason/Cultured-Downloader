# import third-party libraries
import httpx
import aiofiles
from PIL import Image

# import Python's standard libraries
import time
import json
import base64
import shutil
import random
import zipfile
import pathlib
import hashlib
import secrets
import asyncio
import webbrowser
import urllib.parse as urlparse
from typing import Any, Optional, Union

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from spinner import Spinner
    from user_data import save_pixiv_refresh_token, load_pixiv_refresh_token
    from download import log_critical_details_for_post
    from functional import print_danger, print_success, check_download_tasks, remove_illegal_chars_in_path
    from errors import PixivOAuthRefreshedError, PixivOAuthRefreshError
    from functional import async_mkdir, async_remove_file, async_file_exists, get_input
else:
    from .constants import CONSTANTS as C
    from .spinner import Spinner
    from .user_data import save_pixiv_refresh_token, load_pixiv_refresh_token
    from .download import log_critical_details_for_post
    from .functional import print_danger, print_success, check_download_tasks, remove_illegal_chars_in_path
    from .errors import PixivOAuthRefreshedError, PixivOAuthRefreshError
    from .functional import async_mkdir, async_remove_file, async_file_exists, get_input

class PixivAPI:
    """PixivAPI object that handles all the requests to the Pixiv API.

    Code mainly inspired by:
        https://github.com/upbit/pixivpy

    Before using any of the methods, if the object does not have a refresh token yet,
    you must call the start_oauth_flow method to get one.

    Attributes:
        __URL (str):
            Base URL for the Pixiv API.
        __CLIENT_ID (str):
            Client ID for the Pixiv API.
        __USER_AGENT (str):
            User agent for the Pixiv API.
        __CLIENT_SECRET (str):
            Client secret for the Pixiv API.
        __AUTH_TOKEN_URL (str):
            URL for the Pixiv API to get an OAuth token.
        __LOGIN_URL (str):
            URL for the Pixiv API to login.
        __REDIRECT_URI (str):
            Redirect URI for the Pixiv API.
        max_concurrent_downloads (int):
            Maximum number of concurrent downloads when calling the download_multiple_illust method.
        refresh_token (str):
            Refresh token to use to get a new access token (lasts for 1 hour).
        access_token (str):
            Access token to use for the Pixiv API.
        api_timeout (int):
            Timeout for the Pixiv API requests.
        download_timeout (int):
            Timeout for when downloading files.
    """
    def __init__(self, refresh_token: Optional[str] = None, access_token: Optional[str] = None, 
                 max_concurrent_downloads: Optional[int] = 4, 
                 api_timeout: Optional[int] = 15, download_timeout: Optional[int] = 60) -> None:
        """Constructor method for the PixivAPI class.

        Args:
            refresh_token (str, optional):
                Refresh token to use to get a new access token (lasts for 1 hour). Defaults to None.
            access_token (str, optional):
                Access token to use for the Pixiv API. 
                Defaults to None which will use the refresh token to get a new one if the refresh token was provided.
            max_concurrent_downloads (int, optional):
                Maximum number of concurrent downloads when calling the download_multiple_illust method. 
                Defaults to 4.
            api_timeout (int, optional):
                Timeout for the Pixiv API requests. Defaults to 15.
            download_timeout (int, optional):
                Timeout for when downloading files. Defaults to 60.
        """
        self.__URL = "https://app-api.pixiv.net"
        self.__CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
        self.__USER_AGENT = "PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)"
        self.__CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"
        self.__AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"
        self.__LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
        self.__REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"

        self.api_timeout = api_timeout
        self.download_timeout = download_timeout
        self.max_concurrent_downloads = max_concurrent_downloads
        self.refresh_token = refresh_token
        self.access_token = access_token
        if (access_token is None and self.refresh_token is not None):
            self.refresh_oauth_token()

    @staticmethod
    def s256(data: bytes) -> str:
        """S256 transformation method.

        Args:
            data (bytes): 
                Data to be transformed.

        Returns:
            str:
                Transformed data.
        """
        hashed_data = hashlib.sha256(data).digest()
        return base64.urlsafe_b64encode(hashed_data).rstrip(b"=").decode("ascii")

    def start_oauth_flow(self) -> Union[str, None]:
        """Start OAuth flow to get refresh token.

        Credits: https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362

        Returns:
            str | None:
                Refresh token if the flow was successful, None otherwise.
        """
        # Proof Key for Code Exchange by OAuth Public Clients (RFC7636)
        code_verifier = secrets.token_urlsafe(32)
        code_challenge = self.s256(code_verifier.encode("ascii"))
        login_params = {
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "client": "pixiv-android",
        }

        login_url = f"{self.__LOGIN_URL}?{urlparse.urlencode(login_params)}"
        opened_tab = webbrowser.open(
            url=login_url, 
            new=1
        )
        if (not opened_tab):
            print_danger(
                f"Failed to open browser tab. Please open the following URL manually:\n{login_url}\n"
            )
        else:
            # TODO: update guide link
            print_success(
                f"Opened a new tab in your browser to\n{login_url}\n" \
                "If unsure, you can enter '-h' to open a new tab to my guide.\n" \
            )

        headers = {"User-Agent": "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"}
        with httpx.Client(http2=True, headers=headers, timeout=self.api_timeout) as client:
            while (True):
                code = get_input(
                    input_msg="Enter the code from your browser's console (X to cancel, -h for help): ",
                    regex=C.PIXIV_REFRESH_TOKEN_INPUT_REGEX,
                    is_case_sensitive=True
                )
                if (code in ("x", "X")):
                    return
                elif (code == "-h"):
                    opened_tab = webbrowser.open(
                        url=C.PIXIV_OAUTH_GUIDE_PAGE,
                        new=1
                    )
                    if (opened_tab):
                        print_success("Opened a new tab in your browser to the guide.\n")
                    else:
                        print_danger(
                            f"Failed to open browser tab. Please open the following URL manually:\n{C.PIXIV_OAUTH_GUIDE_PAGE}\n" 
                        )

                try:
                    r = client.post(
                        url=self.__AUTH_TOKEN_URL,
                        data={
                            "client_id": self.__CLIENT_ID,
                            "client_secret": self.__CLIENT_SECRET,
                            "code": code,
                            "code_verifier": code_verifier,
                            "grant_type": "authorization_code",
                            "include_policy": "true",
                            "redirect_uri": self.__REDIRECT_URI,
                        }
                    )
                    r.raise_for_status()
                    data = r.json()
                except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                    print_danger(f"Request Error: {e}\nPlease check your internet connection and try again.\n")
                except (httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError) as e:
                    print_danger(f"Response Error: {e}\nPlease check your code and try again.\n")
                else:
                    break

        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        save_pixiv_refresh_token(self.refresh_token)
        return self.refresh_token

    def refresh_oauth_token(self, response: Optional[httpx.Response] = None, 
                            raise_error: Optional[bool] = False) -> bool:
        """Refresh the user's access token using the refresh token.

        Args:
            response (httpx.Response, optional):
                Response object to check if the access token is expired. Defaults to None.
            raise_error (bool, optional):
                Whether to raise an error if the access token has been refreshed. Defaults to False.

        Returns:
            bool:
                Whether the access token has been refreshed.

        Raises:
            PixivOAuthRefreshedError:
                If the access token has been refreshed and raise_error is True.
            PixivOAuthRefreshError:
                If the access token could not be refreshed.
        """
        if (response is not None):
            if (response.status_code != 400):
                return False
            if ("invalid_grant" not in response.json()["error"]["message"]):
                return False

        headers = {"User-Agent": self.__USER_AGENT}
        data = {
            "client_id": self.__CLIENT_ID,
            "client_secret": self.__CLIENT_SECRET,
            "grant_type": "refresh_token",
            "include_policy": "true",
            "refresh_token": self.refresh_token,
        }
        with httpx.Client(http2=True, headers=headers, timeout=self.api_timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    data = client.post(self.__AUTH_TOKEN_URL, data=data)
                    data.raise_for_status()
                    data = data.json()
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError):
                    if (retry_counter == C.MAX_RETRIES):
                        raise PixivOAuthRefreshError("OAuth token refresh failed")
                    time.sleep(C.RETRY_DELAY)
                else:
                    break

        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        if (raise_error):
            raise PixivOAuthRefreshedError("OAuth token refreshed")
        return True

    def get_headers(self, **kwargs) -> dict:
        """Get the required headers to communicate with the Pixiv API.

        Returns:
            dict:
                Headers to use in the request.
        """
        headers = {
            "User-Agent": self.__USER_AGENT,
            "App-OS": "ios",
            "App-OS-Version": "14.6",
            "Authorization": f"Bearer {self.access_token}",
        }
        if (kwargs):
            headers.update(kwargs)
        return headers

    @staticmethod
    def get_illust_url(illust_id: Union[str, int]) -> str:
        """Get the URL of an illustration.

        Args:
            illust_id (str | int):
                ID of the illustration.

        Returns:
            str:
                URL of the illustration.
        """
        return f"https://www.pixiv.net/en/artworks/{illust_id}"

    def __append_to_failed_requests_arr(self, failed_requests_arr: Union[list, None], to_append: Any) -> None:
        """Append to failed requests array if failed_requests_arr is not None.

        Args:
            failed_requests_arr (list | None):
                Array to append to.
            to_append (Any):
                Data to append.

        Returns:
            None
        """
        if (failed_requests_arr is not None):
            failed_requests_arr.append(to_append)

    def get_ugoira_metadata(self, illust_id: str, failed_api_requests: Optional[list] = None) -> dict:
        """Get the metadata of an ugoira (うごくイラスト).

        Args:
            illust_id (str):
                The illust ID that had the ugoira.
            failed_api_requests (list, optional):
                Array to append failed API requests to. Defaults to None.

        Returns:
            dict:
                The metadata of the ugoira.
        """
        url = self.__URL + "/v1/ugoira/metadata"
        with httpx.Client(http2=True, headers=self.get_headers(referer=self.__URL), timeout=self.api_timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    r = client.get(url, params={"illust_id": illust_id})
                    self.refresh_oauth_token(r, raise_error=True)
                    r.raise_for_status()
                    r = r.json()
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError):
                    if (retry_counter == C.MAX_RETRIES):
                        self.__append_to_failed_requests_arr(
                            failed_requests_arr=failed_api_requests,
                            to_append=illust_id
                        )
                        return
                    time.sleep(C.RETRY_DELAY)
                except (PixivOAuthRefreshError, PixivOAuthRefreshedError) as e:
                    if (isinstance(e, PixivOAuthRefreshedError) and retry_counter != C.MAX_RETRIES):
                        client.headers = self.get_headers(referer=self.__URL)
                        continue

                    self.__append_to_failed_requests_arr(
                        failed_requests_arr=failed_api_requests,
                        to_append=illust_id
                    )
                    return
                else:
                    break

        return r["ugoira_metadata"]

    async def download_ugoira_zip(self, ugoira_url: str, illust_id: str, download_path: pathlib.Path, 
                                  failed_downloads_arr: Optional[list] = None) -> None:
        """Download the ugoira zip file.

        Args:
            ugoira_url (str):
                The URL of the ugoira zip file.
            illust_id (str):
                The illust ID that had the ugoira.
            download_path (pathlib.Path):
                The path to download the ugoira zip file to.
            failed_downloads_arr (list, optional):
                Array to append failed downloads to. Defaults to None.

        Returns:
            None
        """
        if (await async_file_exists(download_path)):
            return

        await async_mkdir(download_path.parent, parents=True, exist_ok=True)
        async with httpx.AsyncClient(http2=True, headers=self.get_headers(referer=self.__URL), timeout=self.download_timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    async with client.stream("GET", ugoira_url) as r:
                        self.refresh_oauth_token(r, raise_error=True)
                        r.raise_for_status()
                        async with aiofiles.open(download_path, "wb") as f:
                            async for chunk in r.aiter_bytes(chunk_size=C.CHUNK_SIZE):
                                await f.write(chunk)
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, httpx.StreamError):
                    if (retry_counter == C.MAX_RETRIES):
                        self.__append_to_failed_requests_arr(
                            failed_requests_arr=failed_downloads_arr,
                            to_append=(illust_id, download_path.parent)
                        )
                        return
                    time.sleep(C.RETRY_DELAY)
                except (PixivOAuthRefreshError, PixivOAuthRefreshedError) as e:
                    if (isinstance(e, PixivOAuthRefreshedError) and retry_counter != C.MAX_RETRIES):
                        client.headers = self.get_headers(referer=self.__URL)
                        continue

                    self.__append_to_failed_requests_arr(
                        failed_requests_arr=failed_downloads_arr,
                        to_append=(illust_id, download_path.parent)
                    )
                    return
                except (asyncio.CancelledError):
                    await async_remove_file(download_path)
                    raise
                else:
                    break

    def convert_zip_to_gif(self, zipfile_path: pathlib.Path, frames: dict[str, int], delete_zip: Optional[bool] = False) -> None:
        """Convert the ugoira zip file to a gif.

        Note that this function can take some time to complete.
        Credits: 
            https://github.com/item4/ugoira
            https://stackoverflow.com/a/57751793/16377492

        Args:
            zipfile_path (pathlib.Path):
                The path to the ugoira zip file.
            frames (dict[str, int]):
                The frames information of the ugoira. ({"file_name": delay})
            delete_zip (bool, optional):
                Whether to delete the zip file after converting it to a gif. Defaults to False.

        Returns:
            None
        """
        gif_path = zipfile_path.with_suffix(".gif")
        if (gif_path.exists() and gif_path.is_file()):
            return

        extracted_image_path = zipfile_path.parent.joinpath("extracted_image")
        with zipfile.ZipFile(zipfile_path) as z:
            z.extractall(extracted_image_path)

        durations: list[int] = []
        sorted_files = tuple(
            sorted(extracted_image_path.iterdir(), key=lambda x: int(x.stem))
        )
        # Using generator for memory efficiency
        # Tested: Went from 700MB to 100MB in memory usage
        images = (Image.open(file) for file in sorted_files)
        for image_path in sorted_files:
            durations.append(frames[image_path.name])

        first_img = next(images)
        first_img.save(
            gif_path,
            format="GIF",
            save_all=True,
            append_images=images,
            duration=durations,
            loop=0,
            optimize=False,
            quality=100,
        )

        shutil.rmtree(extracted_image_path)
        if (delete_zip):
            zipfile_path.unlink()

    async def download_illust(self, illust_url: str, illust_id: str, download_path: pathlib.Path,
                              failed_downloads_arr: Optional[list] = None) -> None:
        """Download the illustration.

        Args:
            illust_url (str):
                The URL of the illustration.
            illust_id (str):
                The illust ID that had the illustration.
            download_path (pathlib.Path):
                The path to download the illustration to.
            failed_downloads_arr (list, optional):
                Array to append failed downloads to. Defaults to None.

        Returns:
            None
        """
        if (await async_file_exists(download_path)):
            return

        await async_mkdir(download_path.parent, parents=True, exist_ok=True)
        async with httpx.AsyncClient(http2=True, headers=self.get_headers(referer=self.get_illust_url(illust_id)), timeout=self.download_timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    async with client.stream("GET", illust_url) as r:
                        self.refresh_oauth_token(r, raise_error=True)
                        r.raise_for_status()
                        async with aiofiles.open(download_path, "wb") as f:
                            async for chunk in r.aiter_bytes(chunk_size=None):
                                await f.write(chunk)
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, httpx.StreamError):
                    if (retry_counter == C.MAX_RETRIES):
                        self.__append_to_failed_requests_arr(
                            failed_requests_arr=failed_downloads_arr,
                            to_append=(illust_id, download_path.parent)
                        )
                        return
                    time.sleep(C.RETRY_DELAY)
                except (PixivOAuthRefreshError, PixivOAuthRefreshedError) as e:
                    if (isinstance(e, PixivOAuthRefreshedError) and retry_counter != C.MAX_RETRIES):
                        client.headers = self.get_headers(referer=self.get_illust_url(illust_id))
                        continue

                    self.__append_to_failed_requests_arr(
                        failed_requests_arr=failed_downloads_arr,
                        to_append=(illust_id, download_path.parent)
                    )
                    return
                except (asyncio.CancelledError):
                    await async_remove_file(download_path)
                    raise
                else:
                    break

    def convert_page_num_to_offset(self, min_page_num: int, max_page_num: int) -> tuple[int, int]:
        """Convert the page number to the offset as 
        one page will have 30 illustrations instead of the usual 60.

        Note that if the offset is more than 5000, it will be set to 5000 because 
        Pixiv's API will return a 400 status response as it only allows a maximum offset of 5000.

        Args:
            min_page_num (int):
                The minimum page number.
            max_page_num (int):
                The maximum page number.

        Returns:
            tuple[int, int]:
                The minimum and maximum offset.
        """
        if (min_page_num < 0 or max_page_num < 0):
            raise ValueError("Page numbers must be positive integers.")

        if (min_page_num > max_page_num):
            min_page_num, max_page_num = max_page_num, min_page_num

        min_offset, max_offset = (60 * (min_page_num - 1), 60 * (max_page_num - min_page_num + 1))
        if (min_offset > 5000):
            min_offset = 5000
        if (max_offset > 5000):
            max_offset = 5000
        return (min_offset, max_offset)

    def get_illust_details(self, illust_id: str, failed_api_requests: Optional[list] = None) -> dict:
        """Get the details of the illustration.

        Args:
            illust_id (str):
                The illust ID to get the details of.
            failed_api_requests (list, optional):
                Array to append failed API requests to. Defaults to None.

        Returns:
            dict:
                The details of the illustration.
        """
        url = self.__URL + "/v1/illust/detail"
        with httpx.Client(http2=True, headers=self.get_headers(), timeout=self.api_timeout) as client:
            for retry_counter in range(1, C.MAX_RETRIES + 1):
                try:
                    r = client.get(url, params={"illust_id": illust_id})
                    self.refresh_oauth_token(r, raise_error=True)
                    if (r.status_code == 404):
                        return

                    r.raise_for_status()
                    r = r.json()
                except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError):
                    if (retry_counter == C.MAX_RETRIES):
                        self.__append_to_failed_requests_arr(
                            failed_requests_arr=failed_api_requests,
                            to_append=illust_id
                        )
                        return
                    time.sleep(C.RETRY_DELAY)
                except (PixivOAuthRefreshError, PixivOAuthRefreshedError) as e:
                    if (isinstance(e, PixivOAuthRefreshedError) and retry_counter != C.MAX_RETRIES):
                        client.headers = self.get_headers()
                        continue

                    self.__append_to_failed_requests_arr(
                        failed_requests_arr=failed_api_requests,
                        to_append=illust_id
                    )
                    return
                else:
                    break

        return r["illust"]

    def get_illustrator_illusts(self, user_id: str, min_page_num: int, 
                                max_page_num: int, failed_api_requests: Optional[list] = None) -> list[dict]:
        """Get the illustrations of the illustrator.

        Args:
            user_id (str):
                The user ID of the illustrator.
            min_page_num (int):
                The minimum page number to get the illustrations from.
            max_page_num (int):
                The maximum page number to get the illustrations from.
            failed_api_requests (list, optional):
                Array to append failed API requests to. Defaults to None.

        Returns:
            list[dict]:
                The illustrations of the illustrator.
        """
        illusts: list[dict] = []
        next_url = self.__URL + "/v1/user/illusts"
        min_offset, max_offset = self.convert_page_num_to_offset(
            min_page_num=min_page_num, 
            max_page_num=max_page_num
        )
        params = {
            "user_id": user_id,
            "type": "illust",
            "filter": "for_ios",
            "offset": min_offset
        }
        with httpx.Client(http2=True, headers=self.get_headers(), timeout=self.api_timeout) as client:
            while (next_url is not None and params["offset"] != max_offset):
                for retry_counter in range(1, C.MAX_RETRIES + 1):
                    try:
                        r = client.get(next_url, params=params)
                        self.refresh_oauth_token(r, raise_error=True)
                        r.raise_for_status()
                        r = r.json()
                        params["offset"] += 30
                    except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError):
                        if (retry_counter == C.MAX_RETRIES):
                            self.__append_to_failed_requests_arr(
                                failed_requests_arr=failed_api_requests,
                                to_append=user_id
                            )
                            return
                        time.sleep(C.RETRY_DELAY)
                    except (PixivOAuthRefreshError, PixivOAuthRefreshedError) as e:
                        if (isinstance(e, PixivOAuthRefreshedError) and retry_counter != C.MAX_RETRIES):
                            client.headers = self.get_headers()
                            continue

                        self.__append_to_failed_requests_arr(
                            failed_requests_arr=failed_api_requests,
                            to_append=user_id
                        )
                        return
                    else:
                        break

                illusts.extend(r["illusts"])
                next_url = r.get("next_url")
                self.__sleep_after_request()

        return illusts

    def get_tag_illusts(self, tag_name: str, min_page_num: int, 
                        max_page_num: int, failed_api_requests, strict: bool, sort_order: str) -> dict:
        """Get the illustrations of a tag name.

        Args:
            tag_name (str):
                The tag name to get the illustrations of.
            min_page_num (int):
                The minimum page number to get the illustrations from.
            max_page_num (int):
                The maximum page number to get the illustrations from.
            failed_api_requests (list):
                Array to append failed API requests to.
            strict (bool):
                Whether to match all illustration strictly with the tag name.
                If set to False, it will match all illustrations that contain the tag name.
            sort_order (str):
                The sort order of the illustrations.
                ("date_desc", "date_asc", "popular_desc")

        Returns:
            dict:
                The illustrations of the tag name.
        """
        if (sort_order not in ("date_desc", "date_asc", "popular_desc")):
            raise ValueError("Invalid sort order")

        illusts: list[dict] = []
        next_url = self.__URL + "/v1/search/illust"
        min_offset, max_offset = self.convert_page_num_to_offset(
            min_page_num=min_page_num, 
            max_page_num=max_page_num
        )
        params = {
            "word": 
                tag_name,
            "search_target": 
                "exact_match_for_tags" if (strict) else "partial_match_for_tags",
            "filter": 
                "for_ios",
            "offset": 
                min_offset,
            "sort":
                sort_order
        }
        with httpx.Client(http2=True, headers=self.get_headers(), timeout=self.api_timeout) as client:
            while (next_url is not None and params["offset"] != max_offset):
                for retry_counter in range(1, C.MAX_RETRIES + 1):
                    try:
                        r = client.get(next_url, params=params)
                        self.refresh_oauth_token(r, raise_error=True)
                        r.raise_for_status()
                        r = r.json()
                        min_offset += 30
                        params["offset"] += 30
                    except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.JSONDecodeError):
                        if (retry_counter == C.MAX_RETRIES):
                            self.__append_to_failed_requests_arr(
                                failed_requests_arr=failed_api_requests,
                                to_append=tag_name
                            )
                            return
                        time.sleep(C.RETRY_DELAY)
                    except (PixivOAuthRefreshError, PixivOAuthRefreshedError) as e:
                        if (isinstance(e, PixivOAuthRefreshedError) and retry_counter != C.MAX_RETRIES):
                            client.headers = self.get_headers()
                            continue

                        self.__append_to_failed_requests_arr(
                            failed_requests_arr=failed_api_requests,
                            to_append=tag_name
                        )
                        return
                    else:
                        break

                illusts.extend(r["illusts"])
                next_url = r.get("next_url")
                self.__sleep_after_request()

        return illusts

    @staticmethod
    def __sleep_after_request():
        """Slow down the requests to prevent rate limiting 
        and to avoid being blocked by Cloudflare."""
        return time.sleep(random.uniform(0.8, 2))

    async def download_multiple_illust(
        self, base_folder_path: Union[pathlib.Path, str], 
        convert_ugoira: bool,
        illust_id_arr: Optional[list[str]] = None, 
        user_id_arr: Optional[list[tuple[str, int, int]]] = None, 
        tag_name_arr: Optional[list[tuple[str, int, int]]] = None) -> None:
        """Not using async for Pixiv's API calls as the API is strict on rate limiting 
        and it is protected by Cloudflare but uses async when downloading content from Pixiv's servers.

        Args:
            base_folder_path (pathlib.Path | str):
                The user's default download folder path.
            convert_ugoira (bool):
                Whether to convert ugoira to gif.
            illust_id_arr (list[str], optional):
                Array of illustration IDs to download. Defaults to None.
            user_id_arr (list[tuple[str, int, int]], optional):
                Array of tuples of user IDs to download the 
                illustrations of with the minimum and maximum page numbers. Defaults to None.
            tag_name_arr (list[tuple[str, int, int]], optional):
                Array of tuples of tag names to download the 
                illustrations of with the minimum and maximum page numbers. Defaults to None.

        Returns:
            None
        """
        illust_json_arr = []
        failed_api_requests: list[str] = []
        download_illust_id, download_user_illust, download_tag_name = False, False, False
        if (illust_id_arr):
            for illust_id in illust_id_arr:
                illust_json = self.get_illust_details(illust_id, failed_api_requests)
                self.__sleep_after_request()
                if (illust_json is not None):
                    illust_json_arr.append(illust_json)
            download_illust_id = True
        elif (user_id_arr):
            for user_id, min_page_num, max_page_num in user_id_arr:
                user_illusts = self.get_illustrator_illusts(
                    user_id=user_id, 
                    min_page_num=min_page_num,
                    max_page_num=max_page_num,
                    failed_api_requests=failed_api_requests,
                )
                if (user_illusts is not None):
                    illust_json_arr.extend(user_illusts)
            download_user_illust = True
        elif (tag_name_arr):
            for tag_name, min_page_num, max_page_num, sort_order in tag_name_arr:
                tag_illusts = self.get_tag_illusts(
                    tag_name=tag_name, 
                    min_page_num=min_page_num,
                    max_page_num=max_page_num,
                    failed_api_requests=failed_api_requests,
                    strict=True,
                    sort_order=sort_order
                )
                if (tag_illusts is not None):
                    illust_json_arr.extend(tag_illusts)
            download_tag_name = True
        else:
            return # nothing to download

        if (len(illust_json_arr) == 0):
            print_danger("No illustrations to download.")
            return

        if (isinstance(base_folder_path, str)):
            base_folder_path = pathlib.Path(base_folder_path)

        # parse the JSON responses
        spinner_base_msg = "Processed {progress} out of " + f"{len(illust_json_arr)} JSON responses"
        with Spinner(
            message=spinner_base_msg.format(
                progress=0
            ),
            colour="light_yellow",
            spinner_position="left",
            spinner_type="pong",
            completion_msg=f"Processed {len(illust_json_arr)} JSON responses from Pixiv's API!\n",
            cancelled_msg="Cancelled processing JSON responses from Pixiv's API!\n",
        ) as spinner:
            base_folder_path = base_folder_path.joinpath("Pixiv")
            ugoira_urls: list[tuple[str, dict, dict[str, int], pathlib.Path]] = []
            illust_urls: list[tuple[str, str, pathlib.Path]] = []
            for i, illust_json in enumerate(illust_json_arr):
                spinner.message = spinner_base_msg.format(
                    progress=i + 1
                )
                illust_id = illust_json["id"]
                illust_title = remove_illegal_chars_in_path(
                    string=illust_json["title"]
                )
                illustrator_name = remove_illegal_chars_in_path(
                    string=illust_json["user"]["name"]
                )
                illust_folder = base_folder_path.joinpath(
                    illustrator_name, 
                    f"[{illust_id}] {illust_title}"
                ).resolve()

                illust_type = illust_json["type"]
                if (illust_type == "ugoira"): # animated images which will require a separate API call
                    ugoira_json = self.get_ugoira_metadata(illust_id, failed_api_requests)
                    self.__sleep_after_request()
                    ugoira_url: str = ugoira_json["zip_urls"]["medium"]
                    if ("600x600" in ugoira_url): # since the API will only return the 600x600 URL
                        ugoira_url = ugoira_url.replace("600x600", "1920x1080", 1)
                    frames_info = {frame["file"]: frame["delay"] for frame in ugoira_json["frames"]}
                    ugoira_urls.append(
                        (illust_id, ugoira_url, frames_info, illust_folder)
                    )
                    continue

                # If the post only has one image,
                illust_url = illust_json.get("meta_single_page")
                if (illust_url is not None and illust_url):
                    illust_urls.append((illust_id, illust_url["original_image_url"], illust_folder))
                    continue

                # For posts with multiple images,
                for illust_url in illust_json.get("meta_pages", []):
                    illust_urls.append((illust_id, illust_url["image_urls"]["original"], illust_folder))

            log_filename = "failed_pixiv_api_calls.log"
            for id_request in failed_api_requests:
                if (download_illust_id):
                    log_critical_details_for_post(
                        post_folder=base_folder_path,
                        message=f"Failed to download {self.get_illust_url(id_request)}.\n",
                        log_filename=log_filename,
                    )
                elif (download_user_illust):
                    log_critical_details_for_post(
                        post_folder=base_folder_path,
                        message=f"Failed to download https://www.pixiv.net/en/users/{id_request}.\n",
                        log_filename=log_filename,
                    )
                elif (download_tag_name):
                    log_critical_details_for_post(
                        post_folder=base_folder_path,
                        message=f"Failed to download https://www.pixiv.net/en/tags/{id_request}/artworks.\n",
                        log_filename=log_filename,
                    )
                else:
                    raise ValueError("Invalid download type in Pixiv API when logging failed API requests.")

        # start the download process
        total_to_download = len(ugoira_urls) + len(illust_urls)
        if (total_to_download > 0):
            spinner_base_msg = "Downloaded {progress} out of " + f"{total_to_download} Pixiv URL(s)..."
            with Spinner(
                message=spinner_base_msg.format(
                    progress=0
                ),
                colour="light_yellow",
                spinner_position="left",
                spinner_type="material",
                completion_msg=f"Finished downloading all {total_to_download} Pixiv URL(s)!\n",
                cancelled_msg="Stopped downloading Pixiv URL(s) as per user's request...\n",
            ) as spinner:
                download_tasks = set()
                finished_download = 0
                failed_download_arr: list[tuple[str, pathlib.Path]] = []
                for illust_id, illust_url, illust_folder in illust_urls:
                    if (len(download_tasks) >= self.max_concurrent_downloads):
                        finished_task, download_tasks = await check_download_tasks(
                            download_tasks,
                            all_completed=False
                        )
                        finished_download += len(finished_task)
                        spinner.message = spinner_base_msg.format(
                            progress=finished_download
                        )

                    file_path = illust_folder.joinpath(
                        illust_url.rsplit(sep="/", maxsplit=1)[1]
                    ).resolve()
                    download_tasks.add(
                        asyncio.create_task(
                            self.download_illust(
                                illust_id=illust_id,
                                illust_url=illust_url,
                                download_path=file_path,
                                failed_downloads_arr=failed_download_arr,
                            )
                        )
                    )

                for illust_id, ugoira_url, _, illust_folder in ugoira_urls:
                    if (len(download_tasks) >= self.max_concurrent_downloads):
                        finished_task, download_tasks = await check_download_tasks(
                            download_tasks,
                            all_completed=False
                        )
                        finished_download += len(finished_task)
                        spinner.message = spinner_base_msg.format(
                            progress=finished_download
                        )

                    file_path = illust_folder.joinpath(
                        ugoira_url.rsplit(sep="/", maxsplit=1)[1]
                    ).resolve()
                    download_tasks.add(
                        asyncio.create_task(
                            self.download_ugoira_zip(
                                illust_id=illust_id,
                                ugoira_url=ugoira_url,
                                download_path=file_path,
                                failed_downloads_arr=failed_download_arr,
                            )
                        )
                    )

                finished_task, _ = await check_download_tasks(
                    download_tasks,
                    all_completed=True
                )

                for illust_id, folder_path in failed_download_arr:
                    log_critical_details_for_post(
                        post_folder=folder_path,
                        message=f"Failed to download https://www.pixiv.net/en/artworks/{illust_id}.\n",
                        log_filename="failed_pixiv_downloads.log",
                    )

        # Ugoira conversion to be done synchronously
        # as it can use up a lot of memory (100MB+)
        total_ugoira_to_convert = len(ugoira_urls)
        if (total_ugoira_to_convert > 0 and convert_ugoira):
            spinner_base_msg = "Converted {progress} " + f"out of {total_ugoira_to_convert} Pixiv ugoira(s) to gifs..."
            with Spinner(
                message=spinner_base_msg.format(
                    progress=0    
                ),
                colour="light_yellow",
                spinner_position="left",
                spinner_type="aesthetic",
                completion_msg=f"Finished converting all {total_ugoira_to_convert} Pixiv ugoira(s) to gifs!\n",
                cancelled_msg="Stopped converting Pixiv ugoira(s) as per user's request...\n",
            ) as spinner:
                for i, ugoira_info in enumerate(ugoira_urls):
                    _, ugoira_url, frames_info, illust_folder = ugoira_info
                    self.convert_zip_to_gif(
                        frames=frames_info,
                        zipfile_path=illust_folder.joinpath(
                            ugoira_url.rsplit(sep="/", maxsplit=1)[1]
                        ).resolve(),
                    )
                    spinner.message = spinner_base_msg.format(
                        progress=i + 1
                    )

def get_pixiv_api() -> Union[PixivAPI, None]:
    """Get the Pixiv API instance if possible."""
    pixiv_refresh_token = load_pixiv_refresh_token()
    if (pixiv_refresh_token is not None):
        try:
            return PixivAPI(refresh_token=pixiv_refresh_token)
        except (PixivOAuthRefreshError):
            C.PIXIV_REFRESH_TOKEN_PATH.unlink(missing_ok=True)

# test codes
if (__name__ == "__main__"):
    PixivAPI().start_oauth_flow()