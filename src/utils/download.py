# import Python's standard libraries
import pathlib
import asyncio
from typing import Union, Optional

# import local files
if (__package__ is None or __package__ == ""):
    from crucial import install_dependency, __version__
    from errors import FailedToDownloadError
    from functional import print_danger
    from constants import CONSTANTS as C
else:
    from .crucial import install_dependency, __version__
    from .errors import FailedToDownloadError
    from .functional import print_danger
    from .constants import CONSTANTS as C

# import third-party libraries
import httpx
from http.cookiejar import Cookie, CookieJar

try:
    import aiofiles
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="aiofiles>=0.8.0")
    import aiofiles

try:
    import gdown
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="gdown>=4.4.0")
    import gdown

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

async def log_failed_downloads(url_info: tuple[str, str], website: str, folder_path: pathlib.Path) -> None:
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
    async with aiofiles.open(folder_path.joinpath("failed_downloads.log"), "a") as f:
        url, content_type = url_info
        if (website == "fantia"):
            if (content_type == C.IMAGE_FILE):
                image_id = url.rsplit(sep="/", maxsplit=2)[1]

                # get post id from folder name, f"[{post_id}] {post_title}"
                post_id = folder_path.name.split(sep="]", maxsplit=1)[0].replace("[", "")
                await f.write(f"https://fantia.jp/posts/{post_id}/post_content_photo/{image_id}\n")
                return

            await f.write(url + "\n")
        elif (website == "pixiv_fanbox"):
            await f.write(url + "\n")
        else:
            raise ValueError(f"Invalid website: {website}")

        await f.write("\n")

async def async_download_file(url_info: tuple[str, str], folder_path: pathlib.Path, website: str) -> None:
    """Download a file asynchronously from the given url.

    Args:
        url (tuple[str, str]):
            The url of the file to download and its content type
        folder_path (pathlib.Path):
            The folder path to the file to download.
        website (str):
            The website the url belongs to.

    Returns:
        None
    """
    retries = 0
    url, content_type = url_info
    follow_redirects = (content_type == C.ATTACHMENT_FILE)
    async with httpx.AsyncClient(
        headers=C.BASE_REQ_HEADERS, 
        http2=True, 
        timeout=60, 
        follow_redirects=follow_redirects
    ) as client:
        while (retries < C.MAX_RETRIES):
            try:
                async with client.stream(method="GET", url=url) as response:
                    if (response.status_code != 200):
                        raise FailedToDownloadError(f"Failed to download {url}")

                    file_path = folder_path.joinpath(
                        response.url.path.rsplit(sep="/", maxsplit=1)[1]
                    )
                    if (file_path.exists() and file_path.is_file()):
                        return

                    async with aiofiles.open(file_path, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=C.CHUNK_SIZE):
                            await f.write(chunk)
            except (
                httpx.RequestError,
                httpx.HTTPStatusError,
                httpx.HTTPError,
                httpx.StreamError,
                FailedToDownloadError
            ):
                retries += 1
                file_path.unlink(missing_ok=True)
                await asyncio.sleep(C.RETRY_DELAY)
            else:
                break
        else:
            await log_failed_downloads(
                url_info=url_info, 
                website=website,
                folder_path=folder_path
            )

def format_cookie_to_cookiejar(cookie: dict) -> CookieJar:
    """Format a cookie string to a CookieJar object for httpx requests.

    Args:
        cookie (dict):
            The cookie to convert to a CookieJar object.

    Returns:
        CookieJar:
            The CookieJar object of the cookie.
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
    post_folder_path = download_path.joinpath(creator_name, f"[{post_id}] {post_title}")
    post_folder_path.mkdir(parents=True, exist_ok=True)
    return post_folder_path

def get_fantia_post_details(cookie: dict, download_path: pathlib.Path, post_id: str, 
                            download_flags: tuple[bool, bool, bool]) -> Union[tuple[pathlib.Path, list[tuple[str, str]]], None]:
    """Get the details of a Fantia post using Fantia's API.

    Args:
        cookie (dict):
            The user's cookie to use to get access to the paywall-restricted post contents.
        download_path (pathlib.Path):
            The path to the folder where the post will be downloaded.
        post_id (str):
            The post ID of the post to download.
        download_flags (tuple[bool, bool, bool]):
            A tuple of booleans that represent whether to download
            the post's images, thumbnail, and attachments such as videos.

    Returns:
        A tuple of the post's folder path and a list of tuples 
        that contains the post's content urls and its content type.
        Otherwise, None if the post is not found.
    """
    download_images, download_thumbnail, \
        download_attachments = download_flags

    with httpx.Client(http2=True, cookies=format_cookie_to_cookiejar(cookie), timeout=15) as client:
        response = client.get(C.FANTIA_API_URL + post_id)
        post_info: dict = response.json().get("post")

    if (post_info is None):
        return

    post_title: str = post_info["title"]
    creator_name: str = post_info["fanclub"]["user"]["name"]
    post_folder_path = create_post_folder(
        download_path=download_path,
        creator_name=creator_name,
        post_id=post_id,
        post_title=post_title
    )

    urls_to_download_arr = []
    if (download_thumbnail):
        thumbnail: Union[str, None] = post_info.get("thumb")
        if (thumbnail is not None):
            urls_to_download_arr.append((thumbnail["original"], C.THUMBNAIL_IMAGE))

    if (download_images or download_attachments):
        post_contents: list[dict] = post_info.get("post_contents", [])
        for post_content in post_contents:
            if (download_images):
                post_images: Union[dict, None] = post_content.get("post_content_photos")
                if (post_images is not None):
                    for post_image in post_images:
                        image_url = post_image["url"]["original"]
                        urls_to_download_arr.append((image_url, C.IMAGE_FILE))

            if (download_attachments):
                attachment_url: str = post_content.get("download_uri")
                if (attachment_url is not None):
                    attachment_url = "https://fantia.jp" + attachment_url
                    urls_to_download_arr.append((attachment_url, C.ATTACHMENT_FILE))

    return (post_folder_path, urls_to_download_arr)

def get_pixiv_fanbox_post_details(
    cookie: dict, 
    download_path: pathlib.Path,
    post_id: str, 
    post_url: str,
    download_flags: tuple[bool, bool, bool, bool, bool]) -> Union[tuple[pathlib.Path, list[tuple[str, str]]], None]:
    """Get the details of a Pixiv Fanbox post using Pixiv Fanbox's API.

    Args:
        cookie (dict):
            The user's cookie to use to get access to the paywall-restricted post contents.
        download_path (pathlib.Path):
            The path to the folder where the post will be downloaded.
        post_id (str): 
            The post ID of the post to download.
        post_url (str):
            The post URL of the post to download.
        download_flags (tuple[bool, bool, bool, bool, bool]):
            A tuple of booleans that represent whether to download
            the post's images, thumbnail, attachments such as videos,
            gdrive files, and detect other external links such as MEGA links.

    Returns:
        A tuple of the post's folder path and a list of tuples 
        that contains the post's content urls and its content type.
        Otherwise, None if the post is not found.
    """
    download_images, download_thumbnail, download_attachments, \
        download_gdrive_links, detect_other_download_links = download_flags

    headers = C.PIXIV_API_HEADERS.copy()
    headers["Referer"] = post_url
    with httpx.Client(http2=True, cookies=format_cookie_to_cookiejar(cookie), headers=headers, timeout=15) as client:
        response = client.get(C.PIXIV_FANBOX_API_URL + post_id)
        post_info: dict = response.json().get("body")

    if (post_info is None):
        return

    post_title: str = post_info["title"]
    creator_name: str = post_info["creatorId"]
    post_folder_path = create_post_folder(
        download_path=download_path,
        creator_name=creator_name,
        post_id=post_id,
        post_title=post_title
    )

    urls_to_download_arr = []
    if (download_thumbnail):
        thumbnail: str = post_info.get("coverImageUrl")
        if (thumbnail is not None):
            urls_to_download_arr.append((thumbnail, C.THUMBNAIL_IMAGE))

    post_contents: dict = post_info["body"]
    if (download_gdrive_links or detect_other_download_links):
        article_content: list[dict] = post_contents.get("blocks", [])
        for article_block in article_content:
            text: str = article_block.get("text", "")
            if (text != ""):
                for password_text in C.PASSWORD_TEXTS:
                    if (password_text in text):
                        log_critical_details_for_post(
                            post_folder=post_folder_path,
                            message="Detected a possible password-protected " \
                                    f"content in the post: {password_text}\n",
                            log_filename="detected_passwords.txt"
                        )

            external_links_info_arr: list[dict] = article_block.get("links", [])
            for external_link_info in external_links_info_arr:
                external_link: str = external_link_info.get("url")
                if (external_link is not None):
                    if (download_gdrive_links and external_link.lower().startswith("https://drive.google.com/")):
                        urls_to_download_arr.append((external_link, C.GDRIVE_FILE))
                        continue

                    if (detect_other_download_links):
                        for other_file_hosting_service in C.OTHER_FILE_HOSTING_PROVIDERS:
                            if (other_file_hosting_service in external_link.lower()):
                                if (text != ""):
                                    text = f"[{text}] "
                                log_critical_details_for_post(
                                    post_folder=post_folder_path,
                                    message="Detected a link that points to an external file hosting " \
                                            f"provider in the post: {text}{external_link}\n",
                                    log_filename="detected_external_links.txt"
                                )

    if (download_images):
        image_files: dict[str, dict[str, Union[str, int]]] = post_contents.get("imageMap", {})
        for image_file in image_files.values():
            image_file_url: str = image_file["originalUrl"]
            urls_to_download_arr.append((image_file_url, C.IMAGE_FILE))

    if (download_attachments):
        attachment_files: dict[str, dict[str, Union[str, int]]] = post_contents.get("fileMap", {})
        for attachments in attachment_files.values():
            attachment_url: str = attachments["url"]
            urls_to_download_arr.append((attachment_url, C.ATTACHMENT_FILE))

    return (post_folder_path, urls_to_download_arr)