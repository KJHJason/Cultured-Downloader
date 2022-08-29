# import Python's standard libraries
import pathlib
import shutil
from typing import Union, Optional

# import local files
if (__package__ is None or __package__ == ""):
    from crucial import install_dependency, __version__
    from functional import check_and_make_dir, print_danger
    from constants import CONSTANTS as C
else:
    from .crucial import install_dependency, __version__
    from .functional import check_and_make_dir, print_danger
    from .constants import CONSTANTS as C

# import third-party libraries
try:
    import aiohttp
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="aiohttp>=3.8.1")
    import aiohttp

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

import requests

async def download_fantia_image(postID: str, urls: list[str], folderPath: pathlib.Path) -> None:
    """Download images from Fantia.

    This function will download images from Fantia.
    The images will be downloaded to the folderPath provided.
    The images will be downloaded in parallel.

    Usage Example:
    >>> asyncio.run(download_fantia_image(urls=[urlOne, urlTwo], folderPath=pathlib.Path(".")))

    Args:
        postID (str):
            The postID of the post to download which will be used as reference in the event
            the download fails for logging purposes.
        urls (list[str]):
            The urls of the images to download.
        folderPath (pathlib.Path):
            The path to the folder where the images will be downloaded.

    Returns:
        None
    """
    check_and_make_dir(folderPath)

    filenameArr = []
    for url in urls:
        filenameArr.append(
            url.rsplit(sep="?", maxsplit=1)[0].rsplit(sep="/", maxsplit=1)[1]
        )

    failedToDownload = []
    async with aiohttp.ClientSession(headers=C.HEADERS) as session:
        for idx, url in enumerate(urls):
            async with session.get(url) as response:
                try:
                    if (response.status != 200):
                        raise Exception(f"Failed to download {url}")

                    async with aiofiles.open(folderPath.joinpath(filenameArr[idx]), "wb") as f:
                        await f.write(await response.read())
                except (
                    aiohttp.ClientConnectionError, 
                    aiohttp.ClientConnectorError, 
                    aiohttp.ServerConnectionError,
                    aiohttp.ClientSSLError,
                    aiohttp.ClientResponseError,
                    aiohttp.ContentTypeError,
                    aiohttp.TooManyRedirects,
                    aiohttp.ClientPayloadError,
                    aiohttp.ClientOSError
                ):
                    failedToDownload.append(url)

    if (failedToDownload):
        downloadLogFile = folderPath.joinpath("failed_downloads.log")
        with open(downloadLogFile, "a") as f:
            for url in failedToDownload:
                imageID = url.rsplit(sep="/", maxsplit=2)[1]
                f.write(f"https://fantia.jp/posts/{postID}/post_content_photo/{imageID}\n")

        print_danger(f"\nFailed to download {len(failedToDownload)} images from {postID}.\n")