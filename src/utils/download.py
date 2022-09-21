# import Python's standard libraries
import json
import pathlib
import asyncio
from typing import Union, Optional

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from google_client import GoogleDrive
    from functional import async_remove_file, async_file_exists
else:
    from .constants import CONSTANTS as C
    from .google_client import GoogleDrive
    from .functional import async_remove_file, async_file_exists

# import third-party libraries
import httpx
from http.cookiejar import Cookie, CookieJar

import aiofiles
import aiofiles.os as aiofiles_os

def log_critical_details_for_post(post_folder: pathlib.Path, message: str, 
                                  log_filename: Optional[str] = "read_me.log") -> None:
    """Log critical details about a post to a log file.

    Args:
        post_folder (pathlib.Path):
            The path to the post's folder.
        message (str):
            The message to log.
        log_filename (Optional[str], optional):
            The name of the log file. Defaults to "read_me.log".
    """
    log_file = post_folder.joinpath(log_filename)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message)
        f.write("\n")

def log_failed_downloads(url_info: tuple[str, str], website: str, folder_path: pathlib.Path) -> None:
    """Log failed downloads to a log file.

    Args:
        url_info (tuple[str, str]):
            The url and its type of content.
        website (str):
            The website the url belongs to.
        folder_path (pathlib.Path):
            The path to the folder where the images will be downloaded.

    Returns:
        None
    """
    with open(folder_path.joinpath("failed_downloads.log"), "a") as f:
        url, content_type = url_info
        if (website == "fantia"):
            if (content_type == C.IMAGE_FILE):
                image_id = url.rsplit(sep="/", maxsplit=2)[1]

                # get post id from folder name, f"[{post_id}] {post_title}"
                post_id = folder_path.name.split(sep="]", maxsplit=1)[0].replace("[", "")
                f.write(f"https://fantia.jp/posts/{post_id}/post_content_photo/{image_id}\n")
                return

            f.write(url + "\n")
        elif (website == "pixiv_fanbox"):
            f.write(url + "\n")
        else:
            raise ValueError(f"Invalid website: {website}")

        f.write("\n")

async def async_download_file(url_info: tuple[str, str], folder_path: pathlib.Path, website: str, failed_downloads_arr: list, cookie: Optional[CookieJar] = None) -> None:
    """Download a file asynchronously from the given url.

    Args:
        url (tuple[str, str]):
            The url of the file to download and its content type
        folder_path (pathlib.Path):
            The folder path to the file to download.
        website (str):
            The website the url belongs to.
        failed_downloads_arr (list):
            The array to append failed downloads to.
        cookie (CookieJar, Optional):
            The cookie to use for the request, if any.

    Returns:
        None
    """
    url, content_type = url_info
    follow_redirects = (content_type == C.ATTACHMENT_FILE)

    if (follow_redirects):
        folder_path = folder_path.joinpath("attachments")
    elif (content_type == C.IMAGE_FILE):
        folder_path = folder_path.joinpath("images")
    await aiofiles_os.makedirs(folder_path, exist_ok=True)

    file_path = None
    async with httpx.AsyncClient(
        headers=C.BASE_REQ_HEADERS, 
        http2=True, 
        timeout=60, 
        follow_redirects=follow_redirects,
        cookies=cookie
    ) as client:
        for retry_counter in range(1, C.MAX_RETRIES + 1):
            try:
                async with client.stream(method="GET", url=url) as response:
                    response.raise_for_status()

                    file_path = folder_path.joinpath(
                        response.url.path.rsplit(sep="/", maxsplit=1)[1]
                    )
                    if (await async_file_exists(file_path)):
                        return

                    async with aiofiles.open(file_path, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=C.CHUNK_SIZE):
                            await f.write(chunk)
            except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, httpx.StreamError):
                await async_remove_file(file_path)
                if (retry_counter == C.MAX_RETRIES):
                    failed_downloads_arr.append(
                        (url_info, website, folder_path)
                    )
                    return
                await asyncio.sleep(C.RETRY_DELAY)
            except (asyncio.CancelledError):
                if (file_path is not None):
                    await async_remove_file(file_path)
                raise
            else:
                break

def format_cookie_to_cookiejar(cookie:  Union[dict, CookieJar, None]) -> Union[CookieJar, None]:
    """Format a cookie string to a CookieJar object for httpx requests.

    Args:
        cookie (dict | CookieJar | None):
            The cookie to convert to a CookieJar object.

    Returns:
        CookieJar | None:
            The CookieJar object of the cookie or None if the cookie is None.
    """
    if (cookie is None or isinstance(cookie, CookieJar)):
        return cookie

    cookie_rest_arg_dict = {}
    for key in cookie.keys():
        if (key.lower() in ("httponly", "samesite")):
            cookie_rest_arg_dict[key] = cookie[key]

    cookie_jar = CookieJar()
    cookie = Cookie(
        version=0,
        name=cookie["name"],
        value=cookie["value"],
        port=None,
        port_specified=False,
        domain=cookie["domain"],
        domain_specified=True,
        domain_initial_dot=cookie["domain"].startswith("."),
        path=cookie["path"],
        path_specified=True,
        secure=cookie["secure"],
        expires=cookie["expiry"],
        discard=True,
        comment=None,
        comment_url=None,
        rest=cookie_rest_arg_dict,
        rfc2109=False
    )
    cookie_jar.set_cookie(cookie)
    return cookie_jar

def create_post_folder(download_path: pathlib.Path, 
                       creator_name: str, post_id: str, post_title: str) -> pathlib.Path:
    """Create a folder for the post and returns the created post's folder path.

    Args:
        download_path (pathlib.Path):
            The path to the folder where the post folder will be created.
        creator_name (str):
            The name of the creator.
        post_id (str):
            The ID of the post.
        post_title (str):
            The title of the post.

    Returns:
        pathlib.Path:
            The path to the post folder.
    """
    # replace invalid characters in the post title with a dash
    post_title = C.ILLEGAL_PATH_CHARS_REGEX.sub(repl="-", string=post_title)

    # construct the post folder path
    post_folder_path = download_path.joinpath(creator_name, f"[{post_id}] {post_title}")
    post_folder_path.mkdir(parents=True, exist_ok=True)
    return post_folder_path

def log_failed_post_api_call(download_path: pathlib.Path, post_url: str) -> None:
    """Log a failed post API call to a log file.

    Args:
        download_path (pathlib.Path):
            The path to the folder where the log file will be created.
        post_url (str):
            The url of the post that failed to be downloaded.

    Returns:
        None
    """
    log_critical_details_for_post(
        post_folder=download_path,
        message="Failed to get the details of " \
                f"'{post_url}' after {C.MAX_RETRIES} requests.\n",
        log_filename="download_failures.log"
    )

async def get_post_details(download_path: pathlib.Path, website: str, post_id: str, post_url: str, json_arr: list, cookie: Optional[CookieJar] = None) -> None:
    """Get the details of a post using the respective API of the given website.

    Args:
        download_path (pathlib.Path):
            The path to the folder where the post will be downloaded (used for logging failed API requests).
        website (str):
            The website the post belongs to.
        post_id (str):
            The post ID of the post to download.
        post_url (str):
            The post URL to add to the request header as Referer and for logging failed API requests.
        json_arr (list):
            The array to append the JSON response to.
        cookie (CookieJar, Optional):
            The user's cookie to use to get access to the paywall-restricted post contents.

    Returns:
        The JSON response of the post details.
    """
    if (website == "fantia"):
        headers = C.BASE_REQ_HEADERS.copy()
        api_url = C.FANTIA_API_URL
        main_json = "post"
    elif (website == "pixiv_fanbox"):
        headers = C.PIXIV_FANBOX_API_HEADERS.copy()
        api_url = C.PIXIV_FANBOX_API_URL
        main_json = "body"
    else:
        raise ValueError(f"Invalid website: {website}")

    headers["Referer"] = post_url
    async with httpx.AsyncClient(http2=True, cookies=cookie, timeout=30, headers=headers) as client:
        for retry_counter in range(1, C.MAX_RETRIES + 1):
            try:
                response = await client.get(api_url + post_id)
                if (response.status_code == 404):
                    log_failed_post_api_call(
                        download_path=download_path, 
                        post_url=post_url
                    )
                    return

                response.raise_for_status()
                json_response = response.json()
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError, json.decoder.JSONDecodeError):
                if (retry_counter == C.MAX_RETRIES):
                    log_failed_post_api_call(
                        download_path=download_path, 
                        post_url=post_url
                    )
                    return
                await asyncio.sleep(C.RETRY_DELAY)
            else:
                break

    json_arr.append(json_response.get(main_json))

def process_fantia_json(json_response: Union[dict, None], download_path: pathlib.Path, 
                        download_flags: tuple[bool, bool, bool]) -> Union[tuple[pathlib.Path, list[tuple[str, str]]], None]:
    """Process the json response from Fantia's API and get the post's content urls.

    Args:
        json_response (dict, None):
            The json response from Fantia's API.
        download_path (pathlib.Path):
            The path to the folder where the post will be downloaded.
        download_flags (tuple[bool, bool, bool]):
            A tuple of booleans that represent whether to download
            the post's images, thumbnail, and attachments such as videos.

    Returns:
        A tuple of the post's folder path and a list of tuples 
        that contains the post's content urls and its content type.
        Otherwise, None if the post is not found.
    """
    if (json_response is None):
        return

    download_images, download_thumbnail, \
        download_attachments = download_flags

    post_id: str = json_response["id"]
    post_title: str = json_response["title"]
    creator_name: str = json_response["fanclub"]["user"]["name"]
    post_folder_path = create_post_folder(
        download_path=download_path,
        creator_name=creator_name,
        post_id=post_id,
        post_title=post_title
    )

    urls_to_download_arr = []
    if (download_thumbnail):
        thumbnail: Union[str, None] = json_response.get("thumb")
        if (thumbnail is not None):
            urls_to_download_arr.append((thumbnail["original"], C.THUMBNAIL_IMAGE))

    if (download_images or download_attachments):
        post_contents: list[dict] = json_response.get("post_contents", [])
        for post_content in post_contents:
            if (download_images):
                post_images: dict = post_content.get("post_content_photos", {})
                for post_image in post_images:
                    image_url = post_image["url"]["original"]
                    urls_to_download_arr.append((image_url, C.IMAGE_FILE))

            if (download_attachments):
                attachment_url: Union[str, None] = post_content.get("download_uri")
                if (attachment_url is not None):
                    attachment_url = "https://fantia.jp" + attachment_url
                    urls_to_download_arr.append((attachment_url, C.ATTACHMENT_FILE))

    return (post_folder_path, urls_to_download_arr)

def detect_password_in_text(post_folder_path: pathlib.Path, text: str) -> bool:
    """Detect if the given text contains a password and logs it to the post's folder.

    Args:
        post_folder_path (pathlib.Path):
            The path to the folder where the password will be logged.
        text (str):
            The text to check for a password.

    Returns:
        Bool: True if the text contains a password, otherwise False.
    """
    password_filename = "detected_passwords.txt"
    password_text_path = post_folder_path.joinpath(password_filename)
    if (password_text_path.exists() and password_text_path.is_file() and password_text_path.stat().st_size > 0):
        return False

    for password_text in C.PASSWORD_TEXTS:
        if (password_text in text):
            log_critical_details_for_post(
                post_folder=post_folder_path,
                message="Detected a possible password-protected " \
                        f"content in the post: {text}\n",
                log_filename=password_filename
            )
            return True
    return False

def detect_gdrive_links(text: str, is_url: bool, urls_to_download_arr: list[str]) -> bool:
    """Detect if the given text contains a Google Drive link.

    Args:
        text (str):
            The text to check for a Google Drive link.
        is_url (bool):
            Whether the text is a URL or not.
        urls_to_download_arr (list[str]):
            The array of URLs to download to append the Google Drive link to.

    Returns:
        Bool: True if the text contains a Google Drive link, otherwise False.
    """
    DRIVE_LINK = "https://drive.google.com"
    if (is_url):
        if (text.startswith(DRIVE_LINK)):
            urls_to_download_arr.append((text, C.GDRIVE_FILE))
            return True
        return False

    if (DRIVE_LINK in text):
        urls_to_download_arr.append((text, C.GDRIVE_FILE))
        return True
    return False

def detect_other_external_download_links(text: str, is_url: bool, 
                                         post_folder_path: pathlib.Path) -> bool:
    """Detect if the given text contains a download link
    to an external website, other than GDrive, and logs it to the post's folder.

    Args:
        text (str):
            The text to check for an external link.
        is_url (bool):
            Whether the text is a URL or not.
        post_folder_path (pathlib.Path):
            The path to the folder where the external link will be logged.

    Returns:
        Bool: True if the text contains an external link, otherwise False.
    """
    filename = "detected_external_links.txt"
    text_path = post_folder_path.joinpath(filename)
    if (text_path.exists() and text_path.is_file() and text_path.stat().st_size > 0):
        return False

    for url in C.OTHER_FILE_HOSTING_PROVIDERS:
        if (url in text):
            if (is_url):
                message = "Detected a link that points to an external file hosting " \
                           f"provider in the post: {text}\n"
            else:
                message = "Detected a link that points to an external file hosting " \
                           f"provider in the post's description:\n{text}\n"

            log_critical_details_for_post(
                post_folder=post_folder_path,
                message=message,
                log_filename=filename
            )
            return True
    return False

def process_pixiv_fanbox_json(json_response: Union[dict, None], download_path: pathlib.Path, 
                              download_flags: tuple[bool, bool, bool, bool, bool]) -> Union[tuple[pathlib.Path, list[tuple[str, str]]], None]:
    """Get the details of a Pixiv Fanbox post using Pixiv Fanbox's API.

    Args:
        json_response (dict, None):
            The json response from Pixiv Fanbox's API.
        download_path (pathlib.Path):
            The path to the folder where the post will be downloaded.
        download_flags (tuple[bool, bool, bool, bool, bool]):
            A tuple of booleans that represent whether to download
            the post's images, thumbnail, attachments such as videos,
            gdrive files, and detect other external links such as MEGA links.

    Returns:
        A tuple of the post's folder path and a list of tuples 
        that contains the post's content urls and its content type.
        Otherwise, None if the post is not found.
    """
    if (json_response is None):
        return

    download_images, download_thumbnail, download_attachments, \
        download_gdrive_links, detect_other_download_links = download_flags

    post_id: str = json_response["id"]
    post_title: str = json_response["title"]
    creator_name: str = json_response["creatorId"]
    post_folder_path = create_post_folder(
        download_path=download_path,
        creator_name=creator_name,
        post_id=post_id,
        post_title=post_title
    )

    urls_to_download_arr = []
    if (download_thumbnail):
        thumbnail: str = json_response.get("coverImageUrl")
        if (thumbnail is not None):
            urls_to_download_arr.append((thumbnail, C.THUMBNAIL_IMAGE))

    # Note that Pixiv Fanbox posts have 3 types of formatting (as of now):
    #   1. With proper formatting and mapping of post content elements ("article")
    #   2. With a simple formatting that obly contains info about the text and files ("file", "image")
    post_type: str = json_response["type"]
    post_contents: dict = json_response["body"]

    # Retrieves the post's gdrive links or log external download links such as MEGA links, if any.
    # Will also detect if the post contains a password for the user to use.
    if (download_gdrive_links or detect_other_download_links):
        if (post_type in ("file", "image")):
            post_body: str = post_contents.get("text")
            if (post_body is not None):
                # If the post follow a simple format,
                post_body: list[str] = post_body.split()
                for idx, text in enumerate(post_body):
                    if (detect_password_in_text(post_folder_path, text)):
                        try:
                            log_critical_details_for_post(
                                post_folder=post_folder_path,
                                message="Note: If the password was not present in the text above,\n"\
                                        "the next block of text might contain the password:\n" \
                                        f"{post_body[idx + 1]}\n",
                                log_filename="detected_passwords.txt"
                            )
                        except (IndexError):
                            pass

                    if (detect_other_download_links):
                        detect_other_external_download_links(
                            text=text, 
                            is_url=False, 
                            post_folder_path=post_folder_path
                        )

                    if (download_gdrive_links):
                        detect_gdrive_links(
                            text=text,
                            is_url=False,
                            urls_to_download_arr=urls_to_download_arr
                        )

        elif (post_type == "article"):
            # If the post have proper formatting and mappings,
            article_content: list[dict] = post_contents.get("blocks", [])
            for idx, article_block in enumerate(article_content):
                text: str = article_block.get("text", "")
                if (text != ""):
                    if (download_gdrive_links):
                        detect_gdrive_links(
                            text=text,
                            is_url=False,
                            urls_to_download_arr=urls_to_download_arr
                        )

                    if (detect_other_download_links):
                        detect_other_external_download_links(
                            text=text, 
                            is_url=False, 
                            post_folder_path=post_folder_path
                        )

                    if (detect_password_in_text(post_folder_path, text)):
                        # Get the next 2 blocks of text
                        no_of_blocks = 0
                        try:
                            next_text = article_content[idx + 1].get("text", "")
                        except (IndexError):
                            next_text = ""
                        try:
                            next_next_text = article_content[idx + 2].get("text", "")
                        except (IndexError):
                            next_next_text = ""

                        # Increment the number of blocks if the next block of text is not empty
                        next_text_is_not_empty = (next_text != "")
                        if (next_text_is_not_empty):
                            no_of_blocks += 1
                        next_next_text_is_not_empty = (next_next_text != "")
                        if (next_next_text_is_not_empty):
                            no_of_blocks += 1

                        # log the obtained text
                        if (next_text_is_not_empty):
                            next_text += "\n"
                        if (next_text_is_not_empty or next_next_text_is_not_empty):
                            log_critical_details_for_post(
                                post_folder=post_folder_path,
                                message="Note: If the password was not present in the text above,\n"\
                                        f"the next {no_of_blocks} block of text might contain " \
                                        f"the password:\n{next_text}{next_next_text}\n",
                                log_filename="detected_passwords.txt"
                            )

                external_links_info_arr: list[dict] = article_block.get("links", [])
                for external_link_info in external_links_info_arr:
                    external_link: str = external_link_info.get("url")
                    if (external_link is None):
                        continue

                    if (download_gdrive_links):
                        detected_gdrive = detect_gdrive_links(
                            text=external_link,
                            is_url=True,
                            urls_to_download_arr=urls_to_download_arr
                        )
                        if (detected_gdrive):
                            continue

                    if (detect_other_download_links):
                        detect_other_external_download_links(
                            text=external_link, 
                            is_url=True, 
                            post_folder_path=post_folder_path
                        )

    # Get images and attachments URL(s) from the post
    if (post_type in ("file", "image") and (download_images or download_attachments)):
        # If the post follows a simple format,
        image_and_attachment_files: list[dict] = post_contents.get(f"{post_type}s", [])
        for file_info in image_and_attachment_files:
            file_url = file_info.get("url") or file_info.get("originalUrl")
            if (file_url is not None):
                if (download_images and file_info["extension"] in C.PIXIV_FANBOX_ALLOWED_IMAGE_FORMATS):
                    urls_to_download_arr.append((file_url, C.IMAGE_FILE))
                elif (download_attachments):
                    urls_to_download_arr.append((file_url, C.ATTACHMENT_FILE))

    elif (post_type == "article"):
        if (download_images):
            # If the post have proper formatting and mappings,
            image_files: dict[str, dict[str, Union[str, int]]] = post_contents.get("imageMap", {})
            for image_file in image_files.values():
                image_file_url: str = image_file["originalUrl"]
                urls_to_download_arr.append((image_file_url, C.IMAGE_FILE))

        if (download_attachments):
            # If the post have proper formatting and mappings,
            attachment_files: dict[str, dict[str, Union[str, int]]] = post_contents.get("fileMap", {})
            for attachments in attachment_files.values():
                attachment_url: str = attachments["url"]
                urls_to_download_arr.append((attachment_url, C.ATTACHMENT_FILE))

    return (post_folder_path, urls_to_download_arr)

async def get_gdrive_folder_contents(
    drive_service: GoogleDrive, 
    gdrive_folder_arr: C.GDRIVE_HINT_TYPING,
    failed_requests_arr: list, 
    headers: Optional[dict] = None) -> list[tuple[str, tuple[str, pathlib.Path]]]:
    """Get the folder contents of a Google Drive folder.

    Args:
        drive_service (GoogleDrive): 
            The Google Drive service object.
        gdrive_folder_arr (list[tuple[str, tuple[str, pathlib.Path]]]): 
            The Google Drive folder(s) to get the contents of.
        failed_requests_arr (list): 
            The array to append the failed requests to.
        headers (dict, optional): 
            The headers to use for the requests. Defaults to None.

    Returns:
        list[tuple[str, tuple[str, pathlib.Path]]]:
            A list of tuples containing the file ID(s) and
            a tuple of the original gdrive URL and the post folder that the gdrive URL was found in.
    """
    if (drive_service is None):
        return

    gdrive_folder_api_response = await asyncio.gather(*[
        drive_service.get_folder_contents(
            folder_id=folder_id,
            gdrive_info=gdrive_info,
            failed_requests_arr=failed_requests_arr,
            headers=headers
        )
        for folder_id, gdrive_info in gdrive_folder_arr
    ])

    nested_folders_arr = []
    gdrive_files_arr = []
    for response, gdrive_info in gdrive_folder_api_response:
        if (response is None):
            continue

        for file in response:
            to_append = (file["id"], file["name"], gdrive_info)
            if (file["mimeType"] == "application/vnd.google-apps.folder"):
                nested_folders_arr.append(to_append)
            else:
                gdrive_files_arr.append(to_append)

    if (len(nested_folders_arr) > 0):
        nested_files_arr = await get_gdrive_folder_contents(
            drive_service=drive_service,
            gdrive_folder_arr=nested_folders_arr,
            failed_requests_arr=failed_requests_arr,
            headers=headers
        )
        gdrive_files_arr.extend(nested_files_arr)

    return gdrive_files_arr