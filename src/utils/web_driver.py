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
import asyncio
from os import environ
from typing import Optional, Union, Type

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
    from errors import ChangedHTMLStructureError
    from logger import logger
    from spinner import Spinner
    from user_data import load_cookies
    from download import *
    from functional import print_danger, get_input, save_key_prompt, \
                           website_to_readable_format, get_user_urls, get_user_download_choices
else:
    from .constants import CONSTANTS as C
    from .errors import ChangedHTMLStructureError
    from .logger import logger
    from .spinner import Spinner
    from .user_data import load_cookies
    from .download import *
    from .functional import print_danger, get_input, save_key_prompt, \
                            website_to_readable_format, get_user_urls, get_user_download_choices

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
    message="Initialising a new webdriver instance...", 
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
    # Disable webdriver manager's logs from displaying
    environ["WDM_LOG_LEVEL"] = str(logging.NOTSET)

    # Download the webdriver
    driver_path = ChromeDriverManager(
        path=C.DRIVER_FOLDER_PATH,
        cache_valid_range=C.DRIVER_CACHE_RANGE
    ).install()

    # Create an options object and add
    # the desired configurations to the webdriver
    driver_options = ChromeOptions()
    driver_options.headless = headless
    driver_options.add_argument(f"user-agent={C.USER_AGENT}")

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

def wait_for_page_load(driver: webdriver.Chrome, timeout: Optional[int] = 15) -> None:
    """Wait for a page to load.

    Args:
        driver (webdriver.Chrome): 
            The webdriver instance.
        timeout (int, optional):
            The maximum time to wait for the page to load. Defaults to 15.

    Returns:
        None

    Raises:
        selenium_exceptions.TimeoutException:
            If the page does not load within the specified timeout.
    """
    time.sleep(0.5)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "/html/head/title"))
    )

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
        cookie_exists = C.FANTIA_COOKIE_PATH.exists() and C.FANTIA_COOKIE_PATH.is_file()
    elif (website == "pixiv_fanbox"):
        cookie_name = C.PIXIV_FANBOX_COOKIE_NAME
        website_url = C.PIXIV_FANBOX_WEBSITE_URL
        login_url = C.PIXIV_FANBOX_LOGIN_URL
        url_verifier = C.PIXIV_FANBOX_VERIFY_LOGIN_URL
        cookie_exists = C.PIXIV_FANBOX_COOKIE_PATH.exists() and C.PIXIV_FANBOX_COOKIE_PATH.is_file()
    else:
        raise ValueError("Invalid website in login function...")

    website_name = website_to_readable_format(website)
    login_prompt = get_input(
        input_msg=f"\nDo you want to login to {website_name} (Y/n)?: ",
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

            try:
                input("Press ENTER to continue after logging in...")
            except (EOFError):
                continue
            except (KeyboardInterrupt):
                driver.quit_with_message()
                print_danger(message="Cancelled login...")
                return

            with Spinner(
                message="Verifying login...",
                colour="light_yellow",
                spinner_type="arc",
                spinner_position="left",
                completion_msg="Login verified!"
            ):
                driver.get(url_verifier)
                wait_for_page_load(driver)

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
            input_msg=f"Would you like to retry logging in manually to {website_name}? (Y/n): ",
            inputs=("y", "n"), 
            default="y"
        )
        if (retry_login == "n"):
            driver.quit_with_message()
            return

        if (browser_was_closed):
            driver = get_driver(download_path=".", headless=False, block_images=1, window_size=(800, 800))

    # removes all cookies from the
    # current driver's current url domain ONLY
    # and loads the obtained cookie afterwards
    current_driver.delete_all_cookies()
    current_driver.add_cookie(cookie)

    # update the login status
    # to indicate a successful login
    login_status[website] = cookie

    save_cookie = get_input(
        input_msg="Would you like to {action} the {website_name} session cookie {preposition} your computer for a faster login next time? (Y/n): ".format(
            action="save" if (not cookie_exists) else "overwrite",
            website_name=website_name,
            preposition="to" if (not cookie_exists) else "on"
        ),
        inputs=("y", "n"), 
        default="y"
    )
    if (save_cookie == "n"):
        return cookie

    save_key_locally = save_key_prompt()
    return (cookie, website, save_key_locally)

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
    website_name = website_to_readable_format(website)
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
        # ensure that the current driver 
        # is on the correct domain before deleting all cookies
        timeout = False
        if (not driver.current_url.startswith(website_url)):
            driver.get(website_url)
            try:
                wait_for_page_load(driver)
            except (selenium_exceptions.TimeoutException):
                logger.warning(f"The webdriver timed out while trying to logout from {website}.")
                timeout = True

        if (not timeout):
            # removes all cookies from the
            # current driver's current url domain ONLY
            driver.delete_all_cookies()
            login_status[website] = False

    if (timeout):
        print_danger(f"Timeout Error: Failed to logout from {website_name}...\n")

@Spinner(
    message="Loading cookies if valid...",
    colour="light_yellow",
    spinner_position="left",
    spinner_type="arc"
)
def load_cookies_to_webdriver(driver: webdriver.Chrome, login_status: dict) -> None:
    """Decrypts the user's saved encrypted cookie and loads the cookies to the webdriver instance.

    Args:
        driver (webdriver.Chrome):
            The webdriver instance to load the cookies to.
        login_status (dict):
            The login status of the website to update for the user to read.

    Returns:
        None
    """
    # Load the encrypted cookies from the user's computer
    loaded_cookies = load_cookies(*["fantia", "pixiv_fanbox"])

    # process the loaded cookies
    for thread in loaded_cookies:
        cookie = thread.result
        if (cookie is None):
            continue

        website = thread.website
        if (website == "fantia"):
            website_url = C.FANTIA_WEBSITE_URL
            verify_url = C.FANTIA_VERIFY_LOGIN_URL
        elif (website == "pixiv_fanbox"):
            website_url = C.PIXIV_FANBOX_WEBSITE_URL
            verify_url = C.PIXIV_FANBOX_VERIFY_LOGIN_URL
        else:
            raise ValueError("Invalid website in load_cookie_to_webdriver function...")

        # Add cookies to the driver
        driver.get(website_url)
        try:
            wait_for_page_load(driver)

            driver.delete_all_cookies()
            driver.add_cookie(cookie)

            # verify if the cookies are valid
            driver.get(verify_url)
            wait_for_page_load(driver)
        except (selenium_exceptions.TimeoutException):
            logger.warning(
                f"The webdriver timed out while trying to load the user's {thread.readable_website} cookie."
            )
            return

        if (driver.current_url != verify_url):
            driver.delete_all_cookies()
            time.sleep(0.5)
        else:
            login_status[website] = cookie

def get_creator_posts(driver: webdriver.Chrome, url: str, website: str) -> list[str]:
    """Gets the URL(s) of the creator's posts.

    Args:
        driver (webdriver.Chrome):
            The webdriver instance to use.
        url (str):
            The url of the creator's page to get the post(s) from.
        website (str):
            The website to download the post from.

    Returns:
        A list of every posts' URL(s) in the given URL.
    """
    driver.get(url)
    wait_for_page_load(driver)

    if (website == "fantia"):
        post_xpath = "//a[@class='link-block']"
    elif (website == "pixiv_fanbox"):
        post_xpath = "//a[starts-with(@href, '/posts/')]"
    else:
        raise ValueError("Invalid website in get_creator_posts function...")

    try:
        posts = driver.find_elements(By.XPATH, post_xpath)
    except (selenium_exceptions.NoSuchElementException):
        logger.warning(f"No posts found for {url}...\n\n{driver.page_source}")
        raise ChangedHTMLStructureError(
            "Please raise an issue on GitHub with your log files as " \
            f"{website_to_readable_format(website)}'s HTML structure has possibly changed."
        )

    post_urls = [post.get_attribute("href") for post in posts]
    if (website != "pixiv_fanbox"):
        return post_urls

    # Since the xpath will return two exact same links for a post
    # (One for the image anchor and another for the card anchor),
    # Remove the duplicate links 
    # with the order of the links being preserved.
    return list(dict.fromkeys(post_urls))

async def execute_download_process(website: str, creator_page: bool, download_path: str,
                             driver: webdriver.Chrome, login_status: dict) -> None:
    """Executes the download process for the given website.

    Args:
        website (str): 
            The website the user wishes to download from.
        creator_page (bool): 
            Whether the user wishes to download from a creator's page.
        download_path (str):
            The path to the download directory loaded from the configs file.
        driver (webdriver.Chrome): 
            The webdriver instance to use.
        login_status (dict):
            The current login status of the user to retrieve the 
            user's cookies, if any, to use to get access to paywall restricted posts.

    Returns:
        None
    """
    urls_arr = get_user_urls(website=website, creator_page=creator_page)
    if (urls_arr is None):
        return

    download_flags = get_user_download_choices(website)
    if (download_flags is None):
        return
    print()

    if (creator_page):
        with Spinner(
            message="Retrieving post(s) from creator's page...",
            colour="light_yellow",
            spinner_position="left",
            spinner_type="arc"
        ):
            posts_url_arr = []
            for creator_page_url in urls_arr:
                posts_url_arr.extend(
                    get_creator_posts(driver=driver, url=creator_page_url, website=website)
                )
            urls_arr = posts_url_arr

    urls_to_download: list[tuple[pathlib.Path, list[tuple[str, str]]]] = []
    cookie = format_cookie_to_cookiejar(
        login_status.get(website)
    )
    readable_website_name = website_to_readable_format(website)
    download_path = pathlib.Path(download_path).joinpath(
        readable_website_name.replace(" ", "-", 1)
    )
    base_spinner_msg = " ".join([
        "Retrieved and processed {progress}",
        f"out of {len(urls_arr)}",
        "posts'" if (len(urls_arr) > 1) else "post's",
        f"content details from {readable_website_name}'s API..."
    ])
    with Spinner(
        message=base_spinner_msg.format(
            progress=0
        ),
        colour="light_yellow",
        spinner_position="left",
        spinner_type="arc",
        completion_msg=f"Finished processing all {len(urls_arr)} post(s)'s JSON response(s) from {readable_website_name}'s API!",
        cancelled_msg=f"Download process for {readable_website_name} has been cancelled!",
    ) as spinner:
        json_to_process = []
        api_request_tasks = set()
        finished_api_requests = 0
        for post_url in urls_arr:
            if (len(api_request_tasks) >= C.API_MAX_CONCURRENT_REQUESTS):
                # Wait for some API requests to finish before adding a new task
                done, api_request_tasks = await asyncio.wait(
                    api_request_tasks,
                    return_when=asyncio.FIRST_COMPLETED
                )
                finished_api_requests += len(done)
                spinner.message = base_spinner_msg.format(
                    progress=finished_api_requests
                )

            post_id = post_url.rsplit(sep="/", maxsplit=1)[1]
            api_request_tasks.add(
                asyncio.create_task(
                    get_post_details(
                        cookie=cookie,
                        post_id=post_id,
                        website=website,
                        post_url=post_url,
                        json_arr=json_to_process,
                        download_path=download_path,
                    )
                )
            )

        # Wait for any remaining downloads to finish
        if (api_request_tasks):
            await asyncio.wait(api_request_tasks)

        for json_response in json_to_process:
            if (website == "fantia"):
                processed_json = process_fantia_json(
                    json_response=json_response,
                    download_path=download_path,
                    download_flags=download_flags
                )
            elif (website == "pixiv_fanbox"):
                processed_json = process_pixiv_fanbox_json(
                    json_response=json_response,
                    download_path=download_path,
                    download_flags=download_flags
                )
            else:
                raise ValueError(f"Invalid website, {website}, in execute_download_process function...")

            if (processed_json is not None):
                urls_to_download.append(processed_json)

    # Calculate the total number of urls to download
    total_urls_to_download = 0
    for _, post_content_urls in urls_to_download:
        for _, content_type in post_content_urls:
            if (content_type != C.GDRIVE_FILE):
                total_urls_to_download += 1

    failed_downloads_arr = []
    gdrive_urls_arr: list[str] = []
    max_concurrent_downloads = C.MAX_CONCURRENT_DOWNLOADS_TABLE.get(website, 1)
    base_spinner_msg = " ".join([
        "Downloaded {progress} out of",
        f"{total_urls_to_download} URL(s) from {len(urls_arr)} posts on {readable_website_name}..."
    ])
    with Spinner(
        message=base_spinner_msg.format(
            progress=0,
            website=readable_website_name
        ),
        colour="light_yellow",
        spinner_position="left",
        spinner_type="arc",
        completion_msg=f"Finished downloading all {total_urls_to_download} URL(s) from {len(urls_arr)} post(s) on {readable_website_name}!",
        cancelled_msg=f"Download process for {readable_website_name} has been cancelled!"
    ) as spinner:
        download_tasks = set()
        finished_downloads = 0
        for post_folder_path, post_content_urls_info in urls_to_download:
            for content_url_info in post_content_urls_info:
                if (content_url_info[1] == C.GDRIVE_FILE):
                    gdrive_urls_arr.append(content_url_info[0])
                    continue

                if (len(download_tasks) >= max_concurrent_downloads):
                    # Wait for some download to finish before adding a new task
                    done, download_tasks = await asyncio.wait(
                        download_tasks,
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    finished_downloads += len(done)
                    spinner.message = base_spinner_msg.format(
                        progress=finished_downloads
                    )

                download_tasks.add(
                    asyncio.create_task(
                        async_download_file(
                            url_info=content_url_info,
                            folder_path=post_folder_path,
                            website=website,
                            cookie=cookie,
                            failed_downloads_arr=failed_downloads_arr
                        )
                    )
                )

        # Wait for any remaining downloads to finish
        if (download_tasks):
            await asyncio.wait(download_tasks)

    for url_info, website, folder_path in failed_downloads_arr:
        log_failed_downloads(
            url_info=url_info, 
            website=website,
            folder_path=folder_path
        )
    if (failed_downloads_arr):
        print_danger(
            f"{len(failed_downloads_arr)} download(s) failed. "
            "Please check the generated logs in each of the post's folders."
        )

    # TODO: finish GDrive downloads
    failed_downloads_arr = []
    for gdrive_url in gdrive_urls_arr:
        pass

# test codes
if (__name__ == "__main__"):
    async def test(driver: webdriver.Chrome) -> None:
        await execute_download_process(
            website="pixiv_fanbox",
            creator_page=True,
            driver=driver,
            download_path=pathlib.Path(__file__).parent.absolute(),
            login_status={
                "pixiv_fanbox":
                    None,
                "fantia":
                    None
            }
        )
    with get_driver(".") as driver:
        asyncio.run(test(driver))