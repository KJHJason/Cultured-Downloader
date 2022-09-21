# import Python's standard libraries
import re
import sys
import struct
import pathlib
import platform
import warnings
from typing import TypeAlias
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

# User agent from https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
CHROME_USER_AGENT = " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
OS_USER_AGENTS = {
    "Windows":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Linux":
        "Mozilla/5.0 (X11; Linux x86_64)",
    "Darwin":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6)"
}
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
    USER_AGENT = OS_USER_AGENTS[USER_PLATFORM] + CHROME_USER_AGENT
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

    # Debug mode
    DEBUG_MODE: bool = False # For logger
    API_DEBUG_MODE: bool = True # (For requesting to the web application hosted on localhost)

    # For cryptographic operations with the user's saved cookies
    API_URL: str = "http://127.0.0.1:8080/api/v1" if (API_DEBUG_MODE) else "https://cultureddownloader.com/api/v1"
    TAG: bytes = " ".join(platform.uname()).encode("utf-8")

    # Application constants
    END: str = Style.RESET_ALL
    USER_PLATFORM: str = USER_PLATFORM
    ILLEGAL_PATH_CHARS_REGEX: re.Pattern[str] = re.compile(r"[<>:\"/\\|?*]")
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
    GOOGLE_OAUTH_HELPER_FILE: pathlib.Path = ROOT_PY_FILE_PATH.joinpath("helper", "google_oauth.py")
    ALTERNATIVE_GOOGLE_OAUTH_HELPER_FILE: pathlib.Path = pathlib.Path.home().joinpath("Desktop", "google_oauth.py")

    # For the webdriver manager
    DRIVER_FOLDER_PATH: pathlib.Path = APP_FOLDER_PATH.joinpath("webdrivers")
    DRIVER_CACHE_RANGE: int = 7 # days

    # Applications configuration, Google Drive API key, and cookies file paths
    FANTIA_COOKIE_PATH: pathlib.Path = appDir.joinpath("fantia-cookie")
    PIXIV_FANBOX_COOKIE_PATH: pathlib.Path = appDir.joinpath("pixiv-fanbox-cookie")
    GOOGLE_OAUTH_CLIENT_SECRET: pathlib.Path = appDir.joinpath("google-client-secret")
    GOOGLE_OAUTH_CLIENT_TOKEN: pathlib.Path = appDir.joinpath("google-client-token")
    CONFIG_JSON_FILE_PATH: pathlib.Path = appDir.joinpath("config.json")
    KEY_ID_TOKEN_JSON_PATH: pathlib.Path = appDir.joinpath("key-id-token.json")
    SECRET_KEY_PATH: pathlib.Path = appDir.joinpath("secret.key")

    # GitHub URLs
    ISSUE_PAGE: str = "https://github.com/KJHJason/Cultured-Downloader/issues"
    OAUTH2_GUIDE_PAGE: str = "https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/google_oauth2_guide.md"

    # For downloading
    GDRIVE_HINT_TYPING: TypeAlias = list[tuple[str, tuple[str, pathlib.Path]]]
    USER_AGENT: str = USER_AGENT
    BASE_REQ_HEADERS: dict[str, str] = field(
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
    PIXIV_FANBOX_API_HEADERS: dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent":
                USER_AGENT,
            "Accept": 
                "application/json",
            "Origin": 
                "https://www.fanbox.cc",
        }
    )
    MAX_RETRIES: int = 4
    RETRY_DELAY: int = 1.5 # 1.5 second
    CHUNK_SIZE: int = 1024 * 1024 # 1 MB
    IMAGE_FILE: str = "image"
    THUMBNAIL_IMAGE: str = "thumbnail"
    ATTACHMENT_FILE: str = "attachment"
    GDRIVE_FILE: str = "gdrive"
    GDRIVE_URL_REGEX: re.Pattern[str] = re.compile(
        r"https://drive\.google\.com/(file/d|drive/(u/\d+/)?folders)/([\w-]+)"
    )
    PASSWORD_TEXTS: tuple[str] = ("パス", "Pass", "pass", "密码")
    OTHER_FILE_HOSTING_PROVIDERS: tuple[str] = ("mega",)
    PAGE_NUM_REGEX: re.Pattern[str] = re.compile(r"^[1-9]\d*(-[1-9]\d*)?$")
    API_MAX_CONCURRENT_REQUESTS: int = 5
    MAX_CONCURRENT_DOWNLOADS_TABLE: dict[str, int] = field(
        default_factory=lambda: {
            "pixiv_fanbox":
                2,
            "fantia":
                4
        }
    )

    # For Fantia URLs
    FANTIA_API_URL: str = "https://fantia.jp/api/v1/posts/"
    FANTIA_COOKIE_NAME: str = "_session_id"
    FANTIA_WEBSITE_URL: str = "https://fantia.jp/"
    FANTIA_LOGIN_URL: str = "https://fantia.jp/sessions/signin"
    FANTIA_VERIFY_LOGIN_URL: str = "https://fantia.jp/mypage/users/plans"
    FANTIA_POST_REGEX: re.Pattern[str] = re.compile(r"^https://fantia\.jp/posts/\d+$")
    FANTIA_CREATOR_POSTS_REGEX: re.Pattern[str] = re.compile(r"^https://fantia\.jp/fanclubs/\d+(/posts)?$")

    # For Pixiv Fanbox URLs
    PIXIV_FANBOX_API_URL: str = "https://api.fanbox.cc/post.info?postId="
    PIXIV_FANBOX_COOKIE_NAME: str = "FANBOXSESSID"
    PIXIV_FANBOX_WEBSITE_URL: str = "https://www.fanbox.cc/"
    PIXIV_FANBOX_LOGIN_URL: str = "https://www.fanbox.cc/login"
    PIXIV_FANBOX_VERIFY_LOGIN_URL: str = "https://www.fanbox.cc/creators/supporting"
    PIXIV_FANBOX_POST_REGEX: re.Pattern[str] = re.compile(
        r"^https://(www\.fanbox\.cc/@[\w.-]+|[\w.-]+\.fanbox\.cc)/posts/\d+$"
    )
    PIXIV_FANBOX_CREATOR_POSTS_REGEX: re.Pattern[str] = re.compile(
        r"^https://(www\.fanbox\.cc/@[\w.-]+|[\w.-]+\.fanbox\.cc)(/posts)?$"
    )
    # Pixiv Fanbox permitted file extensions based on
    #   https://fanbox.pixiv.help/hc/en-us/articles/360011057793-What-types-of-attachments-can-I-post-
    PIXIV_FANBOX_ALLOWED_IMAGE_FORMATS: tuple[str] = ("jpg", "jpeg", "png", "gif")

CONSTANTS = Constants()

__all__ = [
    "CONSTANTS"
]