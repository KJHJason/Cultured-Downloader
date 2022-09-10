# import third-party libraries
from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# import Python's standard libraries
import logging
import pathlib
from typing import Optional, Union
from os import environ

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from functional import print_danger
else:
    from .constants import CONSTANTS as C
    from .functional import print_danger

def get_driver(
    download_path: Union[pathlib.Path, str],
    headless: Optional[bool] = True, 
    block_images: Optional[bool] = True, 
    window_size: tuple[int, int] = (1920, 1080)) -> webdriver.Chrome:
    """Get a Chrome webdriver instance.

    Args:
        download_path (Union[pathlib.Path, str]): 
            The path to the download directory.
        headless (bool, optional): 
            Whether to run the browser in headless mode. Defaults to True.
        block_images (bool, optional):
            Whether to block images from loading. Defaults to True.
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

# test codes
if (__name__ == "__main__"):
    with get_driver(".") as driver:
        driver.get("https://www.google.com")
        print(driver.title)
        print(driver.page_source)