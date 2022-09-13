# import third-party libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# import Python's standard libraries
import time
import logging
import pathlib
from typing import Optional, Union
from os import environ

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from functional import print_danger, get_input
else:
    from .constants import CONSTANTS as C
    from .functional import print_danger, get_input

def get_driver(
    download_path: Union[pathlib.Path, str],
    headless: Optional[bool] = True, 
    block_images: Optional[int] = 2, 
    window_size: tuple[int, int] = (1920, 1080)) -> webdriver.Chrome:
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
        A Chrome webdriver instance.
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
        driver = webdriver.Chrome(service=ChromeService(driver_path), options=driver_options)
    except (selenium_exceptions.WebDriverException):
        print_danger(message="\nFailed to initialise a Chrome webdriver instance.")
        print_danger(message="Please check if you have Google Chrome browser installed on your computer.")

        chrome_download_link = "https://www.google.com/chrome/"
        if (C.USER_PLATFORM == "Linux"):
            chrome_download_link += "?platform=linux"
        print_danger(message=f"Google Chrome browser download link: {chrome_download_link}\n")

    driver.set_window_size(*window_size)
    return driver

def login(current_driver: webdriver.Chrome, website: str, 
          driver: Optional[webdriver.Chrome] = None) -> Union[None, dict, tuple[dict, bool]]:
    """Login to the both Fantia and Pixiv Fanbox.

    Args:
        current_driver (webdriver.Chrome):
            The current webdriver instance to load the cookies after login.
        website (str):
            The website to login to.
        driver (webdriver.Chrome, optional):
            The webdriver instance to use for manual login.

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
    elif (website == "pixiv"):
        cookie_name = C.PIXIV_FANBOX_COOKIE_NAME
        website_url = C.PIXIV_FANBOX_WEBSITE_URL
        login_url = C.PIXIV_FANBOX_LOGIN_URL
        url_verifier = C.PIXIV_FANBOX_VERIFY_LOGIN_URL
    else:
        raise ValueError("Invalid website in login function...")

    login_prompt = get_input(
            input_msg="Do you want to login to {website} (Y/n)?: ".format(
                website="Fantia" if (website == "fantia") else "Pixiv Fanbox"
            ),
            inputs=("y", "n"),
            default="y"
    )
    if (login_prompt == "n"):
        return

    # prepare the current webdriver instance
    # to load the cookies later after the user logins manually
    current_driver.get(website_url)

    generated_new_driver = False
    if (driver is None):
        driver = get_driver(download_path=".", headless=False, block_images=1, window_size=(800, 800))
        generated_new_driver = True

    while (1):
        if (driver.current_url != login_url):
            driver.get(login_url)
        time.sleep(1)
        input("Press ENTER to continue after logging in...")

        try:
            driver.get(url_verifier)

            # wait for browser to load the page
            time.sleep(1)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/head/title"))
            )
            if (driver.current_url == url_verifier):
                break
            print_danger(message=f"Error: {website.title()} login failed...")
        except (selenium_exceptions.TimeoutException):
            print_danger(
                message="Failed to load the page, please ensure that you have an active internet connection."
            )
        except (selenium_exceptions.webdriverException):
            print_danger(message="Note: Please do not close the browser!")

        retry_login = get_input(
            input_msg="Would you like to retry logging in manually? (Y/n): ",
            inputs=("y", "n"), 
            default="y"
        )
        if (retry_login == "n"):
            if (generated_new_driver):
                driver.quit()
            return

    cookie = driver.get_cookie(cookie_name)
    if (generated_new_driver):
        driver.quit()

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

    save_cookie = get_input(
        input_msg=f"Would you like to save the {website.title()} session cookie for a faster login next time? (Y/n): ",
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

# test codes
if (__name__ == "__main__"):
    with get_driver(".") as driver:
        driver.get("https://www.google.com")
        print(driver.title)
        print(driver.page_source)