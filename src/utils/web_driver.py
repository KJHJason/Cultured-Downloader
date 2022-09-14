# import third-party libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as selenium_exceptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# import Python's standard libraries
import time
import types
import logging
import pathlib
from os import environ
from typing import Optional, Union, Type

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from logger import logger
    from spinner import Spinner
    from user_data import convert_to_readable_format
    from functional import print_danger, get_input
else:
    from .constants import CONSTANTS as C
    from .logger import logger
    from .spinner import Spinner
    from .user_data import convert_to_readable_format
    from .functional import print_danger, get_input

class CustomWebDriver(webdriver.Chrome):
    """Custom chrome webdriver with some modifications."""
    SHUTDOWN_MSG = "Shutting down webdriver instance..."

    def quit_with_message(self) -> None:
        """Close the browser and display a message since 
        it can take quite a while to shut down the webdriver instance."""
        with Spinner(
            message=self.SHUTDOWN_MSG,
            colour="light_yellow", 
            spinner_type="arc", 
            spinner_position="left"
        ):
            self.quit()

    def __exit__(self, 
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[types.TracebackType]
    ) -> None:
        """Close the browser and display a message since 
        it can take quite a while to shut down the webdriver instance."""
        with Spinner(
            message=self.SHUTDOWN_MSG,
            colour="light_yellow", 
            spinner_type="arc", 
            spinner_position="left"
        ):
            self.quit()

@Spinner(
    message="Initializing a new webdriver instance...", 
    colour="light_yellow", 
    spinner_type="arc", 
    spinner_position="left"
)
def get_driver(
    download_path: Union[pathlib.Path, str],
    headless: Optional[bool] = True, 
    block_images: Optional[int] = 2, 
    window_size: tuple[int, int] = (1920, 1080)) -> CustomWebDriver:
    """Get a Chrome webdriver instance.

    Args:
        download_path (Union[pathlib.Path, str]): 
            The path to the download directory.
        headless (bool, optional): 
            Whether to run the browser in headless mode. Defaults to True.
        block_images (bool, optional):
            Whether to block images from loading. Defaults to 0 for default configurations.
            For numbers, use the definition below:
                0: default, 1: allow, 2: block
        window_size (tuple[int, int], optional):
            The size of the browser window. Defaults to (1920, 1080).

    Returns:
        A Chrome webdriver instance (CustomWebDriver).
    """
    # Configurations for the webdriver manager
    environ["WDM_LOG_LEVEL"] = str(logging.NOTSET)
    CACHE_RANGE_IN_DAYS = 7

    # Download the webdriver
    driver_path = ChromeDriverManager(path=C.APP_FOLDER_PATH, cache_valid_range=CACHE_RANGE_IN_DAYS).install()

    # Create an options object and add
    # the desired configurations to the webdriver
    driver_options = ChromeOptions()
    driver_options.headless = headless

    # performance settings for webdriver
    driver_options.add_argument("--disable-gpu")
    driver_options.add_argument("--disable-dev-shm-usage")

    # disable logs
    driver_options.add_experimental_option(name="excludeSwitches", value=["enable-logging"])

    # configure default download directory and whether to block images
    if (not isinstance(download_path, str)):
        download_path = str(download_path)
    driver_options.add_experimental_option(
        name="prefs", 
        value={
            "download.default_directory": download_path,
            "profile.managed_default_content_settings.images": block_images,
            "download.prompt_for_download": False
        }
    )

    try:
        driver = CustomWebDriver(service=ChromeService(driver_path), options=driver_options)
    except (selenium_exceptions.WebDriverException):
        print_danger(message="\nFailed to initialise a Chrome webdriver instance.")
        print_danger(message="Please check if you have Google Chrome browser installed on your computer.")

        chrome_download_link = "https://www.google.com/chrome/"
        if (C.USER_PLATFORM == "Linux"):
            chrome_download_link += "?platform=linux"
        print_danger(message=f"Google Chrome browser download link: {chrome_download_link}\n")

    driver.set_window_size(*window_size)
    return driver

def login(current_driver: CustomWebDriver, website: str,
          login_status: dict) -> Union[None, dict, tuple[dict, bool]]:
    """Login to the both Fantia and Pixiv Fanbox.

    Args:
        current_driver (CustomWebDriver):
            The current webdriver instance to load the cookies after login.
        website (str):
            The website to login to.
        login_status (dict):
            The login status of the website to update for the user to read.

    Returns:
        - If login is successful:
            - A dictionary of cookies
            - A tuple of a dictionary of cookies and a boolean value
            for storing into the user's computer later
        - If login is unsuccessful:
            - None
    """
    if (website == "fantia"):
        cookie_name = C.FANTIA_COOKIE_NAME
        website_url = C.FANTIA_WEBSITE_URL
        login_url = C.FANTIA_LOGIN_URL
        url_verifier = C.FANTIA_VERIFY_LOGIN_URL
    elif (website == "pixiv_fanbox"):
        cookie_name = C.PIXIV_FANBOX_COOKIE_NAME
        website_url = C.PIXIV_FANBOX_WEBSITE_URL
        login_url = C.PIXIV_FANBOX_LOGIN_URL
        url_verifier = C.PIXIV_FANBOX_VERIFY_LOGIN_URL
    else:
        raise ValueError("Invalid website in login function...")

    website_name = convert_to_readable_format(website)
    login_prompt = get_input(
        input_msg=f"Do you want to login to {website_name} (Y/n)?: ",
        inputs=("y", "n"),
        default="y"
    )
    if (login_prompt == "n"):
        return

    # prepare the current webdriver instance
    # to load the cookies later after the user logins manually
    with Spinner(
        message="Prepping the current webdriver instance...",
        colour="light_yellow",
        spinner_type="arc",
        spinner_position="left"
    ):
        current_driver.get(website_url)

    driver = get_driver(download_path=".", headless=False, block_images=1, window_size=(800, 800))
    while (True):
        browser_was_closed = False
        try:
            if (driver.current_url != login_url):
                driver.get(login_url)
            time.sleep(1)

            input("Press ENTER to continue after logging in...")
            driver.get(url_verifier)

            # wait for browser to load the page
            time.sleep(1)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/head/title"))
            )

            if (driver.current_url == url_verifier):
                cookie = driver.get_cookie(cookie_name)
                driver.quit_with_message()
                break

            print_danger(message=f"Error: {website_name} login was not successful...\n")
        except (selenium_exceptions.TimeoutException):
            print_danger(
                message="Failed to load the page, " \
                        "please ensure that you have an active internet connection.\n"
            )
        except (selenium_exceptions.WebDriverException):
            print_danger(message=f"Error: {website_name} login failed as the browser was closed...\n")
            browser_was_closed = True

        retry_login = get_input(
            input_msg="Would you like to retry logging in manually? (Y/n): ",
            inputs=("y", "n"), 
            default="y"
        )
        if (retry_login == "n"):
            driver.quit_with_message()
            return

        if (browser_was_closed):
            driver = get_driver(download_path=".", headless=False, block_images=1, window_size=(800, 800))

    # a fail-safe to ensure that the
    # current driver is on the correct domain
    # before loading the obtained cookie
    if (not current_driver.current_url.startswith(website_url)):
        current_driver.get(website_url)
        time.sleep(3)

    # removes all cookies from the
    # current driver's current url domain ONLY
    # and loads the obtained cookie afterwards
    current_driver.delete_all_cookies()
    current_driver.add_cookie(cookie)

    # update the login status
    # to indicate a successful login
    login_status[website] = True

    save_cookie = get_input(
        input_msg=f"Would you like to save the {website_name} session cookie for a faster login next time? (Y/n): ",
        inputs=("y", "n"), 
        default="y"
    )
    if (save_cookie == "n"):
        return cookie

    if (C.KEY_ID_TOKEN_JSON_PATH.exists() and C.KEY_ID_TOKEN_JSON_PATH.is_file()):
        save_locally = False
    elif (C.SECRET_KEY_PATH.exists() and C.SECRET_KEY_PATH.is_file()):
        save_locally = True
    else:
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
"""     )
        save_locally = True if (save_key == "local") else False

    return (cookie, save_locally)

def logout(driver: webdriver.Chrome, website: str, login_status: dict) -> None:
    """Logout from a website.

    Args:
        driver (webdriver.Chrome):
            The current webdriver instance.
        website (str):
            The website to logout from.
        login_status (dict):
            The login status of the website to update for the user to read.

    Returns:
        None
    """
    website_name = convert_to_readable_format(website)
    confirm_logout = get_input(
        input_msg=f"Do you want to logout from {website_name} (y/N)?: ",
        inputs=("y", "n"),
        default="n"
    )
    if (confirm_logout == "n"):
        return

    if (website == "fantia"):
        website_url = C.FANTIA_WEBSITE_URL
    elif (website == "pixiv_fanbox"):
        website_url = C.PIXIV_FANBOX_WEBSITE_URL
    else:
        raise ValueError("Invalid website in logout function...")

    with Spinner(
        message=f"Logging out from {website_name}...",
        colour="light_yellow",
        spinner_type="arc",
        spinner_position="left"
    ):
        # a fail-safe to ensure that the
        # current driver is on the correct domain
        # before logging out
        if (not driver.current_url.startswith(website_url)):
            driver.get(website_url)
            time.sleep(3)

        # removes all cookies from the
        # current driver's current url domain ONLY
        driver.delete_all_cookies()
        login_status[website] = False

def load_cookie_to_webdriver(driver: webdriver.Chrome, website: str, login_status: dict, cookie: dict) -> None:
    """Loads the cookies to the webdriver instance (which takes about 6 seconds).

    Args:
        driver (webdriver.Chrome):
            The webdriver instance to load the cookies to.
        website (str):
            The website to load the cookies to.
        login_status (dict):
            The login status of the website to update for the user to read.
        cookie (dict):
            The cookie to load to the webdriver instance.

    Returns:
        None
    """
    if (website == "fantia"):
        website_url = C.FANTIA_WEBSITE_URL
        verify_url = C.FANTIA_VERIFY_LOGIN_URL
    elif (website == "pixiv_fanbox"):
        website_url = C.PIXIV_FANBOX_WEBSITE_URL
        verify_url = C.PIXIV_FANBOX_VERIFY_LOGIN_URL
    else:
        raise ValueError("Invalid website in load_cookie_to_webdriver function...")

    if (isinstance(cookie, dict)):
        # Add cookies to the driver
        driver.get(website_url)
        time.sleep(3)
        driver.delete_all_cookies()
        driver.add_cookie(cookie)

        # verify if the cookies are valid
        driver.get(verify_url)
        time.sleep(3)
        if (driver.current_url != verify_url):
            driver.delete_all_cookies()
        else:
            login_status[website] = True
    else:
        logger.warning(f"Invalid cookie type, '{type(cookie)}', for {website}...")

# test codes
if (__name__ == "__main__"):
    with get_driver(".") as driver:
        driver.get("https://www.google.com")
        print(driver.title)
        # print(driver.page_source)