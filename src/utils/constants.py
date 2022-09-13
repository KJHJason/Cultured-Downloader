# import Python's standard libraries
import re
import sys
import struct
import pathlib
import platform
from dataclasses import dataclass, field

# import third-party libraries
from colorama import Style

# Code to be executed upon import of this module
USER_PLATFORM = platform.system()

DIRECTORIES = {
    "Windows": "AppData/Roaming/Cultured-Downloader",
    "Linux": ".config/Cultured-Downloader",
    "Darwin": "Library/Preferences/Cultured-Downloader"
}

appDir = pathlib.Path.home().absolute()
if (USER_PLATFORM in DIRECTORIES):
    appDir = appDir.joinpath(DIRECTORIES[USER_PLATFORM])
else:
    print("Your OS is not supported")
    print("Supported OS: Windows, Linux, macOS...")
    print("Please enter any key to exit")
    sys.exit(1)

appDir.mkdir(parents=True, exist_ok=True)

@dataclass(frozen=True, repr=False)
class Constants:
    """This dataclass is used to store all the constants used in the application."""
    # Inputs regex or tuples
    CMD_REGEX: re.Pattern[str] = re.compile(r"^[1-6xy]$")

    # Debug mode (For requesting to the web application hosted on localhost)
    DEBUG_MODE: bool = False

    # For cryptographic operations with the user's saved cookies
    API_URL: str = "http://127.0.0.1:8080/api/v1" if (DEBUG_MODE) else "https://cultureddownloader.com/api/v1"
    TAG: bytes = " ".join(platform.uname()).encode("utf-8")

    # Application constants
    END: str = Style.RESET_ALL
    USER_PLATFORM: str = USER_PLATFORM
    IS_64BITS: bool = (struct.calcsize("P") * 8 == 64) # from https://stackoverflow.com/a/12568652/16377492
    DESKTOP_PATH: pathlib.Path = pathlib.Path.home().joinpath("Desktop")

    # Application paths
    ROOT_PY_FILE_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent.absolute()
    APP_FOLDER_PATH: pathlib.Path = appDir
    LOG_FOLDER_PATH: pathlib.Path = appDir.joinpath("logs")

    # Applications configuration and cookies file paths
    CONFIG_JSON_FILE_PATH: pathlib.Path = appDir.joinpath("config.json")
    KEY_ID_TOKEN_JSON_PATH: pathlib.Path = appDir.joinpath("key-id-token.json")
    SECRET_KEY_PATH: pathlib.Path = appDir.joinpath("secret.key")

    # Spinner JSON path
    SPINNERS_JSON_PATH: pathlib.Path = ROOT_PY_FILE_PATH.joinpath("utils", "json", "spinners.json")

    # GitHub issue page
    ISSUE_PAGE: str = "https://github.com/KJHJason/Cultured-Downloader/issues"

    # For downloading
    REQ_HEADERS: dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent": 
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Content-Type": 
                "application/json"
        }
    )
    POST_NUM_FOLDER_NAME: re.Pattern[str] = re.compile(r"^(Post-)(\d+)$")
    PAGE_NUM: re.Pattern[str] = re.compile(r"^([1-9]\d*)(-([1-9]\d*))?$")

    # For Fantia URLs
    FANTIA_COOKIE_NAME: str = "_session_id"
    FANTIA_WEBSITE_URL: str = "https://fantia.jp/"
    FANTIA_LOGIN_URL: str = "https://fantia.jp/sessions/signin"
    FANTIA_VERIFY_LOGIN_URL: str = "https://fantia.jp/mypage/users/plans"
    FANTIA_POST: re.Pattern[str] = re.compile(r"^(https://fantia.jp/posts/)\d+$")
    FANTIA_CREATOR_POSTS: re.Pattern[str] = re.compile(r"^(https://fantia.jp/fanclubs/)\d+(/posts)$")

    # For Pixiv Fanbox URLs
    PIXIV_FANBOX_COOKIE_NAME: str = "FANBOXSESSID"
    PIXIV_FANBOX_WEBSITE_URL: str = "https://www.fanbox.cc/"
    PIXIV_FANBOX_LOGIN_URL: str = "https://www.fanbox.cc/login"
    PIXIV_FANBOX_VERIFY_LOGIN_URL: str = "https://www.fanbox.cc/creators/supporting"
    PIXIV_FANBOX_POST: re.Pattern[str] = re.compile(
        r"^(https://www.fanbox.cc/@)[\w&.-]+(/posts/)\d+$|^(https://)[\w&.-]+(.fanbox.cc/posts/)\d+$"
    )
    PIXIV_FANBOX_CREATOR_POSTS: re.Pattern[str] = re.compile(
        r"^(https://www.fanbox.cc/@)[\w&.-]+(/posts)$|^(https://)[\w&.-]+(.fanbox.cc/posts)$"
    )

CONSTANTS = Constants()

__all__ = [
    "CONSTANTS"
]