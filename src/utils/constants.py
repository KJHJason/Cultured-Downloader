# import Python's standard libraries
from dataclasses import dataclass, field
import re
import platform
import pathlib
import sys

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

if (not appDir.exists() and not appDir.is_dir()):
    appDir.mkdir(parents=True)

@dataclass(frozen=True, repr=False)
class Constants:
    """This dataclass is used to store all the constants used in the application."""
    # Inputs regex or tuples
    CMD_REGEX: re.Pattern[str] = re.compile(r"^[1-6xy]$")

    # Debug mode (For requesting to the web application hosted on localhost)
    DEBUG_MODE: bool = True

    # For cryptographic operations with the user's saved cookies
    WEBSITE_URL: str = "http://127.0.0.1:8080" if (DEBUG_MODE) else "https://cultureddownloader.com"
    SERVER_RESPONSE_SCHEMA: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "cookie": {"type": "string"}
            },
            "required": ["cookie"]
        }
    )
    SERVER_PUBLIC_KEY_SCHEMA: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "public_key": {"type": "string"}
            },
            "required": ["public_key"]
        }
    )

    # Application constants
    END: str = Style.RESET_ALL
    USER_PLATFORM: str = USER_PLATFORM
    ROOT_PY_FILE_PATH: pathlib.Path = pathlib.Path(__file__).parent.parent.absolute()
    APP_FOLDER_PATH: pathlib.Path = appDir
    LOG_FOLDER_PATH: pathlib.Path = appDir.joinpath("logs")
    CONFIG_JSON_FILE_PATH: pathlib.Path = appDir.joinpath("config.json")
    COOKIES_PATH: pathlib.Path = appDir.joinpath("cookies")

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

    # For Fantia URLS
    FANTIA_POST: re.Pattern[str] = re.compile(r"^(https://fantia.jp/posts/)\d+$")
    FANTIA_CREATOR_POSTS: re.Pattern[str] = re.compile(r"^(https://fantia.jp/fanclubs/)\d+(/posts)$")

    # For Pixiv Fanbox URLS
    PIXIV_FANBOX_POST: re.Pattern[str] = re.compile(
        r"^(https://www.fanbox.cc/@)[\w&.-]+(/posts/)\d+$|^(https://)[\w&.-]+(.fanbox.cc/posts/)\d+$"
    )
    PIXIV_FANBOX_CREATOR_POSTS: re.Pattern[str] = re.compile(
        r"^(https://www.fanbox.cc/@)[\w&.-]+(/posts)$|^(https://)[\w&.-]+(.fanbox.cc/posts)$"
    )

    # Config json schema
    CONFIG_SCHEMA: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "download_directory": {
                    "type": "string"
                },
                "language": {
                    "type": "string",
                    "enum": ["en"] # only en is supported (considering jp)
                }
            },
            "required": ["download_directory", "language"]
        }
    )

CONSTANTS = Constants()

__all__ = [
    "CONSTANTS"
]