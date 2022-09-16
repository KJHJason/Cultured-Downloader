# import Python's standard libraries
import re
import sys
import struct
import pathlib
import platform
import warnings
from datetime import datetime
from dataclasses import dataclass, field

# import third-party libraries
from colorama import Style

# import local files
if (__package__ is None or __package__ == ""):
    from crucial import __version__
else:
    from .crucial import __version__

# Code to be executed upon import of this module
USER_PLATFORM = platform.system()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

DIRECTORIES = {
    "Windows": "AppData/Roaming/Cultured-Downloader",
    "Linux": ".config/Cultured-Downloader",
    "Darwin": "Library/Preferences/Cultured-Downloader"
}

appDir = pathlib.Path.home().absolute()
if (USER_PLATFORM in DIRECTORIES):
    if (USER_PLATFORM not in ("Windows", "Linux")):
        warnings.warn(
            message="Your operating system has not been tested so you may experience issues.", 
            category=RuntimeWarning
        )
    appDir = appDir.joinpath(DIRECTORIES[USER_PLATFORM])
    appDir.mkdir(parents=True, exist_ok=True)
else:
    print(f"Your OS, '{USER_PLATFORM}', is not supported")
    print("Supported OS: Windows, Linux, macOS...")
    print("Please enter any key to exit")
    input()
    sys.exit(1)

@dataclass(frozen=True, repr=False)
class Constants:
    """This dataclass is used to store all the constants used in the application."""
    # Inputs regex or tuples
    CMD_REGEX: re.Pattern[str] = re.compile(r"^[1-8xy]$")
    GOOGLE_API_KEY_REGEX: re.Pattern[str] = re.compile(
        r"^AIza[\w-]{35}$|^[xX]$" # based on https://github.com/odomojuli/RegExAPI
    )

    # Debug mode (For requesting to the web application hosted on localhost)
    DEBUG_MODE: bool = False

    # For cryptographic operations with the user's saved cookies
    API_URL: str = "http://127.0.0.1:8080/api/v1" if (DEBUG_MODE) else "https://cultureddownloader.com/api/v1"
    TAG: bytes = " ".join(platform.uname()).encode("utf-8")

    # Application constants
    END: str = Style.RESET_ALL
    USER_PLATFORM: str = USER_PLATFORM
    LOGGER_NAME: str = f"Cultured Downloader V{__version__}"
    IS_64BITS: bool = (struct.calcsize("P") * 8 == 64) # from https://stackoverflow.com/a/12568652/16377492
    DESKTOP_PATH: pathlib.Path = pathlib.Path.home().joinpath("Desktop")

    # Application paths
    ROOT_PY_FILE_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent.absolute()
    APP_FOLDER_PATH: pathlib.Path = appDir
    LOG_FOLDER_PATH: pathlib.Path = appDir.joinpath("logs")
    TODAYS_LOG_FILE_PATH: pathlib.Path = LOG_FOLDER_PATH.joinpath(
        f"cultured-downloader_v{__version__}_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    # For the webdriver manager
    DRIVER_FOLDER_PATH: pathlib.Path = APP_FOLDER_PATH.joinpath("webdrivers")
    DRIVER_CACHE_RANGE: int = 7 # days

    # Applications configuration, Google Drive API key, and cookies file paths
    FANTIA_COOKIE_PATH: pathlib.Path = appDir.joinpath("fantia-cookie")
    PIXIV_FANBOX_COOKIE_PATH: pathlib.Path = appDir.joinpath("pixiv-fanbox-cookie")
    GOOGLE_DRIVE_API_KEY_PATH: pathlib.Path = appDir.joinpath("gdrive-api-key")
    CONFIG_JSON_FILE_PATH: pathlib.Path = appDir.joinpath("config.json")
    KEY_ID_TOKEN_JSON_PATH: pathlib.Path = appDir.joinpath("key-id-token.json")
    SECRET_KEY_PATH: pathlib.Path = appDir.joinpath("secret.key")

    # Spinner JSON path
    SPINNERS_JSON_PATH: pathlib.Path = ROOT_PY_FILE_PATH.joinpath("json", "spinners.json")

    # GitHub issue page
    ISSUE_PAGE: str = "https://github.com/KJHJason/Cultured-Downloader/issues"

    # For downloading
    USER_AGENT: str = USER_AGENT
    REQ_HEADERS: dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent": 
                USER_AGENT,
        }
    )
    JSON_REQ_HEADERS: dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent": 
                USER_AGENT,
            "Content-Type": 
                "application/json"
        }
    )
    PAGE_NUM_REGEX: re.Pattern[str] = re.compile(r"^[1-9]\d*(-[1-9]\d*)?$")

    # For Fantia URLs
    FANTIA_COOKIE_NAME: str = "_session_id"
    FANTIA_WEBSITE_URL: str = "https://fantia.jp/"
    FANTIA_LOGIN_URL: str = "https://fantia.jp/sessions/signin"
    FANTIA_VERIFY_LOGIN_URL: str = "https://fantia.jp/mypage/users/plans"
    FANTIA_POST_REGEX: re.Pattern[str] = re.compile(r"^https://fantia\.jp/posts/\d+$")
    FANTIA_CREATOR_POSTS_REGEX: re.Pattern[str] = re.compile(r"^https://fantia\.jp/fanclubs/\d+(/posts)?$")
    FANTIA_POST_TITLE_REGEX: re.Pattern[str] = re.compile(r"^(.*) - (.*)の投稿｜ファンティア\[Fantia\]$")

    # For Pixiv Fanbox URLs
    PIXIV_FANBOX_COOKIE_NAME: str = "FANBOXSESSID"
    PIXIV_FANBOX_WEBSITE_URL: str = "https://www.fanbox.cc/"
    PIXIV_FANBOX_LOGIN_URL: str = "https://www.fanbox.cc/login"
    PIXIV_FANBOX_VERIFY_LOGIN_URL: str = "https://www.fanbox.cc/creators/supporting"
    PIXIV_FANBOX_POST_REGEX: re.Pattern[str] = re.compile(
        r"^https://(www\.fanbox\.cc/@[\w&.-]+|[\w&.-]+\.fanbox\.cc)/posts/\d+$"
    )
    PIXIV_FANBOX_CREATOR_POSTS_REGEX: re.Pattern[str] = re.compile(
        r"^https://(www\.fanbox\.cc/@[\w&.-]+|[\w&.-]+\.fanbox\.cc)(/posts)?$"
    )
    PIXIV_FANBOX_POST_TITLE_REGEX: re.Pattern[str] = re.compile(r"^(.*)｜(.*)｜pixivFANBOX$")

CONSTANTS = Constants()

__all__ = [
    "CONSTANTS"
]