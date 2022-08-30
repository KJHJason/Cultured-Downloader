# import Python's standard libraries
import pathlib
import shutil
from typing import Union, Optional

# import local files
if (__package__ is None or __package__ == ""):
    from crucial import install_dependency, __version__
    from functional import print_danger
    from constants import CONSTANTS as C
else:
    from .crucial import install_dependency, __version__
    from .functional import print_danger
    from .constants import CONSTANTS as C

# import third-party libraries
try:
    import httpx
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="httpx[http2]>=0.23.0")
    import httpx

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

async def download_fantia_image(post_id: str, urls: list[str], folder_path: pathlib.Path) -> None:
    """Download images from Fantia.

    This function will download images from Fantia.
    The images will be downloaded to the folder_path provided.
    The images will be downloaded in parallel.

    Usage Example:
    >>> asyncio.run(download_fantia_image(urls=[urlOne, urlTwo], folder_path=pathlib.Path(".")))

    Args:
        post_id (str):
            The post ID of the post to download which will be used as reference in the event
            the download fails for logging purposes.
        urls (list[str]):
            The urls of the images to download.
        folder_path (pathlib.Path):
            The path to the folder where the images will be downloaded.

    Returns:
        None
    """
    folder_path.mkdir(parents=True, exist_ok=True)

    filename_arr = []
    for url in urls:
        filename_arr.append(
            url.rsplit(sep="?", maxsplit=1)[0].rsplit(sep="/", maxsplit=1)[1]
        )

    # To keep track of failed downloads and log them 
    # for the user to manually download them.
    failed_to_download = []

    # Using httpx instead of aiohttp for HTTP/2 support since Fantia uses AWS S3
    # and I have tested it for HTTP/2 compatibility which would help improve download speeds.
    async with httpx.AsyncClient(headers=C.REQ_HEADERS, http2=True) as client:
        for idx, url in enumerate(urls):
            async with client.stream(method="GET", url=url) as response:
                file_path = folder_path.joinpath(filename_arr[idx])
                try:
                    if (response.status_code != 200):
                        raise Exception(f"Failed to download {url}")

                    async with aiofiles.open(file_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            await f.write(chunk)
                except (
                    httpx.RequestError,
                    httpx.HTTPStatusError,
                    httpx.HTTPError,
                    httpx.StreamError
                ):
                    file_path.unlink(missing_ok=True)
                    failed_to_download.append(url)

    if (failed_to_download):
        download_log_file = folder_path.joinpath("failed_downloads.log")
        with open(download_log_file, "a") as f:
            for url in failed_to_download:
                image_id = url.rsplit(sep="/", maxsplit=2)[1]
                f.write(f"https://fantia.jp/posts/{post_id}/post_content_photo/{image_id}\n")

        print_danger(f"\nFailed to download {len(failed_to_download)} images from {post_id}.\n")