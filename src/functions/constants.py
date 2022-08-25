# import Python's standard libraries
from dataclasses import dataclass, field
import re
import platform
import pathlib

# import third-party libraries
from colorama import Style

@dataclass(frozen=True, repr=False)
class Constants:
    """This dataclass is used to store all the constants used in the application."""

    # Inputs regex or tuples
    CMD_REGEX: re.Pattern[str] = re.compile(r"^[1-6xy]$")

    # Application constants
    END: str = Style.RESET_ALL
    USER_PLATFORM: str = platform.system()
    ROOT_FILE_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent.absolute()

    # GitHub issue page
    ISSUE_PAGE: str = "https://github.com/KJHJason/Cultured-Downloader/issues"

    # For downloading
    HEADERS: dict[str, str] = field(default_factory=lambda :{
        "User-Agent": 
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    })
    POST_NUM_FOLDER_NAME: re.Pattern[str] = re.compile(r"^(Post-)(\d+)$")
    PAGE_NUM: re.Pattern[str] = re.compile(r"[1-9][0-9]{0,}(-)[1-9][0-9]{0,}|[1-9][0-9]{0,}")

    # For Fantia URLS
    FANTIA_POST: re.Pattern[str] = re.compile(r"(https://fantia.jp/posts/)\d+")
    FANTIA_CREATOR_POSTS: re.Pattern[str] = re.compile(r"(https://fantia.jp/fanclubs/)\d+(/posts)")

    # For Pixiv Fanbox URLS
    PIXIV_FANBOX_POST: re.Pattern[str] = re.compile(
        r"(https://www.fanbox.cc/@)[\w&.-]+(/posts/)\d+|(https://)[\w&.-]+(.fanbox.cc/posts/)\d+"
    )
    PIXIV_FANBOX_CREATOR_POSTS: re.Pattern[str] = re.compile(
        r"(https://www.fanbox.cc/@)[\w&.-]+(/posts)|(https://)[\w&.-]+(.fanbox.cc/posts)"
    )

CONSTANTS = Constants()

__all__ = [
    "CONSTANTS"
]