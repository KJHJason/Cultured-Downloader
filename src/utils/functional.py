# import Python's standard libraries
import re
import time
import json
import pathlib
from typing import Union, Optional, Any

# import local files
if (__package__ is None or __package__ == ""):
    from spinner import Spinner
    from schemas.config import ConfigSchema
    from errors import APIServerError
    from constants import CONSTANTS as C
    from logger import logger
else:
    from .spinner import Spinner
    from .schemas.config import ConfigSchema
    from .errors import APIServerError
    from .constants import CONSTANTS as C
    from .logger import logger

# import third-party libraries
import httpx
from colorama import Fore as F
from pydantic import BaseModel
import pydantic.error_wrappers as pydantic_error_wrappers 

def website_to_readable_format(website: str) -> str:
    """Converts a website string to a readable format.

    Args:
        website (str): 
            The website to convert.

    Returns:
        str: 
            The readable format of the website.
    """
    readable_table = {
        "fantia": "Fantia",
        "pixiv_fanbox": "Pixiv Fanbox",
    }
    if (website not in readable_table):
        raise ValueError(f"Invalid website: {website}")
    return readable_table[website]

def log_api_error(error_msg: str) -> None:
    """Log any errors such as Cultured Downloader API's 5XX errors.

    Args:
        error_msg (str):
            The error message to log.

    Returns:
        None

    Raise:
        APIServerError after logging the error message.
    """
    logger.error(f"API Server Error:\n{error_msg}")
    raise APIServerError(error_msg)

def validate_schema(schema: BaseModel, data: Union[dict, list], 
                    return_bool: Optional[bool] = True) -> Union[bool, BaseModel]:
    """Validates the data against the schema

    Args:
        schema (BaseModel): 
            The pydantic base model object to validate against
        data (dict | list):
            The data to validate
        return_bool (bool, optional):
            Whether to return a boolean or the pydantic base model object.

    Returns:
        Union[bool, BaseModel]:
            False if the data is invalid, otherwise the pydantic base model object with the data or a boolean.
    """
    if (not isinstance(data, Union[dict, list])):
        return False

    try:
        pydantic_obj = schema(**data)
        return pydantic_obj if (not return_bool) else True
    except (pydantic_error_wrappers.ValidationError) as e:
        logger.info(
            f"Data is invalid when validated against the schema, {schema.__name__}: {e}\n\nData: {data}"
        )
        return False

def print_danger(message: Any, **kwargs) -> None:
    """Print a message in red.

    Args:
        message (Any):
            The message to print.
        kwargs:
            Any keyword arguments to pass to the print function.

    Returns:
        None
    """
    print(f"{F.LIGHTRED_EX}{message}{F.RESET}", **kwargs)

def print_warning(message: Any, **kwargs) -> None:
    """Print a message in light yellow.

    Args:
        message (Any):
            The message to print.
        kwargs:
            Any keyword arguments to pass to the print function.

    Returns:
        None
    """
    print(f"{F.LIGHTYELLOW_EX}{message}{F.RESET}", **kwargs)

def print_success(message: Any, **kwargs) -> None:
    """Print a message in green.

    Args:
        message (Any):
            The message to print.
        kwargs:
            Any keyword arguments to pass to the print function.

    Returns:
        None
    """
    print(f"{F.LIGHTGREEN_EX}{message}{F.RESET}", **kwargs)

def save_key_prompt() -> bool:
    """Prompt the user where necessary if they want to save their 
    generated secret key on their computer or to Cultured Downloader API."""
    if (C.KEY_ID_TOKEN_JSON_PATH.exists() and C.KEY_ID_TOKEN_JSON_PATH.is_file()):
        return False

    if (C.SECRET_KEY_PATH.exists() and C.SECRET_KEY_PATH.is_file()):
        return True

    save_key = get_input(
        input_msg="Enter your desired action (API, LOCAL): ",
        inputs=("api", "local"),
        extra_information="""
Would you like to save your secret key on your computer or on Cultured Downloader API?

If you were to save it on Cultured Downloader API, 
key rotations will be enabled for you and it is more secure if your computer is being shared.
Important Note: If you are currently using a proxy such as a VPN, please disable it as the saved key
is mapped to your IP address (Don't worry as your IP address is hashed on our database).

However, if you prefer faster loading speed than security, 
you can instead opt for your key to be saved locally on your computer.

TLDR (Too long, didn't read):
Enter \"API\" to save your secret key to Cultured Downloader API for security,
\"LOCAL\" otherwise to save it locally on your computer for faster loading time.
""")
    return True if (save_key == "local") else False

def load_configs() -> ConfigSchema:
    """Load the configs from the config file.

    Returns:
        ConfigSchema: 
            The configs loaded from the config file.
    """
    configs = {}
    if (C.CONFIG_JSON_FILE_PATH.exists() and C.CONFIG_JSON_FILE_PATH.is_file()):
        with open(C.CONFIG_JSON_FILE_PATH, "r") as f:
            configs = json.load(f)

    schema_obj = validate_schema(schema=ConfigSchema, data=configs, return_bool=False)
    if (schema_obj is False):
        # If the config JSON data is invalid,
        # reset the config file to the default values 
        # and save it to the config JSON file.
        schema_obj = ConfigSchema(**{})
        edit_configs(new_configs=schema_obj.dict())

    # check if the download directory exists
    download_dir = pathlib.Path(schema_obj.download_directory)
    if (not download_dir.exists() or not download_dir.is_dir()):
        # if the download directory does not exist,
        # reset to the user's desktop folder path.
        schema_obj.download_directory = str(pathlib.Path.home().joinpath("Desktop", "cultured-downloader"))

    return schema_obj

def edit_configs(new_configs: dict) -> None:
    """Edit the configs in the config file.

    Args:
        new_configs (dict):
            The new configuration to save to the config file.

    Returns:
        None
    """
    with open(C.CONFIG_JSON_FILE_PATH, "w") as f:
        json.dump(new_configs, f, indent=4)

def change_download_directory(configs: Optional[ConfigSchema] = None, 
                              print_message: Optional[bool] = False) -> None:
    """Change the download directory in the config file.

    Args:
        configs (ConfigSchema, optional):
            The configs to edit. If None, the configs will be loaded from the config file.
        print_message (bool, optional):
            Whether to print the messages to the user to inform them that the changes have been saved
            but will require the user to re-run the program for the changes to take effect.

    Returns:
        None
    """
    if (configs is None):
        configs = load_configs()

    print_warning(f"Your current download directory is\n{configs.download_directory}")
    change_download_directory = get_input(
        input_msg="Do you want to change your download directory? (y/N): ",
        inputs=("y", "n"),
        default="n"
    )
    if (change_download_directory == "y"):
        while (True):
            download_directory_path = input("Enter your new download directory (X to cancel): ").strip()
            if (download_directory_path == ""):
                print_danger("Please enter a valid download directory.\n")
                continue

            if (download_directory_path.lower() == "x"):
                print_warning("Cancelled changing webdriver's download directory.")
                break

            download_directory_path = pathlib.Path(download_directory_path)
            if (not download_directory_path.exists() or not download_directory_path.is_dir()):
                print_danger("Download directory does not exist, please create it first and try again.\n")
                continue

            download_directory_path = str(download_directory_path)
            if (configs.download_directory == download_directory_path):
                print_danger("Download directory is already set to that.\n")
                continue

            configs.download_directory = download_directory_path
            edit_configs(configs.dict())
            print_success(f"Download directory successfully changed to\n{download_directory_path}")

            if (print_message):
                print_danger("\nImportant: You will need to re-run the program for the changes to take effect.")

            break
    print()

def print_menu(login_status: dict[str, bool], gdrive_api_key: Union[str, None]) -> None:
    """Print the menu for the user to read and enter their desired action.

    Args:
        login_status (dict[str, bool]):
            The login status of the user,
            E.g. {"pixiv_fanbox": False, "fantia": True}
        gdrive_api_key (str | None):
            The Google Drive API key if it exists, None otherwise.

    Returns:
        None
    """
    fantia_status = login_status.get("fantia")
    pixiv_status = login_status.get("pixiv_fanbox")
    print(f"""{F.LIGHTYELLOW_EX}
> Login Status...
> Fantia: {'Logged In' if (fantia_status) else 'Guest (Not logged in)'}
> Pixiv: {'Logged In' if (pixiv_status) else 'Guest (Not logged in)'}
{C.END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{C.END} --------------------
      {F.GREEN}1. Download images from Fantia post(s){C.END}
      {F.GREEN}2. Download all Fantia posts from creator(s){C.END}
      {F.LIGHTCYAN_EX}3. Download images from pixiv Fanbox post(s){C.END}
      {F.LIGHTCYAN_EX}4. Download all pixiv Fanbox posts from a creator(s){C.END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{C.END} ----------------------
      {F.LIGHTBLUE_EX}5. Change Default Download Folder{C.END}""")

    if (gdrive_api_key is None):
        print(f"""      {F.LIGHTBLUE_EX}6. Set Google Drive API Key{C.END}""")
    else:
        print(f"""      {F.LIGHTBLUE_EX}6. Remove Google Drive API Key{C.END}""")

    if (not fantia_status or not pixiv_status):
        print(f"      {F.LIGHTBLUE_EX}7. Login{C.END}")
    if (fantia_status or pixiv_status):
        print(f"      {F.LIGHTBLUE_EX}8. Logout{C.END}")

    print(f"\n---------------------- {F.LIGHTYELLOW_EX}Other Options{C.END} ----------------------")
    print(f"      {F.LIGHTRED_EX}Y. Report a bug{C.END}")
    print(f"      {F.RED}X. Shutdown the program{C.END}")
    print()

def get_input(input_msg: str, inputs: Optional[Union[tuple[str], list[str]]] = None, 
              regex: re.Pattern[str] = None, default: Optional[str] = None, warning: str = None, 
              extra_information: Optional[str] = None, is_case_sensitive: Optional[bool] = False) -> Any:
    """Get the expected input from the user.

    Args:
        input_msg (str):
            The message to print to the user.
        inputs (tuple[str] | list[str], optional):
            The inputs that the user can enter.
            Note: inputs must be lowercase but will be converted to lowercase string as a failsafe.
            If this is passed in, regex parameter cannot be passed in!
        regex (re.Pattern[str], optional):
            The regex pattern to match the input against.
            If this is passed in, inputs parameter cannot be passed in!
        default (str, optional):
            The default input to be returned if the user doesn't enter anything.
        warning (str, optional):
            The warning message to print to the user if the input is invalid.
        extra_information (str, optional):
            The extra information to print to the user before the input message.
        is_case_sensitive (bool, optional):
            Whether the input is case sensitive or not. 
            If so, the inputs and the user's input will not be converted to lowercase.

    Returns:
        The input the user entered.

    Raises:
        ValueError:
            If the inputs and regex are both passed in.
    """
    if (inputs and regex):
        raise ValueError("inputs and regex cannot be passed in together")

    if (inputs is not None and (not isinstance(inputs, tuple) and not isinstance(inputs, list))):
        raise TypeError("inputs must be a tuple or a list")
    if (regex is not None and not isinstance(regex, re.Pattern)):
        raise TypeError("regex must be a re.Pattern")
    if (warning is not None and not isinstance(warning, str)):
        raise TypeError("warning must be a str")

    if (inputs is not None):
        # fail-safe if the list or tuple passed in does not contain strings
        if (not is_case_sensitive):
            inputs = tuple(str(inp).lower() for inp in inputs)
        else:
            inputs = tuple(str(inp) for inp in inputs)

    while (True):
        if (extra_information is not None):
            print_warning(extra_information)

        user_input = input(input_msg).strip()
        if (not is_case_sensitive):
            user_input = user_input.lower()

        if (inputs is not None and user_input in inputs):
            return user_input
        elif (regex is not None and regex.match(user_input)):
            return user_input
        elif (default is not None and user_input == ""):
            return default
        else:
            print_danger(f"Sorry, please enter a valid input." if (warning is None) else warning)

def get_user_download_choices(website: str) -> Union[tuple[bool, bool, bool], tuple[bool, bool, bool, bool, bool], None]:
    """Prompt the user and get their download preferences.

    Args:
        website (str):
            The website to get the download preferences for.
            If the website is "fantia", gdrive and detection of 
            other file hosting provider links will be disabled.

    Returns:
        A tuple of boolean or None if the user cancels the download process:
            (download_images, download_thumbnail, download_attachment).\n
            If the website is not "fantia", the tuple will have an additional last 2 booleans:
                download_gdrive_links, detect_other_download_links
    """
    while (True):
        download_images = get_input(
            input_msg="Download images? (Y/n/x to cancel): ",
            inputs=("y", "n", "x"),
            default="y"
        )
        if (download_images == "x"):
            return

        download_thumbnail = get_input(
            input_msg="Download thumbnail? (Y/n/x to cancel): ",
            inputs=("y", "n", "x"),
            default="y"
        )
        if (download_thumbnail == "x"):
            return

        download_attachments = get_input(
            input_msg="Download attachments? (Y/n/x to cancel): ",
            inputs=("y", "n", "x"),
            default="y"
        )
        if (download_attachments == "x"):
            return

        download_flags = [
            download_images == "y", 
            download_thumbnail == "y",
            download_attachments == "y"
        ]
        if (website != "fantia"):
            download_gdrive_links = get_input(
                input_msg="Download Google Drive links? (Y/n/x to cancel): ",
                inputs=("y", "n", "x"),
                default="y"
            )
            if (download_gdrive_links == "x"):
                return

            detect_other_download_links = get_input(
                input_msg="Detect other download links such as MEGA links? (Y/n/x to cancel): ",
                inputs=("y", "n", "x"),
                default="y"
            )
            if (detect_other_download_links == "x"):
                return

            download_flags.extend([
                download_gdrive_links == "y", 
                detect_other_download_links == "y"
            ])

        if (not any(download_flags)):
            print_danger("Please select at least one download option...\n")
        else:
            return tuple(download_flags)

def get_user_urls(website: str, creator_page: bool) -> Union[list[str], None]:
    """Get the URLs from the user.

    Args:
        website (str):
            The website the user is downloading from.
        creator_page (bool):
            Whether the user is downloading from a creator's page or not.

    Returns:
        list[str] | None: 
            The list of validated URLs, None if the user wishes to exit.
    """
    url_guide_and_regex_table = {
        "fantia": (
            ("https://fantia.jp/posts/1234567", C.FANTIA_POST_REGEX),
            ("https://fantia.jp/fanclubs/1234/posts", C.FANTIA_CREATOR_POSTS_REGEX)
        ),
        "pixiv_fanbox": (
            ("https://www.fanbox.cc/@creator_name/posts/1234567 or " \
             "https://creator_name.fanbox.cc/posts/1234567", C.PIXIV_FANBOX_POST_REGEX),
            ("https://www.fanbox.cc/@creator_name/posts or " \
             "https://creator_name.fanbox.cc/posts", C.PIXIV_FANBOX_CREATOR_POSTS_REGEX)
        )
    }
    if (website not in url_guide_and_regex_table):
        raise ValueError(f"Invalid website: {website}")

    extra_info = "This option is for URL(s) such as "
    url_guide, input_regex = url_guide_and_regex_table[website][creator_page]
    extra_info += url_guide
    extra_info += "\nAdditionally, you can enter multiple URLs separated by a comma."
    while (True):
        print_warning(extra_info)
        user_input = input("\nEnter URL(s) (X to cancel): ").strip()
        if (user_input == ""):
            print_danger("User Error: Please enter a URL")
            continue
        elif (user_input in ("X", "x")):
            return

        urls_arr = [url.strip() for url in user_input.split(",")]
        unique_urls = list(dict.fromkeys(urls_arr, None))
        if (len(unique_urls) != len(urls_arr)):
            print_danger("Warning: Duplicate URLs have been removed from your input...")

        formatted_urls = []
        for url in unique_urls:
            # Since a url can end with a slash,
            # remove it so for the regex validations
            # and to add GET parameters to the url.
            if (url.endswith("/")):
                url = url[:-1]

            if (input_regex.fullmatch(url) is not None):
                if (creator_page and not url.endswith("/posts")):
                    url += "/posts"
                formatted_urls.append(url)
                continue

            error_msg = "User Error: The URL, {url}, is invalid.\n" \
                        "Please make sure {suggestion} correct and try again.".format(
                            url=url,
                            suggestion="all the URLs entered are" \
                                        if (len(url) > 1) \
                                        else "the URL entered is"
                        )
            print_danger(error_msg)
            break
        else:
            # print out the formatted URLs and confirm with the user
            print_warning("\nThe following URLs will be downloaded:\n{urls}".format(
                urls=", ".join(formatted_urls)
            ))
            confirm = get_input(
                input_msg="Do you wish to download from these URLs? (Y/n): ",
                inputs=("y", "n"),
                default="y",
            )
            if (confirm == "n"):
                continue

            # Since there is no need to get more inputs 
            # from the user for downloading posts,
            # return the formatted URLs.
            if (not creator_page):
                return formatted_urls
            else:
                break

    # get page number from user
    print_warning(
        "\nPlease enter the page numbers you wish to download from corresponding to the URLs you entered." \
        "\nFor example, if you entered 2 URLs, you will enter something like '1, 1-3' to indicate " \
        "that you wish to download from the 1st page of the first URL and the 1st to 3rd page of the second URL."
    )
    page_num_prompt = "\nPlease enter {} (X to cancel): ".format(
        f"{len(formatted_urls)} page numbers corresponding to the entered URLs" \
        if (len(formatted_urls > 1)) \
        else "a page number"
    )
    while (True):
        page_inputs = input(page_num_prompt).strip()
        if (page_inputs == ""):
            print_danger("User Error: Please enter a page number")
            continue
        elif (user_input in ("X", "x")):
            return

        page_nums_arr = page_inputs.split(sep=",")
        if (len(page_nums_arr) != len(formatted_urls)):
            print_danger(
                "User Error: The number of page numbers entered does not match the number of URLs entered"
            )
            continue

        url_with_page_nums_arr = []
        for idx, page_num in enumerate(page_nums_arr):
            page_num = page_num.strip()
            if (C.PAGE_NUM_REGEX.fullmatch(page_num) is None):
                print_danger(f"User Error: The page number, {page_num}, is invalid.")
                print_danger("Please enter in the correct format such as '1, 1-3' and try again.")
                break

            page_nums = page_num.split(sep="-", maxsplit=1)
            if (len(page_nums) == 1):
                url_with_page_nums_arr.append(formatted_urls[idx] + f"?page={page_nums[0]}")
                continue

            # if a range was given, make sure the range is valid
            page_nums = [int(page_num) for page_num in page_nums]
            if (page_nums[0] > page_nums[1]):
                page_nums[0], page_nums[1] = page_nums[1], page_nums[0]

            for page_num in range(page_nums[0], page_nums[1] + 1):
                url_with_page_nums_arr.append(formatted_urls[idx] + f"?page={page_num}")
        else:
            return url_with_page_nums_arr

def delete_empty_and_old_logs() -> None:
    """Delete all empty log files and log files
    older than 30 days except for the current day's log file.

    Returns:
        None
    """
    for log_file in C.LOG_FOLDER_PATH.iterdir():
        if (log_file.is_file() and log_file != C.TODAYS_LOG_FILE_PATH):
            file_info = log_file.stat()
            if (file_info.st_size == 0 or file_info.st_mtime < (time.time() - 2592000)):
                try:
                    log_file.unlink()
                except (PermissionError, FileNotFoundError):
                    pass

@Spinner(
    message="Checking for an active internet connection...",
    colour="light_yellow",
    spinner_type="arc",
    spinner_position="left"
)
def check_internet_connection() -> bool:
    """Check if the user has an internet connection by sending a HEAD request to google.com

    Returns:
        bool: 
            True if the user has an internet connection, False otherwise.
    """
    with httpx.Client(http2=True, headers=C.BASE_REQ_HEADERS, timeout=5) as client:
        try:
            client.head("https://www.google.com")
        except (httpx.ConnectTimeout):
            return False
    return True

def user_has_saved_cookies() -> bool:
    """Check if the user has saved cookies for Fantia and Pixiv Fanbox.

    Returns:
        bool: 
            True if the user has saved any cookies, False otherwise.
    """
    return ((C.FANTIA_COOKIE_PATH.exists() and C.FANTIA_COOKIE_PATH.is_file()) or \
            (C.PIXIV_FANBOX_COOKIE_PATH.exists() and C.PIXIV_FANBOX_COOKIE_PATH.is_file()))