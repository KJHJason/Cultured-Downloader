# Import Standard Library, os, to close the program
from os import _exit as osExit

try:
    import Header
    __author__ = Header.__author__
    __copyright__ = Header.__copyright__
    __license__ = Header.__license__
    __version__ = Header.__version__
except ImportError:
    print("Could not import Header module/Header モジュールのインポートに失敗しました...")
    input("Please enter any key to exit/何か入力すると終了します...")
    osExit()

# Import Third-party Libraries
try:
    import requests, dill
    from colorama import init as coloramaInit
    from colorama import Style
    from colorama import Fore as F
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as chromeService
    from selenium.webdriver.chrome.options import Options as chromeOptions
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.service import Service as edgeService
    from selenium.webdriver.edge.options import Options as edgeOptions
    from Crypto.Cipher import ChaCha20_Poly1305 as Cha
    from Crypto.Random import get_random_bytes
except (ImportError, ModuleNotFoundError):
    print("Failed to import third-party libraries/サードパーティーライブラリのインポートに失敗しました...")
    input("Please enter any key to exit/何か入力すると終了します...")
    osExit()

# Import Standard Libraries
try:
    import pathlib, json, sys, logging, webbrowser, re, platform
    from urllib.parse import urlparse
    from json.decoder import JSONDecodeError
    from time import sleep
    from datetime import datetime
    from shutil import rmtree, copyfileobj, move
    from base64 import b64encode, b64decode
except (ImportError, ModuleNotFoundError):
    print("Failed to import standard libraries/標準ライブラリのインポートに失敗しました...")
    print("Please use Python 3.8.X and above/Python 3.8.X以降をご使用ください。")
    input("Please enter any key to exit/何か入力すると終了します...")
    osExit()

# Importing my Python Files as Modules
try:
    from EncryptedData import EncryptedData
except (ImportError, ModuleNotFoundError):
    print("Failed to import EncryptedData module/EncryptedData モジュールのインポートに失敗しました...")
    input("Please enter any key to exit/何か入力すると終了します...")
    osExit()

"""--------------------------- Custom Errors ---------------------------"""

class DecryptError(Exception):
    """
    Raised when the program is unable to decrypt an encrypted value.
    """
    pass

class EncryptionKeyError(Exception):
    """
    Raised when the program is unable to set the key for the cipher variable.

    Usually this happens when the key is not 32 bytes long.
    """
    pass

class SessionError(Exception):
    """
    Raised when the program is to retrieve the session ID from the cookies of pixiv and Fantia

    Usually this happens when the cookies are not valid and manually placed by the user.
    """
    pass


"""--------------------------- End of Custom Errors ---------------------------"""

"""--------------------------- Config Codes ---------------------------"""

def shutdown():
    """
    Closes the main global variable driver's webdriver session prints out some messages for the user.
    """
    if lang == "en":
        print(f"{F.LIGHTYELLOW_EX}Thank you for using Cultured Downloader.{END}")
        input("Please enter any key to exit...")
    elif lang == "jp":
        print(f"{F.LIGHTYELLOW_EX}Cultured Downloaderをご利用いただきありがとうございます。{END}")
        input("何か入力すると終了します。。。")
    
    if lang == "en": print(f"{F.RED}Exiting...{END}")
    elif lang == "jp": print(f"{F.RED}終了しています...{END}")

    try: driver.quit()
    except: pass

    osExit(0)

def print_error_log_notification():
    """
    Used for alerting the user of where the log file is located at and to report this bug to the developer.
    """
    logFolderPath = get_saved_config_data_folder().joinpath("logs")
    print(f"\n{F.RED}Unknown Error Occurred/不明なエラーが発生した{END}")
    print(f"{F.RED}Please provide the developer with a error text file generated in {logFolderPath}\n{logFolderPath}に生成されたエラーテキストファイルを開発者に提供してください。\n{END}")
    try: driver.quit()
    except: pass

def log_error():
    """
    Used for writing the error to a log file usually located in the Cultured Downloader folder in the AppData LocalLow folder.
    """
    filePath = get_saved_config_data_folder().joinpath("logs")
    filePath.mkdir(parents=True, exist_ok=True)

    fileName = "".join([f"error-v{__version__}-", datetime.now().strftime("%d-%m-%Y"), ".log"])
    fullFilePath = filePath.joinpath(fileName)
    
    if not fullFilePath.is_file():
        with open(fullFilePath, "w") as f:
            f.write(f"Cultured Downloader v{__version__ } Error Logs\n\n")
    else:
        with open(fullFilePath, "a") as f:
            f.write("\n")

    logging.basicConfig(filename=fullFilePath, filemode="a", format="%(asctime)s - %(message)s")
    logging.error("Error Details: ", exc_info=True)

def error_shutdown(**errorMessages):
    """
    Params:
    - en for English error messages
    - jp for Japanese error messages

    Used for printing out error messages defined in the params before shutting down the program when an error occurs.
    """
    if "en" in errorMessages and lang == "en":
        enErrorMessages = errorMessages.get("en")
        if type(enErrorMessages) == tuple:
            for line in enErrorMessages:
                print(f"{F.RED}{line}{END}")
        else: print(f"{F.RED}{enErrorMessages}{END}")
        input("Please enter any key to exit...")
        print("Thank you for your understanding.")
        
    elif "jp" in errorMessages and lang == "jp":
        jpErrorMessages = errorMessages.get("jp")
        if type(jpErrorMessages) == tuple:
            for line in jpErrorMessages:
                print(f"{F.RED}{line}{END}")
        else: print(f"{F.RED}{jpErrorMessages}{END}")
        input("何か入力すると終了します。。。")
        print("ご理解頂き誠にありがとうございます。")

    try: driver.quit()
    except: pass
    log_error()
    sleep(2)
    raise SystemExit

def print_in_both_en_jp(**message):
    """
    Used for printing either English or Japanese messages.

    Params:
    - en for English message
    - jp for Japanese message

    If the global variable lang is not defined, it will print both English and Japanese messages.
    """
    enMessages = message.get("en")
    jpMessages = message.get("jp")

    if lang == "en":
        if type(enMessages) == tuple:
            for enLine in enMessages:
                print(enLine)
        else: print(enMessages)
    elif lang == "jp":
        if type(jpMessages) == tuple:
            for jpLine in jpMessages:
                print(jpLine)
        else: print(jpMessages)
    else:
        if type(enMessages) == tuple:
            for enLine in enMessages:
                print(enLine)
        else: print(enMessages)
        if type(jpMessages) == tuple:
            for jpLine in jpMessages:
                print(jpLine)
        else: print(jpMessages)

def get_input_from_user(**kwargs):
    """
    Returns user's input based on the defined command paramater without 
    letting the user enter anything else besides the defined command parameter.

    Params:
    - prompt: The prompt to be displayed to the user.
    - prints: The message to be printed to the user.
    - command: The input to be accepted by the program.
    - warning: Used for displaying a custom error message.

    Defaults:
    - command: None but must be defined at all time as it will raise an Exception if not defined
    - prompt: "", an input without any prompt
    - prints: None, will not print out any messages
    - warning: None, will not display any error messages
    """
    prints = kwargs.get("prints")

    prompt = kwargs.get("prompt")
    if prompt == None: prompt = ""

    commands = kwargs.get("command")
    if commands == None: raise Exception("command parameter must be defined in the function, get_input_from_user")

    warning = kwargs.get("warning")

    if prints != None:
        if type(prints) == tuple:
            for line in prints:
                print(f"{F.LIGHTYELLOW_EX}{line}{END}")
        else: print(f"{F.LIGHTYELLOW_EX}{prints}{END}")

    while True:
        userInput = input(prompt).lower().strip()
        if userInput in commands: return userInput
        else: 
            try:
                if warning and lang == "en": print(f"{F.RED}Error: {warning}.{END}")
                elif warning and lang == "jp": print(f"{F.RED}エラー: {warning}{END}")
                else: 
                    if lang == "en": commandToPrint = " or ".join(commands)
                    else: commandToPrint = "または".join(commands)
                    print_in_both_en_jp(
                        en=(f"{F.RED}Error: Invalid input. Please enter {commandToPrint}.{END}"),
                        jp=(f"{F.RED}エラー: 不正な入力です。{commandToPrint}を入力してください。{END}")
                    )
            except NameError:
                # if lang is not defined yet
                commandToPrintEn = " or ".join(commands)
                commandToPrintJp = "または".join(commands)
                if warning: 
                    print(f"{F.RED}Error: Invalid language prefix entered.{END}")
                    print(f"{F.RED}エラー: 入力された言語プレフィックスが無効です。{END}")
                else: 
                    print(f"{F.RED}Error: Invalid input. Please enter {commandToPrintEn}.{END}"),
                    print(f"{F.RED}エラー: 不正な入力です。{commandToPrintJp}を入力してください。{END}")

def check_if_json_file_exists():
    """
    Checks if the json files exist in the Cultured Downloader folder in the AppData LocalLow folder.

    If it exist, it will try to load it and if there is a JSONDecodeError, it will dump an empty dictionary as a placeholder.

    Otherwise, it will create a new config.json file and dump an empty dictionary as a placeholder.
    """
    jsonFolderPath = appPath.joinpath("configs")
    jsonFolderPath.mkdir(parents=True, exist_ok=True)
    if not jsonPath.is_file():
        print(f"{F.RED}Error: config.json does not exist.{END}", f"\n{F.LIGHTYELLOW_EX}Creating config.json file...{END}"),
        print(f"{F.RED}エラー: config.jsonが存在しません。{END}", f"\n{F.LIGHTYELLOW_EX}config.jsonファイルを作成しています...{END}")
        
        with open(jsonPath, "w") as f:
            json.dump({}, f)
    else: 
        try:
            with open(jsonPath, "r") as f:
                json.load(f)
        except JSONDecodeError:
            print(f"{F.RED}Error: config.json is corrupted.{END}")
            print(f"{F.LIGHTYELLOW_EX}Resetting config.json file...{END}")
            print(f"{F.RED}エラー: config.jsonが壊れています。{END}")
            print(f"{F.LIGHTYELLOW_EX}config.jsonファイルをリセットします...{END}\n")
            with open(jsonPath, "w") as f:
                json.dump({}, f)

        print(f"{F.LIGHTYELLOW_EX}Loading configurations from config.json...{END}")
        print(f"{F.LIGHTYELLOW_EX}config.jsonから設定を読み込みます...{END}")

def get_saved_config_data_folder():
    """
    Returns a pathlib Path object of the saved config data folder according to the OS platform.

    Supported OS: Windows, Linux, macOS
    """
    osPlatform = platform.system()
    if osPlatform == "Windows":
        dataDirectory = pathlib.Path.home().joinpath("AppData/Roaming/CulturedDownloader")
    elif osPlatform == "Linux":
        dataDirectory = pathlib.Path.home().joinpath(".config/CulturedDownloader")
    elif osPlatform == "Darwin": # macOS
        dataDirectory = pathlib.Path.home().joinpath("Library/Preferences/CulturedDownloader")
    else:
        print(f"{F.RED}Your OS is not supported/お使いのOSはサポートされていません...{END}")
        print(f"{F.RED}Supported OS/サポートされているOS: Windows, Linux, macOS...{END}")
        input("Please enter any key to exit/何か入力すると終了します...")
        osExit(1)

    dataDirectory.mkdir(parents=True, exist_ok=True)
    return dataDirectory

def get_driver(browserType, **additionalOptions):
    """
    Requires one argument to be defined:: 
    - "chrome"
    - "edge"

    Optional params:
    - headless --> True or False
    - blockImg --> a number

    For numbers, use the definition below:
    - 0 is default
    - 1 is to allow
    - 2 is to block
    """
    headlessOption = additionalOptions.get("headless")
    if headlessOption == None: headlessOption = True # set to True by default

    blockImages = additionalOptions.get("blockImg")
    if blockImages == None: blockImages = 2 # set to 2 by default to block all images

    print_in_both_en_jp(
        en=(f"\n{F.LIGHTYELLOW_EX}Initialising Browser...{END}"),
        jp=(f"\n{F.LIGHTYELLOW_EX}ブラウザの初期化中です...{END}")
    )
    if browserType == "chrome":
        #minimise the browser window and hides unnecessary text output
        cOptions = chromeOptions()
        cOptions.headless = headlessOption
        cOptions.add_argument("--log-level=3")
        cOptions.add_argument("--disable-gpu")
        cOptions.add_argument("--disable-dev-shm-usage") # from https://stackoverflow.com/questions/62898801/selenium-headless-chrome-runs-much-slower

        # for checking response code
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        # change default download location
        cOptions.add_experimental_option("prefs", {
            "download.default_directory": str(browserDownloadLocation),
            "profile.managed_default_content_settings.images": blockImages
        })

        # auto downloads chromedriver.exe
        gService = chromeService(ChromeDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Chrome(service=gService, options=cOptions, desired_capabilities=capabilities)
    elif browserType == "edge":
        # minimise the browser window and hides unnecessary text output
        eOptions = edgeOptions()
        eOptions.headless = headlessOption
        eOptions.use_chromium = True
        eOptions.add_argument("--log-level=3")
        eOptions.add_argument("--disable-gpu")
        eOptions.add_argument("--disable-dev-shm-usage") # from https://stackoverflow.com/questions/62898801/selenium-headless-chrome-runs-much-slower

        # for checking response code
        capabilities = DesiredCapabilities.EDGE.copy()
        capabilities["ms:loggingPrefs"] = {"performance": "ALL"}

        # change default download location
        eOptions.add_experimental_option("prefs", {
            "download.default_directory": str(browserDownloadLocation),
            "profile.managed_default_content_settings.images": blockImages
        })

        # auto downloads msedgedriver.exe
        eService = edgeService(EdgeChromiumDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Edge(service=eService, options=eOptions, capabilities=capabilities)
    else:
        with open(jsonPath, "r") as f:
            config = json.load(f)
        
        config["Browser"] = ""
        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)

        error_shutdown(
            en=("Error: Unknown browser type in config.json", "Please restart this program."),
            jap=("エラー： config.jsonに不明なブラウザタイプがある。", "このプログラムを再起動してください。")
        )

    driver.set_window_size(1280, 720)
    return driver

def check_browser_config():
    """
    Checks if config.json has the necessary information for loading in the user's selected default browser.

    If it doesn not have the necessary information, it will return None.

    Otherwise, it will return the browser type which will usually be either "chrome" or "edge".
    """
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        browserType = config["Browser"]
        if browserType == "": return None
        else: return browserType
    except KeyError:
        browserDict = {"Browser": ""}
        config.update(browserDict)
        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)
        return None
    except:
        error_shutdown(
            en=("Unexpected Error: Error when trying to check browser config.", "Please report this error to the developer."),
            jap=("予期せぬエラー： ブラウザの設定を確認しようとするとエラーになる。", "このエラーを開発者に報告してください。")
        )

def get_user_browser_preference():
    """
    To get the user's preferred browser which will either return "chrome" or "edge"
    """
    if lang == "en":
        inputPrompt = "Select a browser from the available options: "
        printsPrompt = ("What browser would you like to use?", "Available browsers: Chrome, Edge.")
        warningPrompt = "Invalid browser, please enter a browser from the available browsers."
    else:
        inputPrompt = "利用可能なオプションからブラウザを選択します： "
        printsPrompt = ("どのブラウザを使用しますか？", "使用可能なブラウザ： Chrome, Edge。")
        warningPrompt = "不正なブラウザです。使用可能なブラウザから選んでください。"

    selectedBrowser = get_input_from_user(prompt=inputPrompt, command=("chrome", "edge"), prints=printsPrompt, warning=warningPrompt)
    return selectedBrowser

def get_browser_preferences():
    """
    To get the user's default browser in the config.json...
    
    This function will check the config.json file if the user has defined their preferred browser in the json file by calling the function check_browser_config.

    Hence, in any event that the function check_browser_config() returns a string and not None and if the returned string from check_browser_config() is not "chrome" or "edge", the user might have entered manually to config.json.

    However, the function get_driver(browserType) will do the necessary checks and change the config.json file browser data to an empty string if it's not "chrome" or "edge".

    Otherwise, if the user has not set a default browser, it will ask the user to select a browser and prompt them 
    if they want to save their preferred browser type to config.json for future runs.

    This function will return the browser type which will usually be either "chrome" or "edge".
    """
    loadBrowser = check_browser_config()
    if loadBrowser == None:
        selectedBrowser = get_user_browser_preference()

        if lang == "en": browserPrompt = "Would you like to automatically use this browser upon running this program again? (y/n): "
        else: browserPrompt = "本プログラムの再実行時に、自動的にこのブラウザを使用しますか？ (y/n)： "

        saveBrowser = get_input_from_user(prompt=browserPrompt, command=("y", "n"))
        
        if saveBrowser == "y": save_browser_config(selectedBrowser)

        return selectedBrowser
    else: 
        return loadBrowser

def save_browser_config(selectedBrowser):
    """
    To save the user's preferred browser to config.json.

    Requires one argument to be defined:
    - the browser type which will usually be either "chrome" or "edge".
    """
    with open(jsonPath, "r") as f:
        config = json.load(f)
    config["Browser"] = selectedBrowser
    with open(jsonPath, "w") as f:
        json.dump(config, f, indent=4)
    print_in_both_en_jp(
        en=(f"{F.GREEN}{selectedBrowser.title()} will be automatically loaded next time!{END}"),
        jp=(f"{F.GREEN}{selectedBrowser.title()}は次回起動時に自動的にロードされます！{END}")
    )

def set_lang(config):
    """
    Saves the user's preferred language to config.json

    This function will ask the user to enter either "en" or "jp" and will then save that into config.json

    Requires one argument to be defined:
    - the config dictionary obtained from reading config.json
    """
    try:
        print_in_both_en_jp(
            en=(f"\n{F.RED}Error: Language is not defined in the config.json file.{END}"),
            jp=(f"\n{F.RED}エラー： config.jsonのLanguage（言語）が見当たらないです。{END}")
        )
    except:
        print(f"\n{F.RED}エラー： config.jsonのLanguage（言語）が見当たらないです。{END}")
        print(f"\n{F.RED}Error: Language is not defined in the config.json file.{END}")


    langInput = get_input_from_user(prompt="Select a language/言語を選択してください (en/jp): ", command=("en", "jp"))

    langExists = False
    if "Language" in config:
        languageData = config["Language"]
        langExists = True
    else: 
        languageData = {"Language": ""}

    if langExists: languageData = langInput
    else: languageData["Language"] = langInput

    with open(jsonPath, "w") as f:
        if not langExists: config.update(languageData)
        json.dump(config, f, indent=4)

    return langInput

def get_lang():
    """
    For loading the user's preferred language from config.json

    If the user has not set a preferred language in config.json, this function will call another function, set_lang, to ask the user to select a language and then save it to config.json for future runs.
    """
    config = {}
    try:
        with open(jsonPath, "r") as f:
            config = json.load(f)

        prefLang = config["Language"]
        if prefLang == "": raise Exception("Key is empty.")
        return prefLang
    except JSONDecodeError:
        with open(jsonPath, "w") as f:
            json.dump({}, f)
        return set_lang({})
    except:
        return set_lang(config)

def update_lang():
    """
    To update the user's preferred language choice into config.json

    It will prompt the user if they really want to change the language.

    If the user entered "n" for no, it will return either "en" or "jp" based on the config.json defined language.

    Otherwise, it will update the language in the config.json by inverting the values.

    E.g. if the config.json has "en" as the language, it will update the config.json to "jp" and vice versa.

    Afterwards, it will then return the updated language which is either "en" or "jp".
    """
    with open(jsonPath, "r") as f:
        config = json.load(f)

    if "Language" in config:
        if lang == "en": langPrompt = "Are you sure you would like to change the language? (y/n): "
        else: langPrompt = "言語を変更してもよろしいですか？(y/n)： "
        langChange = get_input_from_user(prompt=langPrompt, command=("y", "n"))

        if langChange == "y":
            if lang == "en":
                config["Language"] = "jp"
            else:
                config["Language"] = "en"
            

            with open(jsonPath, "w") as f:
                json.dump(config, f, indent=4)
        else:
            print_in_both_en_jp(
                en=(f"{F.LIGHTYELLOW_EX}Language change cancelled.{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}言語変更中止。{END}")
            )

        return config["Language"]
    else:
        return set_lang(config)

def check_if_user_is_logged_in():
    """
    Checks the global variables, fantiaCookieLoaded and pixivCookieLoaded if they both are True in which it will return True, Otherwise it will return False.
    """
    fantiaLoggedIn = pixivLoggedIn = False

    if fantiaCookieLoaded: fantiaLoggedIn = True
    if pixivCookieLoaded: pixivLoggedIn = True

    if fantiaLoggedIn and pixivLoggedIn: return True
    else: return False

def set_default_download_directory_to_desktop(jsonConfig):
    """
    To set the user's default download directory to the desktop and save it to config.json

    Requires one argument to be defined:
    - the config dictionary obtained from reading config.json
    """
    defaultDownloadFolderPath = pathlib.Path.home().joinpath("Desktop", "CulturedDownloader")
    jsonConfig["Download_Directory"] = str(defaultDownloadFolderPath)
    with open(jsonPath, "w") as f:
        json.dump(jsonConfig, f, indent=4)

    print_in_both_en_jp(
        en=(
            f"{F.YELLOW}Note: The default download folder will be defaulted to your desktop folder.{END}",
            f"{F.YELLOW}Default Download Folder Path: {defaultDownloadFolderPath}{END}"
        ),
        jp=(
            f"{F.YELLOW}注意： デフォルトのダウンロードフォルダをデスクトップに設定しました。{END}",
            f"{F.YELLOW}ダウンロードフォルダのフルパス： {defaultDownloadFolderPath}{END}"
        )
    )
    return defaultDownloadFolderPath

def set_default_download_directory(jsonConfig, **options):
    """
    To set the user's default download directory by prompting to enter the full path on their pc and save it to config.json

    Requires one argument to be defined:
    - the config dictionary obtained from reading config.json

    Optional arguments:
    - setDefaultLocationUponCancellation (bool): If False, it NOT will set the default download directory to the desktop if user do not want to change the default download directory.
    --> Default: True
    """
    setDefaultLocationCondition = options.get("setDefaultLocationUponCancellation")
    if setDefaultLocationCondition == None: setDefaultLocationCondition = True

    if lang == "en": 
        downloadFolderPrompt = "Would you like to change the default download location? (y/n): "
        downloadFolderChangePrompt = "Enter the FULL path of the download folder (X to cancel): "
    elif lang == "jp": 
        downloadFolderPrompt = "デフォルトのダウンロード場所を変更しますか？(y/n)： "
        downloadFolderChangePrompt = "ダウンロードフォルダのフルパスを入力してください (\"X\"でキャンセル)： "
    else: 
        downloadFolderPrompt = "Would you like to change the default download location?/デフォルトのダウンロード場所を変更しますか？ (y/n):"
        downloadFolderChangePrompt = "Enter the FULL path of the download folder (X to cancel)/\nダウンロードフォルダのフルパスを入力してください (\"X\"でキャンセル)： "

    downloadFolderChangeInput = get_input_from_user(prompt=downloadFolderPrompt, command=("y", "n"))

    if downloadFolderChangeInput == "n": 
        if setDefaultLocationCondition: return set_default_download_directory_to_desktop(jsonConfig)
        else: return

    while True:
        downloadPath = input(downloadFolderChangePrompt).strip()
        if downloadPath == "x" or downloadPath == "X": return set_default_download_directory_to_desktop(jsonConfig)
        
        downloadPath = pathlib.Path(downloadPath)

        if downloadPath.exists():
            if pathlib.Path(downloadPath).is_dir(): 
                jsonConfig["Download_Directory"] = str(downloadPath)
                with open(jsonPath, "w") as f:
                    json.dump(jsonConfig, f, indent=4)

                print_in_both_en_jp(
                    en=(f"{F.GREEN}The default folder has been changed to {downloadPath}{END}"),
                    jp=(f"{F.GREEN}デフォルトフォルダを {downloadPath} に変更しました。{END}")
                )
    
                return downloadPath
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Error: The download folder path you entered is not a directory.{END}"),
                    jp=(f"{F.RED}エラー： ダウンロードフォルダのパスがディレクトリではありません。{END}")
                )
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: Download folder path does not exist.{END}"),
                jp=(f"{F.RED}エラー： ダウンロードフォルダのパスが存在しません。{END}")
            )

def get_default_download_directory():
    """
    To read config.json and retrieves the default download directory.

    If there is a JSONDecodeError, it will write an empty dictionary to config.json
    """
    config = {}
    try:
        with open(jsonPath, "r") as f:
            config = json.load(f)

        prefDownloadDirectory = config["Download_Directory"]
        if prefDownloadDirectory == "": raise Exception("Key is empty.")

        prefDownloadDirectory = pathlib.Path(prefDownloadDirectory)
        prefDownloadDirectory.mkdir(parents=True, exist_ok=True)
        return prefDownloadDirectory
    except JSONDecodeError:
        with open(jsonPath, "w") as f:
            json.dump({}, f)
        return set_default_download_directory({})
    except:
        return set_default_download_directory(config)

def get_key():
    """
    To get the key for encryption and decryption which will return a 32 bytes string

    Note: it will create the configs folder if the configs has not been created yet.
    """
    configFolder = get_saved_config_data_folder().joinpath("configs")
    configFolder.mkdir(parents=True, exist_ok=True)

    keyPath = configFolder.joinpath("key")
    if keyPath.is_file():
        with open(keyPath, "rb") as f:
            key = dill.load(f)
    else:
        key = get_random_bytes(32)
        with open(keyPath, "wb") as f:
            dill.dump(key, f)

    return key

def delete_encrypted_data():
    """
    Used when the function encrypt_data or decrypt_data has encountered issues decrypting the encrypted cookies

    This function will delete the files, key, pixiv_cookies, or fantia_cookies (if any are found) in the "configs" folder.
    """
    print("\n")
    print_in_both_en_jp(
        en=(f"{F.RED}Fatal Error: Could not decrypt cookie.{END}", 
        f"{F.RED}Resetting Key and deleting encrypted cookies...{END}"),
        jp=(f"{F.RED}致命的なエラー: クッキーを復号化できませんでした。{END}", 
        f"{F.RED}鍵のリセットと暗号化されたクッキーを削除します...{END}")
    )

    keyPath = appPath.joinpath("configs", "key")
    if keyPath.is_file(): keyPath.unlink()
    
    pixivCookiePath = appPath.joinpath("configs", "pixiv_cookies")
    if pixivCookiePath.is_file(): pixivCookiePath.unlink()

    fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
    if fantiaCookiePath.is_file(): fantiaCookiePath.unlink()

    print_in_both_en_jp(
        en=(f"{F.RED}Please restart the program.{END}"), 
        jp=(f"{F.RED}このプログラムを再起動してください。{END}")
    )
    if lang == "en": input("Please enter any key to exit...")
    elif lang == "jp": input("何か入力すると終了します...")

def encrypt_data(data):
    """
    To encrypt the data using the global variable ChaChaKey obtained from the function get_key as the encryption key

    Requires one argument to be defined:
    - A dictionary containing the data to be encrypted
    """
    header = b"Cultured_Downloader" # converts string to bytes string
    if type(data) == dict:
        data = json.dumps(data) # converts the dict to a string

        try:
            cipher = Cha.new(key=ChaChaKey)
        except TypeError:
            raise EncryptionKeyError

        cipher.update(header)
        cipherText, tag = cipher.encrypt_and_digest(data.encode())

        dictKeys = ["nonce", "header", "cipherText", "tag"]
        valuesList = [b64encode(x).decode() for x in (cipher.nonce, header, cipherText, tag)] # b64encodes the values and decode it to a string

        encryptedData = dict(zip(dictKeys, valuesList)) # converts both lists to a dictionary

        return EncryptedData(encryptedData)
    else:
        raise Exception("Data to be encrypted is not a dictionary...")

def decrypt_data(encryptedData):
    """
    To decrypt the data using the global variable ChaChaKey obtained from the function get_key as the encryption key

    Requires one argument to be defined:
    - A dictionary containing the encrypted values
    """
    try:
        b64encodedDict = encryptedData.get_encrypted_data() # a dictionary of b64encoded values
        b64decodedDict = {key:b64decode(b64encodedDict[key]) for key in b64encodedDict.keys()}

        cipher = Cha.new(key=ChaChaKey, nonce=b64decodedDict["nonce"])
        cipher.update(b64decodedDict["header"])

        plaintext = cipher.decrypt_and_verify(b64decodedDict["cipherText"], b64decodedDict["tag"])
        return json.loads(plaintext.decode()) # since the value of the cookie is a string, json.loads to deserialise it to a dictionary
    except (ValueError, KeyError, TypeError):
        raise DecryptError

"""--------------------------- End of Config Codes ---------------------------"""

"""--------------------------- Start of Functions Codes ---------------------------"""

def check_if_input_is_url(inputString, website):
    """
    Validates if the user's inputs is a valid URL and is a URL for Fantia posts, Fantia image URL, and Pixiv Fanbox posts using regex.

    Requires two arguments to be defined:
    - User's input (string or list)
    - The website, either "fantiaPost", "fantiaImage", "pixivFanbox", "fantiaPostPage", or "pixivFanboxPostPage" (string)
    """
    if type(inputString) != list:
        try:
            result = urlparse(inputString)
            if all([result.scheme, result.netloc]):
                if website == "fantiaPost":
                    if re.fullmatch(fantiaPostRegex, inputString):
                        return True
                    else:
                        return False
                elif website == "fantiaImage":
                    if re.fullmatch(fantiaImageURLRegex, inputString):
                        return True
                    else:
                        return False
                elif website == "pixivFanbox":
                    if re.match(pixivFanboxPostRegex, inputString):
                        return True
                    else:
                        return False
                elif website == "fantiaPostPage":
                    if re.fullmatch(fantiaPostPageRegex, inputString):
                        return True
                    else:
                        return False
                elif website == "pixivFanboxPostPage":
                    if re.fullmatch(pixivFanboxPostPageRegex, inputString):
                        return True
                    else:
                        return False
            else: return False
        except:
            return False
    else:
        for url in inputString:
            try:
                result = urlparse(url)
                if not all([result.scheme, result.netloc]): return False

                if website == "fantiaPost":
                    if not re.fullmatch(fantiaPostRegex, url): return False
                elif website == "fantiaImage":
                    if not re.fullmatch(fantiaImageURLRegex, url): return False
                elif website == "pixivFanbox":
                    if not re.match(pixivFanboxPostRegex, url): return False
                elif website == "fantiaPostPage":
                    if not re.fullmatch(fantiaPostPageRegex, url): return False
                elif website == "pixivFanboxPostPage":
                    if not re.fullmatch(pixivFanboxPostPageRegex, url): return False
            except:
                return False

        return True

def split_inputs_to_possible_multiple_inputs(userInput):
    """
    Removes all whitespaces including Japanese whitespaces and splits the user's inputs into a list of possible inputs based on the delimiters, "," or "、".

    Requires one argument to be defined:
    - A string
    """
    userInput = userInput.replace(" ", "")
    userInput = userInput.replace("　", "")
    if "," in userInput: userInput = userInput.split(",")
    elif "、" in userInput: userInput = userInput.split("、")
    return userInput

# function below from https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code
def get_status(logs):
    """
    Function to get the status code of a webpage

    Used for auto detecting the number of images to download for Fantia (option 1 on the menu)

    Credits to Jarad: https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code

    Requires one argument to be defined:
    - A log obtained from webdriver.get_log("performance")
    """
    for log in logs:
        if log["message"]:
            d = json.loads(log["message"])
            try:
                content_type = "text/html" in d["message"]["params"]["response"]["headers"]["content-type"]
                response_received = d["message"]["method"] == "Network.responseReceived"
                if content_type and response_received:
                    return d["message"]["params"]["response"]["status"]
            except:
                pass

def check_if_directory_has_files(dirPath):
    """
    Returns True if there is any files or folders in the argument given.

    Otherwise, it will return False.

    Requires one argument to be defined:
    - A pathlib Path object
    """
    hasFiles = any(dirPath.iterdir())
    return hasFiles

# function for requests library cookie session
def get_cookie_for_session(website, **options):
    """
    Return the cookie for pixiv or Fantia account needed for the login session used for the download of the images via the requests library.

    Will return a requests session object with the corresponding cookie data if the cookie file exists.

    Otherwise, it will return an empty string, "".

    Requires one argument to be defined:
    - The website name which is either "pixiv" or "fantia" (string) 

    Optional param:
    - sessionID, a value of a cookie (string) --> if defined, it will not load the cookie values from the configs folder but will load based on the defined session ID.
    """
    definedSessionID = options.get("sessionID")

    cookiePath = appPath.joinpath("configs", f"{website}_cookies")

    if website == "pixiv":
        domain = "fanbox.cc"
        cookieName = "FANBOXSESSID"
    elif website == "fantia":
        domain = "fantia.jp"
        cookieName = "_session_id"
    else:
        raise Exception("Invalid website in get_cookie_for_session function...")


    if cookiePath.is_file() and not definedSessionID:
        sessionID = ""
        with open(cookiePath, "rb") as f:
            cookie = decrypt_data(dill.load(f))
            if cookie["name"] == cookieName:
                sessionID = cookie["value"]
        
        if sessionID != "":
            sessionObject = requests.session()
            sessionIDCookie = requests.cookies.create_cookie(domain=domain, name=cookieName, value=sessionID)
            sessionObject.cookies.set_cookie(sessionIDCookie)
            return sessionObject
        else: return ""
    else:
        if definedSessionID:
            sessionObject = requests.session()
            sessionIDCookie = requests.cookies.create_cookie(domain=domain, name=cookieName, value=definedSessionID)
            sessionObject.cookies.set_cookie(sessionIDCookie)
            return sessionObject
        else: return ""

def load_cookie(website):
    """
    For adding Fantia cookie into the webdriver.

    Will return True or False depending on whether the cookie has been loaded successfully or not.

    Requires one argument to be defined:
    - The website which is either "pixiv" or "fantia" (string)
    """
    cookiePath = appPath.joinpath("configs", f"{website}_cookies")

    if cookiePath.is_file():
        if website == "fantia": driver.get("https://fantia.jp/")
        elif website == "pixiv": driver.get("https://www.fanbox.cc/")
        else: raise Exception("Invalid website argument in load_cookie function...")

        with open(cookiePath, 'rb') as f:
            cookie = decrypt_data(dill.load(f))

        driver.delete_all_cookies()
        driver.add_cookie(cookie)

        if website == "fantia": websiteURL = "https://fantia.jp/mypage/users/plans"
        else: websiteURL = "https://www.fanbox.cc/messages"

        driver.get(websiteURL)
        if driver.current_url == websiteURL: 
            print_in_both_en_jp(
                en=(f"{F.GREEN}{website.title()} cookied loaded successfully!{END}"),
                jp=(f"{F.GREEN}{website.title()}のクッキーが正常に読み込まれました！{END}")
            )
            return True
        else: return False
    else: return False

def get_file_name(imageURL, website):
    """
    Returns the file name based on the URL given.

    Requires two arguments to be defined:
    - A URL (string)
    - The website name (string)
    """
    if website == "Fantia":
        try: return imageURL.split("/")[-1].split("?")[0]
        except: error_shutdown(
                en=("Error: Unable to retrieve image name from the image URL.", "Please report this error to the developer."),
                jap=("エラー： 画像URLから画像名を取得できません。", "このエラーを開発者に報告してください。")
            )
    elif website == "Pixiv":
        try: return imageURL.split("/")[-1]
        except: error_shutdown(
                en=("Error: Unable to retrieve image name from the image URL.", "Please report this error to the developer."),
                jap=("エラー： 画像URLから画像名を取得できません。", "このエラーを開発者に報告してください。")
            )
    else: error_shutdown(
            en=("Error: Unknown website.", "Please report this error to the developer."),
            jap=("エラー： 不明なウェブサイト。", "このエラーを開発者に報告してください。")
        )

# Unused function
# def get_pixiv_image_full_res_url(imageURL):
#     """
#     Returns the url without the height and width limit defined by pixiv

#     Requires one argument to be defined:
#     - The image's URL (string)
#     """
#     try:
#         if imageURL.split(".")[-1] == "gif": return imageURL
#         else:
#             urlArray = []
#             for urlParts in imageURL.split("/"):
#                 if urlParts == "w" or urlParts == "1200": pass
#                 else: urlArray.append(urlParts)
#             return "/".join(urlArray)
#     except AttributeError:
#         raise AttributeError

def save_image(imageURL, pathToSave, **requestSession):
    """
    Downloads the image using the requests library.

    Requires two arguments to be defined:
    - The image's URL (string)
    - The path to save the image (pathlib Path object)

    Optional param:
    - session (requests session object)
    """
    if "session" in requestSession:
        session = requestSession["session"]
        with session.get(imageURL, stream=True) as r:
            with open(pathToSave, "wb") as f:
                copyfileobj(r.raw, f)
    else:    
        with requests.get(imageURL, stream=True) as r:
            with open(pathToSave, "wb") as f:
                copyfileobj(r.raw, f)

def print_progress_bar(prog, totalEl, caption):
    """
    For printing a progress bar such as the one below.

    [============] 100% Downloading 2 out of 2 images...

    Requires three arguments to be defined:
    - The current progress (int)
    - The max progress or max number of elements (int)
    - A caption such as "Downloading 2 out of 2 images..." (string)
    """
    barLength = 20 #size of progress bar
    try:
        currentProg = prog / totalEl
    except ZeroDivisionError:
        return

    sys.stdout.write("\r")
    sys.stdout.write(f"{F.LIGHTYELLOW_EX}[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}{END}")
    sys.stdout.flush()

def print_download_completion_message(totalImage, subFolderPath, **options):
    """
    For printing the completion message to alert the user that all the images have been downloaded.

    Requires two arguments to be defined:
    - The total number of images (int)
    - The path to the folder where the images are saved (pathlib Path object or a string)

    Optional param:
    - attachments (bool) if True, will print out the corresponding message instead of just alerting the user that the program have downloaded all the images. 
    --> default: False if not defined
    """
    if "attachments" in options: attachments = options["attachments"]
    else: attachments = False

    if totalImage > 0:
        if attachments:
            print_in_both_en_jp(
            en=(
                f"\n{F.GREEN}Successfully downloaded {totalImage} images and attachments at\n{subFolderPath}{END}"
            ),
            jp=(
                f"\n{F.GREEN}{subFolderPath} にある{totalImage}個のイメージと添付ファイルのダウンロードに成功しました。{END}"
            )
        )
        else:
            print_in_both_en_jp(
                en=(
                    f"\n{F.GREEN}Successfully downloaded {totalImage} images at\n{subFolderPath}{END}"
                ),
                jp=(
                    f"\n{F.GREEN}{subFolderPath} に{totalImage}枚の画像をダウンロードしました!{END}"
                )
            )
    else:
        print_in_both_en_jp(
            en=(f"\n{F.RED}Error: No images to download.{END}"),
            jp=(f"\n{F.RED}エラー： ダウンロードする画像がありません。{END}")
        )

def open_new_tab():
    """
    For executing a javascript code on the browser to open a new tab.
    """
    driver.execute_script("window.open('_blank');")
    driver.switch_to.window(driver.window_handles[-1])

def close_new_tab():
    """
    For executing a javascript code on the browser to close the new tab.
    """
    driver.execute_script("window.close();")
    driver.switch_to.window(driver.window_handles[0])

# Unused function
# def get_latest_post_num_from_file_name():
#     """
#     To retrieve the latest/highest post_num from all the files in the browser's default download folder.

#     This is used when the requests session object is not defined and is equal to "".

#     Returns the latest/highest post_num (int)
#     """
#     postNumList = []
#     try:
#         for filePath in browserDownloadLocation.iterdir():
#             if filePath.is_file():
#                 filePath = str(filePath.name).split("_")
#                 postNumList.append(int(filePath[1]))
#         return max(postNumList) + 1
#     except:
#         return 0

# Unused failsafe function if pixivSession is equal to ""
# def download_image_javascript(imageSrcURL, imageName):
#     """
#     Returns a javascript code to be executed for downloading pixiv images on the webdriver browser.

#     Requires two arguments to be defined:
#     - The image's URL (string)
#     - The image's name (string)
#     """
#     downloadImageHeaderJS = """function download(imageURL) {"""
#     downloadImageFooterJS = f"""
#     const fileName = "{imageName}"  + imageURL.split('/').pop();
#     var el = document.createElement("a");
#     el.setAttribute("href", imageURL);
#     el.setAttribute("download", fileName);
#     document.body.appendChild(el);
#     el.click();
#     el.remove();
# """
#     downloadImageExecuteFn = f"download('{imageSrcURL}');"
    
#     return "".join([downloadImageHeaderJS, downloadImageFooterJS, "}\n", downloadImageExecuteFn])

def check_for_incomplete_download():
    """
    To check for any incomplete downloads by the webdriver's browser in its default download location.
    """
    sleep(2) # some delays to make sure every files has been downloaded.
    while True:
        browserDownloadLocation.mkdir(parents=True, exist_ok=True)
        hasIncompleteDownloads = False
        for filePath in browserDownloadLocation.iterdir():
            if filePath.is_file():
                fileExtension = str(filePath.name).split(".")[-1]
                if fileExtension.lower() == "crdownload": # since edge is set to use chromium, hence not checking for .partial files
                    hasIncompleteDownloads = True

        if not hasIncompleteDownloads: break

def remove_any_files_in_directory(pathToDelete):
    """
    Remove any files in the given directory defined by the first argument.

    Requires one argument to be defined:
    - The path to the directory to be deleted (pathlib Path object)
    """
    if pathToDelete.is_dir():
        for file in pathToDelete.iterdir():
            if file.is_file():
                file.unlink()
    else:
        raise Exception("The given path is not a directory...")

def download(urlInput, website, subFolderPath, **options):
    """
    To download images from Fantia or pixiv Fanbox.

    Requires three arguments to be defined:
    - The url of the Fantia/pixiv posts or the Fantia image url (string)
    - The website which is either "FantiaImageURL", "FantiaPost", or "Pixiv" (string)
    - The path to the folder where the images are saved or a string which will be the latest post num for pixiv downloads (pathlib Path object or a string)

    Optional param:
    - attachments (boolean). If True, will download any attachments from the given url (default: False if not defined)
    """
    driver.get(urlInput)

    downloadAttachmentFlag = options.get("attachments")
    if downloadAttachmentFlag == None: downloadAttachmentFlag = False

    if website == "FantiaImageURL":
        # downloading nth num of images based on the Fantia image given
        # e.g. https://fantia.jp/posts/*/post_content_photo/*
        imageSrc = driver.find_element(by=By.XPATH, value="/html/body/img").get_attribute("src")
        imagePath = subFolderPath.joinpath(get_file_name(imageSrc, "Fantia"))
        subFolderPath.mkdir(parents=True, exist_ok=True)
        save_image(imageSrc, imagePath)

    elif website == "FantiaPost":
        sleep(3)
        try: thumbnailSrc = driver.find_element(by=By.XPATH, value="//img[contains(@class, 'img-default')]").get_attribute("src")
        except: thumbnailSrc = None

        if thumbnailSrc:
            thumbnailDownloadFolder = subFolderPath.joinpath("thumbnail")
            thumbnailDownloadFolder.mkdir(parents=True, exist_ok=True)
            imagePath = thumbnailDownloadFolder.joinpath(get_file_name(thumbnailSrc, "Fantia"))
            # no session needed since it's displayed regardless of membership status
            save_image(thumbnailSrc, imagePath) 
        
        imagesURLToDownloadArray = []

        fantiaImageClassOffset = 0
        # retrieving images' URL that are usually free but can restricted to those with memebership but these images are usually low in resolution
        try: imagePosts = driver.find_elements(by=By.CLASS_NAME, value="fantiaImage")
        except: imagePosts = []

        fantiaImageClassOffset = len(imagePosts)

        # Retrieving Fantia blog images's URL that are may be locked by default due to membership restrictions
        for imagePost in imagePosts:
            imageHREFLink = imagePost.get_attribute("href")
            imagesURLToDownloadArray.append(imageHREFLink)

        # Retrieving images' URL that are free and are usually low in resolution but can be restricted to those with membership and have high resolution images
        try: fullyDisplayedImageAnchor = driver.find_elements(by=By.XPATH, value="//a[@class='image-container clickable']") 
        except: fullyDisplayedImageAnchor = []
        
        for anchor in fullyDisplayedImageAnchor:
            anchor.click()
            sleep(0.5)
            fullyDisplayedImageURL = driver.find_element(by=By.XPATH, value="//a[contains(text(),'オリジナルサイズを表示 ')]").get_attribute("href")
            imagesURLToDownloadArray.append(fullyDisplayedImageURL)
            driver.find_element(by=By.XPATH, value="//a[@class='btn btn-dark btn-sm']").click()
            sleep(0.5)

        # Retrieving images' URL that are free but can be restricted to those with membership but has multiple images hence, the force-square class
        try: premiumImages = driver.find_elements(by=By.XPATH, value="//a[@class='image-container force-square clickable']")
        except: premiumImages = []

        for paidImageContainer in premiumImages:
            paidImageContainer.click()
            sleep(0.5)
            paidImageURL = driver.find_element(by=By.XPATH, value="//a[contains(text(),'オリジナルサイズを表示 ')]").get_attribute("href")
            imagesURLToDownloadArray.append(paidImageURL)
            driver.find_element(by=By.XPATH, value="//a[@class='btn btn-dark btn-sm']").click()
            sleep(0.5)
        
        # Retrieving attachment url if the user chose to download attachment as well as an addon to this program and start printing the progress bar
        totalImageProgress = 0
        if downloadAttachmentFlag:
            try: attachmentAnchors = driver.find_elements(by=By.XPATH, value="//a[@class='btn btn-success btn-very-lg']")
            except: attachmentAnchors = []

            totalImages = len(imagesURLToDownloadArray) + len(attachmentAnchors)

            remove_any_files_in_directory(browserDownloadLocation)
            for anchor in attachmentAnchors:
                if lang == "en": downloadMessage = f"Downloading image/attachment no.{totalImageProgress} out of {totalImages}"
                elif lang == "jp": downloadMessage = f"画像や添付ファイル {totalImageProgress} / {totalImages} をダウンロード中"

                if totalImageProgress == 0:
                    print_progress_bar(totalImageProgress, totalImages, downloadMessage)
                    totalImageProgress += 1

                driver.get(anchor.get_attribute("href")) # instead of clicking since for some reasons, it doesn't always work

                sleep(3) # for the browser to download the attachment
                
                if lang == "en": downloadMessage = f"Downloading image/attachment no.{totalImageProgress} out of {totalImages}"
                elif lang == "jp": downloadMessage = f"画像や添付ファイル {totalImageProgress} / {totalImages} をダウンロード中"

                print_progress_bar(totalImageProgress, totalImages, downloadMessage)
                totalImageProgress += 1
            
            if attachmentAnchors:
                check_for_incomplete_download()
                # moves all the files to the corresponding folder based on the user's input.
                attachmentFolderPath = subFolderPath.joinpath("attachments")
                for file in browserDownloadLocation.iterdir():
                    attachmentFolderPath.mkdir(parents=True, exist_ok=True)
                    move(file, attachmentFolderPath.joinpath(file.name)) 
            else:
                totalImageProgress += 1 # since the for loop won't be executed, plus one for the next loop
        else:
            totalImages = len(imagesURLToDownloadArray)

            if lang == "en": downloadMessage = f"Downloading image no.{totalImageProgress} out of {totalImages}{END}"
            elif lang == "jp":  downloadMessage = f"画像 {totalImageProgress} / {totalImages} をダウンロード中"

            print_progress_bar(totalImageProgress, totalImages, downloadMessage)
            totalImageProgress += 1

        # Downloading all the retrieved images' URL
        if fantiaImageClassOffset > 0: 
            downloadFolder = subFolderPath.joinpath("website_displayed_images")
        else:
            downloadFolder = subFolderPath.joinpath("downloaded_images")
        
        counter = 0
        for imageURL in imagesURLToDownloadArray:
            downloadFolder.mkdir(parents=True, exist_ok=True)

            if downloadAttachmentFlag:
                if lang == "en": downloadMessage = f"Downloading image/attachment no.{totalImageProgress} out of {totalImages}"
                elif lang == "jp": downloadMessage = f"画像や添付ファイル {totalImageProgress} / {totalImages} をダウンロード中"
            else:
                if lang == "en": downloadMessage = f"Downloading image no.{totalImageProgress} out of {totalImages}{END}"
                elif lang == "jp":  downloadMessage = f"画像 {totalImageProgress} / {totalImages} をダウンロード中"

            open_new_tab()
            driver.get(imageURL)
            imageSrc = driver.find_element(by=By.XPATH, value="/html/body/img").get_attribute("src")
            imagePath = downloadFolder.joinpath(get_file_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)
            close_new_tab()

            if fantiaImageClassOffset > 0:
                if counter != fantiaImageClassOffset: counter += 1
                if counter == fantiaImageClassOffset:
                    downloadFolder = subFolderPath.joinpath("downloaded_images")

            print_progress_bar(totalImageProgress, totalImages, downloadMessage)
            totalImageProgress += 1

        print_download_completion_message(totalImages, subFolderPath, attachment=downloadAttachmentFlag)

    elif website == "Pixiv":
        sleep(3)
        urlToDownloadArray = []

        # downloads gifs or static images based on a pixiv post
        try: imagesAnchors = driver.find_elements(by=By.XPATH, value="//a[contains(@class, 'iyApTb')]")
        except: imagesAnchors = []

        for anchor in imagesAnchors:
            urlToDownloadArray.append(anchor.get_attribute("href"))

        # for attachment, get anchor url and go to that url to download it, similar to Fantia's process
        # Chose this approach since large files will take a while and the remote connection may close after a certain period of time
        progress = 0
        if downloadAttachmentFlag:
            try: attachmentAnchors = driver.find_elements(by=By.XPATH, value="//a[@class='sc-gw5z20-7 bGOrSj']")
            except: attachmentAnchors = []

            totalImages = len(urlToDownloadArray) + len(attachmentAnchors)
            remove_any_files_in_directory(browserDownloadLocation)
            for anchor in attachmentAnchors:
                if lang == "en": downloadMessage = f"Downloading image/attachment no.{progress} out of {totalImages}"
                elif lang == "jp": downloadMessage = f"画像や添付ファイル {progress} / {totalImages} をダウンロード中"

                if progress == 0:
                    print_progress_bar(progress, totalImages, downloadMessage)
                    progress += 1

                driver.get(anchor.get_attribute("href")) # instead of clicking since for some reasons, it doesn't always work

                sleep(3) # for the browser to download the attachment

                if lang == "en": downloadMessage = f"Downloading image/attachment no.{progress} out of {totalImages}"
                elif lang == "jp": downloadMessage = f"画像や添付ファイル {progress} / {totalImages} をダウンロード中"

                print_progress_bar(progress, totalImages, downloadMessage)
                progress += 1

            if attachmentAnchors:
                check_for_incomplete_download()
                # moves all the files to the corresponding folder based on the user's input.
                for file in browserDownloadLocation.iterdir():
                    subFolderPath.mkdir(parents=True, exist_ok=True)
                    move(file, subFolderPath.joinpath(file.name)) 
            else:
                progress += 1 # since the for loop won't be executed, plus one for the next loop
        else:
            totalImages = len(urlToDownloadArray)
            if lang == "en": downloadMessage = f"Downloading image no.{progress} out of {totalImages}{END}"
            elif lang == "jp":  downloadMessage = f"画像 {progress} / {totalImages} をダウンロード中"
            print_progress_bar(progress, totalImages, downloadMessage)
            progress += 1
        
        for url in urlToDownloadArray:
            subFolderPath.mkdir(parents=True, exist_ok=True)
            
            save_image(url, subFolderPath.joinpath(get_file_name(url, "Pixiv")), session=pixivSession)

            if downloadAttachmentFlag:
                if lang == "en": downloadMessage = f"Downloading image/attachment no.{progress} out of {totalImages}"
                elif lang == "jp": downloadMessage = f"画像や添付ファイル {progress} / {totalImages} をダウンロード中"
            else:
                if lang == "en": downloadMessage = f"Downloading image no.{progress} out of {totalImages}{END}"
                elif lang == "jp":  downloadMessage = f"画像 {progress} / {totalImages} をダウンロード中"

            print_progress_bar(progress, totalImages, downloadMessage)
            progress += 1
            
        print_download_completion_message(totalImages, subFolderPath, attachment=downloadAttachmentFlag)

    else: raise Exception("Invalid website argument in download function...")

def check_if_folder_name_contains_illegal_char(userFolderNameInput):
    """
    Returns True if the user's input path has illegal characters such as ":" or "*", etc.

    Requires one argument to be defined:
    - A folder name entered by the user (string)

    More information on illegal characters in a file/folder name: https://docs.microsoft.com/en-gb/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN
    """
    illegalChars = '<>:"/\\|?*' # based on https://docs.microsoft.com/en-gb/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN
    if any(char in illegalChars for char in userFolderNameInput): return True
    else: return False

def create_subfolder(website):
    """
    Asks the user for a folder name to save all the images to be downloaded into (The user can enter "X" to cancel this process).

    Afterwards, it creates a folder with the name the user entered and returns a pathlib Path object to the user's defined folder to that folder.

    Requires one argument to be defined:
    - The website the user is downloading images from, either "fantia" or "pixiv" (string)
    """
    while True:
        if lang == "en": folderName = input("Enter the name of the folder you want to save the images (X to cancel): ").strip()
        else: folderName = input("画像を保存するフォルダーの名前を入力してください (\"X\"でキャンセル): ").strip()

        if not check_if_folder_name_contains_illegal_char(folderName):
            if folderName.upper() == "X": return "X"
            if folderName != "":
                # subfolder
                if website == "fantia": imagePath = fantiaDownloadLocation.joinpath(folderName)
                elif website == "pixiv": imagePath = pixivDownloadLocation.joinpath(folderName)
                else: raise Exception("Invalid website for create_subfolder function...")

                imagePath.mkdir(parents=True, exist_ok=True)

                if check_if_directory_has_files(imagePath): 
                    print_in_both_en_jp(
                        en=(f"{F.RED}Error: Folder already exists with images inside.\nPlease enter a different {END}{F.RED}{Style.BRIGHT}NEW{END} {F.RED}name for a new folder.{END}"),
                        jp=(f"{F.RED}エラー： フォルダはすでに存在し、その中に画像があります。{END}{F.RED}{Style.BRIGHT}新しい名前{END}{F.RED}を入力してください。{END}")
                    )
                    print("\n")
                else: return imagePath
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Error: Please enter a name for the folder.{END}"),
                    jp=(f"{F.RED}エラー： フォルダの名前を入力してください。{END}")
                )
                print("\n")
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: Please enter a valid folder name.{END}"),
                jp=(f"{F.RED}エラー： 有効なフォルダ名を入力してください。{END}")
            )
            print("\n")

def login(currentDriver, website):
    """
    Used to verify if the loaded cookie is valid and allows the webdriver to be logged in.

    Returns True if the cookie is valid, False otherwise.

    Requires two arguments to be defined:
    - The current driver (WebDriver)
    - The website the user is downloading images from, either "fantia" or "pixiv" (string)
    """
    if website == "fantia":
        loginURL = "https://fantia.jp/sessions/signin"
        urlVerifier = "https://fantia.jp/mypage/users/plans"
    elif website == "pixiv":
        loginURL = "https://www.fanbox.cc/login"
        urlVerifier = "https://www.fanbox.cc/creators/supporting"
    else:
        raise Exception("Invalid website in login function...")

    currentDriver.get(loginURL)

    print_in_both_en_jp(
        en=(
            f"{F.LIGHTYELLOW_EX}A new browser should have opened. However, please do not close it at all times!{END}",
            f"{F.LIGHTYELLOW_EX}Please enter your username and password and login to {website.title()} manually.{END}",
        ),
        jp=(
            f"{F.LIGHTYELLOW_EX}新しいブラウザが起動したはずです。ただし、常に閉じないようにしてください！{END}", 
            f"{F.LIGHTYELLOW_EX}ユーザー名とパスワードを入力し、手動で{website.title()}にログインしてください。{END}",
        )
    )

    if lang == "en": input("Press any key to continue after logging in...")
    else: input("ログイン後に何かキーを押してください...")

    try:
        currentDriver.get(urlVerifier)
        sleep(1)
        # waiting until the browser loads the page
        WebDriverWait(currentDriver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
    except TimeoutException:
        print_in_both_en_jp(
            en=(f"{F.RED}Error: TimeoutException. Please try again.{END}"),
            jp=(f"{F.RED}エラー: タイムアウトエラー。再度実行してください。{END}")
        )
        return False

    if currentDriver.current_url != urlVerifier: return False
    else: return True

def save_and_load_cookie(originalDriver, website, **options):
    """
    To save the cookie needed for the login session into the configs folder and encrypts the cookie data.

    Returns True if user is successfully logged in but does not necessarily mean that 
    the cookie is saved into the configs folder as the user can choose to save it or not.

    Requires two arguments to be defined:
    - The current driver (WebDriver)
    - The website the user is downloading images from, either "fantia" or "pixiv" (string)

    Optional param:
    - getID to retrieve the cookie session ID (bool)
    """

    getSessionID = options.get("getID")

    newDriver = get_driver(selectedBrowser, headless=False, blockImg=1)
    if website == "fantia":
        cookieName = "_session_id"
        websiteURL = "https://fantia.jp/"
    elif website == "pixiv":
        cookieName = "FANBOXSESSID"
        websiteURL = "https://www.fanbox.cc/"
    else:
        raise Exception("Invalid website in save_and_load_cookie function...")

    cookiePath = appPath.joinpath("configs", f"{website}_cookies")
    loggedIn = False
    while True:
        loggedIn = login(newDriver, website)
        if loggedIn: break
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: {website.title()} login failed.{END}"),
                jp=(f"{F.RED}エラー： Fantiaのログインに失敗しました。{END}")
            )
            if lang == "en": retryInput = get_input_from_user(prompt="Would you like to retry logging in manually? (y/n): ", command=("y", "n"))
            else: retryInput = get_input_from_user(prompt="もう一度手動でログインし直しますか？(y/n)： ", command=("y", "n"))
            if retryInput == "n": break

    if loggedIn:
        if lang == "en": cookiePrompt = f"Would you like to save your {website.title()} session cookie for a faster login next time? (y/n): "
        else: cookiePrompt = f"{website.title()}のセッションクッキーを保存して、次回のログインを早くしたいですか？ (y/n): "
        saveCookieCondition = get_input_from_user(prompt=cookiePrompt, command=("y", "n"))

        if newDriver.current_url != websiteURL: newDriver.get(websiteURL)
        cookies = newDriver.get_cookies()

        cookieToSave = ""
        for cookie in cookies:
            if cookie["name"] == cookieName:
                cookieToSave = cookie
        
        if saveCookieCondition == "y":
            configFolder = appPath.joinpath("configs")
            configFolder.mkdir(parents=True, exist_ok=True)
            with open(cookiePath, "wb") as f:
                dill.dump(encrypt_data(cookieToSave), f)

            print_in_both_en_jp(
                en=(f"{F.GREEN}The cookie has been saved to {cookiePath}\nThe cookie will be automatically loaded in next time in Cultured Downloader for a faster login process!{END}"),
                jp=(f"{F.GREEN}{cookiePath} に保存されたクッキーは、次回からCultured Downloaderで自動的に読み込まれ、ログイン処理が速くなります!{END}")
            )
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Saving of {website.title()} cookie will be aborted as per user's request.{END}"),
                jp=(f"{F.RED}{website.title()}のセッションCookieの保存は、ユーザーの要求に応じて中止されます。{END}")
            )

        if originalDriver.current_url != websiteURL: 
            originalDriver.get(websiteURL)
            sleep(3)

        originalDriver.delete_all_cookies()
        originalDriver.add_cookie(cookie)

        newDriver.quit()
        if getSessionID: return True, cookieToSave["value"]
        else: return True
    else: 
        newDriver.quit()
        if getSessionID: return False, None
        else: return False

def get_page_num(userURLInput):
    """
    Used for retreiving the number of pages to go through from the user's input.

    Note: It uses the compiled regex to check for input validity such as "1-2", or "1".

    Requires one argument to be defined:
    - The user's URL input (string or list)
    """
    print("\n")
    while True:
        print_in_both_en_jp(
            en=(f"{F.YELLOW}Note: If you have entered multiple urls previously, please enter in this format, \"1-3, 5, 2-10\"{END}"),
            jp=(f"{F.YELLOW}注意： 以前に複数のURLを入力したことがある場合は、このフォーマットで入力してください。\"1-3、5、2-10\"{END}")
        )
        if lang == "en": pageInput = split_inputs_to_possible_multiple_inputs(input("Enter the number of pages (X to cancel): "))
        else: pageInput = split_inputs_to_possible_multiple_inputs(input("ページ数を入力します (Xでキャンセル)： "))

        if pageInput == "x" or pageInput == "X": 
            return False
            
        if (pageInput == ""):
            print_in_both_en_jp(
                en=(
                    f"{F.RED}Error: No URL entered or URL entered.{END}"
                ),
                jp=(
                    f"{F.RED}エラー： URLが入力されていない。{END}"
                )
            )
        else: 
            if type(pageInput) == list:
                validPageNumInputs = True
                for pageNum in pageInput:
                    if re.fullmatch(pageNumRegex, pageNum) == None:
                        validPageNumInputs = False
                if validPageNumInputs:
                    if type(userURLInput) == list:
                        if len(userURLInput) == len(pageInput):
                            return pageInput
                        else:
                            print_in_both_en_jp(
                                en=(
                                    f"{F.RED}Error: The number of URLs entered is different from the number of pages entered.{END}"
                                ),
                                jp=(
                                    f"{F.RED}エラー： URLの個数とページ数の個数が違います。{END}"
                                )
                            )
                    else:
                        print_in_both_en_jp(
                                en=(
                                    f"{F.RED}Error: The number of URLs entered is different from the number of pages entered.{END}"
                                ),
                                jp=(
                                    f"{F.RED}エラー： URLの個数とページ数の個数が違います。{END}"
                                )
                            )
                else:
                    print_in_both_en_jp(
                        en=(
                            f"{F.RED}Error: Invalid format.{END}"
                        ),
                        jp=(
                            f"{F.RED}エラー： ページ数が無効である。{END}"
                        )
                    )
            elif type(pageInput) == str:
                if re.fullmatch(pageNumRegex, pageInput) == None:
                    print_in_both_en_jp(
                        en=(
                            f"{F.RED}Error: Invalid format.{END}"
                        ),
                        jp=(
                            f"{F.RED}エラー： ページ数が無効である。{END}"
                        )
                    )
                else:
                    if type(userURLInput) == str:
                        return pageInput
                    else:
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: The number of URLs entered is different from the number of pages entered.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： URLの個数とページ数の個数が違います。{END}"
                            )
                        )
            else:
                raise Exception("pageInput variable for downloading fantia posts is not a list or string...")

def print_menu():
    """
    To print out the menu which will reflects any changes based on certain conditions such as whether the user is logged in, etc.
    """
    if not fantiaCookieLoaded: 
        if lang == "en": fantiaStatus = "Guest (Not logged in)"
        elif lang == "jp": fantiaStatus = "ゲスト（ログインしていない）"
    else:
        if lang == "en": fantiaStatus = "Logged in via cookies"
        elif lang == "jp": fantiaStatus = "クッキーでログインしました"
        
    if not pixivCookieLoaded: 
        if lang == "en": pixivStatus = "Guest (Not logged in)"
        elif lang == "jp": pixivStatus = "ゲスト（ログインしていない）"
    else:
        if lang == "en": pixivStatus = "Logged in via cookies"
        elif lang == "jp": pixivStatus = "クッキーでログインしました"

    if lang == "jp": 
        menuHead = f"""{F.LIGHTYELLOW_EX}
> ログイン・ステータス...
> Fantia: {fantiaStatus}
> Pixiv: {pixivStatus}
{END}
--------------------- {F.LIGHTYELLOW_EX}ダウンロードのオプション{END} ---------------------
      {F.GREEN}1. Fantia投稿URLから画像をダウンロードする{END}
      {F.GREEN}2. 全投稿ページのURLからFantiaの全投稿をダウンロードする。{END}
      {F.CYAN}3. Pixivファンボックスの投稿URLから画像をダウンロードする{END}
      {F.CYAN}4. 全投稿ページのURLからPixivファンボックスの全投稿をダウンロードする。{END}

---------------------- {F.LIGHTYELLOW_EX}コンフィグのオプション{END} ----------------------
      {F.LIGHTBLUE_EX}5. デフォルトのダウンロードフォルダを変更する{END}
      {F.LIGHTBLUE_EX}6. ブラウザを変更する{END}
      {F.LIGHTBLUE_EX}7. 言語を変更する{END}
"""
        if fantiaStatus == "ゲスト（ログインしていない）" or pixivStatus == "ゲスト（ログインしていない）":
            menuAdditionalOptions = f"""      {F.LIGHTBLUE_EX}8. ログインする{END}\n"""
        else:
            menuAdditionalOptions = ""

        menuFooterStart = f"""
-------------------------- {F.LIGHTYELLOW_EX}他のオプション{END} ---------------------------"""
        if appPath.joinpath("configs", "pixiv_cookies").is_file() or appPath.joinpath("configs", "fantia_cookies").is_file(): 
            menuDeleteCookieOption = f"""\n      {F.LIGHTRED_EX}DC. 保存されたクッキーを削除する{END}"""
        else: 
            menuDeleteCookieOption = ""

        if check_if_directory_has_files(appPath.joinpath("configs")): 
            menuDeleteDataOption = f"""\n      {F.RED}D. Cultured Downloaderで作成されたデータをすべて削除します。{END}\n"""
        else: 
            menuDeleteDataOption = "\n"

        menuFooterEnd = f"""      {F.LIGHTRED_EX}Y. バグを報告する{END}
      {F.RED}X. プログラムを終了する{END}
 """
    else:
        menuHead = f"""{F.LIGHTYELLOW_EX}
> Login Status...
> Fantia: {fantiaStatus}
> Pixiv: {pixivStatus}
{END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{END} --------------------
      {F.GREEN}1. Download images from a Fantia post URL{END}
      {F.GREEN}2. Download all Fantia posts from an all posts page URL{END}
      {F.CYAN}3. Download images from a pixiv Fanbox post URL{END}
      {F.CYAN}4. Download all pixiv Fanbox posts from an all posts page URL{END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{END} ----------------------
      {F.LIGHTBLUE_EX}5. Change Default Download Folder{END}
      {F.LIGHTBLUE_EX}6. Change Default Browser{END}
      {F.LIGHTBLUE_EX}7. Change Language{END}
"""
        if fantiaStatus == "Guest (Not logged in)" or pixivStatus == "Guest (Not logged in)":
            menuAdditionalOptions = f"""      {F.LIGHTBLUE_EX}8. Login{END}\n"""
        else:
            menuAdditionalOptions = ""

        menuFooterStart = f"""
---------------------- {F.LIGHTYELLOW_EX}Other Options{END} ----------------------"""
        if appPath.joinpath("configs", "pixiv_cookies").is_file() or appPath.joinpath("configs", "fantia_cookies").is_file(): 
            menuDeleteCookieOption = f"""\n      {F.LIGHTRED_EX}DC. Delete saved cookies{END}"""
        else:
            menuDeleteCookieOption = ""

        if check_if_directory_has_files(appPath.joinpath("configs")): 
            menuDeleteDataOption = f"""\n      {F.RED}D. Delete all data created by Cultured Downloader{END}\n"""
        else: 
            menuDeleteDataOption = "\n"

        menuFooterEnd = f"""      {F.LIGHTRED_EX}Y. Report a bug{END}
      {F.RED}X. Shutdown the program{END}
 """
        
    print("".join([menuHead, menuAdditionalOptions, menuFooterStart, menuDeleteCookieOption, menuDeleteDataOption, menuFooterEnd]))

"""--------------------------- End of Functions Codes ---------------------------"""

"""--------------------------- Start of Main Codes ---------------------------"""

def main():
    """
    The main code of the program.
    """
    pythonMainVer = sys.version_info[0]
    pythonSubVer = sys.version_info[1]
    if pythonMainVer < 3 or pythonSubVer < 8:
        print(f"{F.RED}Fatal Error: This program requires running Python 3.8 or higher!", f"You are running Python {pythonMainVer}.{pythonSubVer}{F.RESET}"),
        print("{F.RED}致命的なエラー： このプログラムにはPython 3.8以上が必要です。", f"あなたはPython {pythonMainVer}.{pythonSubVer}を実行しています。{F.RESET}")
        input("Please enter any key to exit/何か入力すると終了します...")
        raise SystemExit

    # declare global variables
    global appPath
    global jsonPath
    global decKey
    global driver
    global lang
    global selectedBrowser
    global ChaChaKey

    global fantiaDownloadLocation
    global pixivDownloadLocation
    global browserDownloadLocation

    global pixivCookieLoaded
    global fantiaCookieLoaded
    global pixivSession

    appPath = get_saved_config_data_folder()
    jsonPath = appPath.joinpath("configs", "config.json")

    ChaChaKey = get_key()

    # checks if config.json exists and the necessary configs are defined
    check_if_json_file_exists()

    lang = get_lang()
    print_in_both_en_jp(
        en=(f"{F.LIGHTYELLOW_EX}Running program...{END}"),
        jp=(f"{F.LIGHTYELLOW_EX}プログラムを実行する...{END}")
    )

    directoryPath = get_default_download_directory()

    fantiaDownloadLocation = directoryPath.joinpath("fantia_downloads")
    fantiaDownloadLocation.mkdir(parents=True, exist_ok=True)

    pixivDownloadLocation = directoryPath.joinpath("pixiv_downloads")
    pixivDownloadLocation.mkdir(parents=True, exist_ok=True)

    browserDownloadLocation = directoryPath.joinpath("browser_downloads")
    browserDownloadLocation.mkdir(parents=True, exist_ok=True)

    # get the preferred browser
    loadBrowser = check_browser_config()
    if loadBrowser == None:
        selectedBrowser = get_browser_preferences()
        driver = get_driver(selectedBrowser)
    else: 
        selectedBrowser = loadBrowser
        driver = get_driver(loadBrowser)

    # retrieve cookie if exists
    pixivCookieLoaded = fantiaCookieLoaded = False

    fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
    pixivCookiePath = appPath.joinpath("configs", "pixiv_cookies")

    fantiaCookieExist = fantiaCookiePath.is_file()
    pixivCookieExist = pixivCookiePath.is_file()

    if fantiaCookieExist or pixivCookieExist:    
        if lang == "en": cookiePrompt = "Would you like to load in your existing cookies? (y/n): "
        else: cookiePrompt = "保存されたクッキーを読み込みますか？ (y/n)： "
        userCookieInput = get_input_from_user(prompt=cookiePrompt, command=("y", "n"))
        if userCookieInput == "y":
            if pixivCookieExist: pixivCookieLoaded = load_cookie("pixiv")
            if fantiaCookieExist: fantiaCookieLoaded = load_cookie("fantia")
        else:
            print_in_both_en_jp(
                en=(f"{F.YELLOW}Saved cookies will not be loaded into the webdriver...{END}"),
                jp=(f"{F.YELLOW}その場合、保存されたクッキーは読み込まれません...{END}")
            )
    if not fantiaCookieLoaded or not pixivCookieLoaded:
        print("\n")
        if lang == "en": loginPrompt = "Would you like to login? (y/n): "
        else: loginPrompt = "ログインしますか？ (y/n)： "
        loginInput = get_input_from_user(prompt=loginPrompt, command=("y", "n"))
        if loginInput == "y":
            # gets account details for Fantia and Pixiv for downloading images that requires a membership
            if not pixivCookieLoaded:
                pixivCookieLoaded, pixivSessionID = save_and_load_cookie(driver, "pixiv", getID=True)
            if not fantiaCookieLoaded:
                fantiaCookieLoaded = save_and_load_cookie(driver, "fantia")

    if pixivCookieLoaded and pixivCookieExist: pixivSession = get_cookie_for_session("pixiv")
    elif pixivCookieLoaded and not pixivCookieExist: pixivSession = get_cookie_for_session("pixiv", sessionID=pixivSessionID)
    else: pixivSession = None # None instead of "" so that it won't raise a SessionError

    if pixivSession == "": raise SessionError

    cmdInput = ""
    cmdCommands = ("1", "2", "3", "4", "5", "6", "7", "8", "d", "dc", "x", "y")
    while cmdInput != "x":
        print_menu()
        if lang == "en":
            cmdInput = get_input_from_user(prompt="Enter command: ", command=cmdCommands, warning="Invalid command input, please enter a valid command from the menu above.")
        else:
            cmdInput = get_input_from_user(prompt="コマンドを入力してください： ", command=cmdCommands, warning="不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。")

        if cmdInput == "1":
            imagePath = create_subfolder("fantia")
            if imagePath != "X":
                startDownloadingFlag = True
                print("\n")
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}This option is for URL such as\nhttps://fantia.jp/posts/1147606{END}"), 
                    jp=(f"{F.LIGHTYELLOW_EX}このオプションは、\nhttps://fantia.jp/posts/1147606 のようなURLのためのものです。{END}")
                )
                while True:
                    print_in_both_en_jp(
                        en=(
                            f"{F.LIGHTYELLOW_EX}You can put multiple urls as well by entering a comma in between each urls...{END}",
                            f"{F.LIGHTYELLOW_EX}For example,\n\"https://fantia.jp/posts/1147606, https://fantia.jp/posts/1086639\"{END}"
                        ), 
                        jp=(
                            f"{F.LIGHTYELLOW_EX}各URLの間にカンマを入力することで、複数のURLを入れることも可能です...{END}",
                            f"{F.LIGHTYELLOW_EX}例えば、\n\"https://fantia.jp/posts/1147606, https://fantia.jp/posts/1086639\"{END}"
                        )
                    )
                    if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of the Fantia post (X to cancel): "))
                    else: urlInput = split_inputs_to_possible_multiple_inputs(input("Fantiaの投稿のURLを入力します (Xでキャンセル)： "))

                    if urlInput == "x" or urlInput == "X": 
                        startDownloadingFlag = False
                        break

                    if (urlInput == "") or (check_if_input_is_url(urlInput, "fantiaPost") == False):
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: No URL entered or URL entered is/are invalid.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： URLが入力されていない、または入力されたURLが無効である。{END}"
                            )
                        )
                    else: break

                if startDownloadingFlag:
                    if lang == "en": attachmentPrompt = "Would you like to download attachments such as psd files, videos, gifs (if found)? (y/n): "
                    else: attachmentPrompt = "psdファイルや動画ファイルやgifファイルをダウンロードしますか (見つかった場合)？ (y/n): "
                    downloadAttachmentFlag = get_input_from_user(prompt=attachmentPrompt, command=("y", "n"))

                    if downloadAttachmentFlag == "y": downloadAttachmentFlag = True
                    else: downloadAttachmentFlag = False

                    if type(urlInput) == list: numOfPosts = len(urlInput)
                    else: numOfPosts = 1
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.YELLOW}Please wait as auto downloading files from Fantia can take quite a while if the file size is large...{END}",
                            f"{F.YELLOW}The program will automatically download files from {numOfPosts} posts.{END}",
                            f"{F.YELLOW}If it freezes, fret not! It's in the midst of downloading large files.\nJust let it run and do not terminate the program! Otherwise you will have to restart the download again.{END}"
                        ),
                        jp=(
                            f"{F.YELLOW}Fantiaからのファイルの自動ダウンロードは、ファイルサイズが大きい場合、かなり時間がかかるので、お待ちください...{END}",
                            f"{F.YELLOW}このプログラムは、{numOfPosts}投稿の中からファイルを自動的にダウンロードします。{END}",
                            f"{F.YELLOW}フリーズしても大丈夫! 大きなファイルをダウンロードしている最中なのです。\nそのまま実行させ、プログラムを終了させないでください! そうしないと、またダウンロードを再開しなければならなくなります。{END}"
                        )
                    )
                    print("\n")
                    
                    if type(urlInput) == list:
                        counter = 0
                        for url in urlInput: 
                            downloadDirectoryFolder = imagePath.joinpath(f"Post_{counter}")
                            download(url, "FantiaPost", downloadDirectoryFolder, attachments=downloadAttachmentFlag)
                            counter += 1
                    else: download(urlInput, "FantiaPost", imagePath, attachments=downloadAttachmentFlag)

        elif cmdInput == "2":
            imagePath = create_subfolder("fantia")
            if imagePath != "X":
                startDownloadingFlag = True
                print("\n")
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}This option is for URL such as https://fantia.jp/fanclubs/5744/posts{END}"), 
                    jp=(f"{F.LIGHTYELLOW_EX}このオプションは、https://fantia.jp/fanclubs/5744/posts のようなURLのためのものです。{END}")
                )
                while True:
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.LIGHTYELLOW_EX}However, please enter the base URL first! (e.g. https://fantia.jp/fanclubs/5744/posts){END}",
                            f"{F.LIGHTYELLOW_EX}For multiple inputs, please add a comma in between the urls.\n(e.g. https://fantia.jp/fanclubs/5744/posts, https://fantia.jp/fanclubs/14935/posts){END}",
                            f"{F.LIGHTYELLOW_EX}Afterwards, you will be prompted to enter the number of pages in this format, \"1-5\" or \"5\" to indicate page 1 to 5 or page 5 respectively.{END}"
                        ), 
                        jp=(
                            f"{F.LIGHTYELLOW_EX}ただし、最初にベースURLを入力してください (例: https://fantia.jp/fanclubs/5744/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}複数のURLを入力する場合は、URLの後にコンマを入力してください。\n(例: https://fantia.jp/fanclubs/5744/posts、https://fantia.jp/fanclubs/14935/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}その後、ページ数を入力する画面になるので、1～5ページを示す \"1-5\"やページ5を示す\"5\"を入力下さい。{END}"
                        )
                    )
                    if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of Fantia's all posts page (X to cancel): "))
                    else: urlInput = split_inputs_to_possible_multiple_inputs(input("Fantiaの全投稿ページのURLを入力下さい (Xでキャンセル)： "))

                    if urlInput == "x" or urlInput == "X": 
                        startDownloadingFlag = False
                        break

                    if (urlInput == "") or (check_if_input_is_url(urlInput, "fantiaPostPage") == False):
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: No URL entered or URL entered is/are invalid.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： URLが入力されていない、または入力されたURLが無効である。{END}"
                            )
                        )
                    else: break
                
                # asking the user for the number of pages to download
                if startDownloadingFlag:
                    pageInput = get_page_num(urlInput)
                    if not pageInput: startDownloadingFlag = False

                if startDownloadingFlag:
                    fantiaPostPreviewURLArray = []
                    if type(pageInput) == str and type(urlInput) == str:
                        try:
                            pageNum = int(pageInput)
                            fantiaPostPreviewURLArray.append("".join([urlInput, "?page=", str(pageNum)]))
                        except:
                            pageNumList = pageInput.split("-")
                            pageNumList.sort()
                            for i in range(int(pageNumList[0]), int(pageNumList[1]) + 1):
                                fantiaPostPreviewURLArray.append("".join([urlInput, "?page=", str(i)]))
                    elif type(pageInput) == list and type(urlInput) == list:
                        arrayPointer = 0
                        for pageNumInput in pageInput:
                            try:
                                pageNum = int(pageNumInput)
                                fantiaPostPreviewURLArray.append("".join([urlInput[arrayPointer], "?page=", str(pageNum)]))
                            except:
                                pageNumList = pageNumInput.split("-")
                                pageNumList.sort()
                                for i in range(int(pageNumList[0]), int(pageNumList[1]) + 1):
                                    fantiaPostPreviewURLArray.append("".join([urlInput[arrayPointer], "?page=", str(i)]))
                            
                            arrayPointer += 1
                    else:
                        raise Exception("Fantia posts download's variables are not in correct format...")

                    if lang == "en": attachmentPrompt = "Would you like to download attachments such as psd files, videos, gifs (if found)? (y/n): "
                    else: attachmentPrompt = "psdファイルや動画ファイルやgifファイルをダウンロードしますか (見つかった場合)？ (y/n): "
                    downloadAttachmentFlag = get_input_from_user(prompt=attachmentPrompt, command=("y", "n"))

                    if downloadAttachmentFlag == "y": downloadAttachmentFlag = True
                    else: downloadAttachmentFlag = False

                    if type(urlInput) == list: numOfPostPage = len(urlInput)
                    else: numOfPostPage = 1
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.YELLOW}Please wait as auto downloading files from Fantia can take quite a while if the file size is large...{END}",
                            f"{F.YELLOW}The program will automatically download files from {numOfPostPage} all posts preview pages.{END}",
                            f"{F.YELLOW}If it freezes, fret not! It's in the midst of downloading large files.\nJust let it run and do not terminate the program! Otherwise you will have to restart the download again.{END}"
                        ),
                        jp=(
                            f"{F.YELLOW}Fantiaからのファイルの自動ダウンロードは、ファイルサイズが大きい場合、かなり時間がかかるので、お待ちください...{END}",
                            f"{F.YELLOW}このプログラムは、{numOfPostPage}件の投稿プレビューページから自動的にファイルをダウンロードする。{END}",
                            f"{F.YELLOW}フリーズしても大丈夫! 大きなファイルをダウンロードしている最中なのです。\nそのまま実行させ、プログラムを終了させないでください! そうしないと、またダウンロードを再開しなければならなくなります。{END}"
                        )
                    )
                    print("\n")
                    postURLToDownloadArray = []
                    for postURL in fantiaPostPreviewURLArray: 
                        driver.get(postURL)
                        sleep(3)
                        try: posts = driver.find_elements(by=By.XPATH, value="//a[@class='link-block']")
                        except: posts = []

                        for postAnchorEl in posts:
                            postURLToDownloadArray.append(postAnchorEl.get_attribute("href"))

                    if postURLToDownloadArray:
                        counter = 0
                        for postURL in postURLToDownloadArray:
                            downloadDirectoryFolder = imagePath.joinpath(f"Post_{counter}")
                            download(postURL, "FantiaPost", downloadDirectoryFolder, attachments=downloadAttachmentFlag)
                            counter += 1
                    else:
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: No posts found on the given URL.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： 指定されたURLに投稿が見つかりませんでした。{END}"
                            )
                        )

        elif cmdInput == "3":
            imagePath = ""
            if pixivSession != "": imagePath = create_subfolder("pixiv")
            if imagePath != "X":
                startDownloadingFlag = True
                print("\n")
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}This option is for URL such as\nhttps://www.fanbox.cc/@gmkj0324/posts/3103384{END}"), 
                    jp=(f"{F.LIGHTYELLOW_EX}このオプションは、\nhttps://www.fanbox.cc/@gmkj0324/posts/3103384 のようなURLのためのものです。{END}")
                )
                while True:
                    print_in_both_en_jp(
                        en=(
                            f"{F.LIGHTYELLOW_EX}You can put multiple urls as well by entering a comma in between each urls...{END}",
                            f"{F.LIGHTYELLOW_EX}For example,\n\"https://www.fanbox.cc/@gmkj0324/posts/3103384, https://www.fanbox.cc/@gmkj0324/posts/3072263\"{END}"
                        ), 
                        jp=(
                            f"{F.LIGHTYELLOW_EX}各URLの間にカンマを入力することで、複数のURLを入れることも可能です...{END}",
                            f"{F.LIGHTYELLOW_EX}例えば、\n\"https://www.fanbox.cc/@gmkj0324/posts/3103384, https://www.fanbox.cc/@gmkj0324/posts/3072263\"{END}"
                        )
                    )
                    if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of the Pixiv Fanbox post (X to cancel): "))
                    else: urlInput = split_inputs_to_possible_multiple_inputs(input("Pixivファンボックスの投稿URLを入力してください (Xでキャンセル)： "))

                    if urlInput == "x" or urlInput == "X":
                        startDownloadingFlag = False
                        break

                    if (urlInput == "") or (check_if_input_is_url(urlInput, "pixivFanbox") == False): 
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: No URL entered or URL entered is/are invalid.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： URLが入力されていない、または入力されたURLが無効である。{END}"
                            )
                        )
                    else: break

                if startDownloadingFlag:
                    if lang == "en": attachmentPrompt = "Would you like to download attachments such as psd files, videos, gifs (if found)? (y/n): "
                    else: attachmentPrompt = "psdファイルや動画ファイルやgifファイルをダウンロードしますか (見つかった場合)？ (y/n): "
                    downloadAttachmentFlag = get_input_from_user(prompt=attachmentPrompt, command=("y", "n"))

                    if downloadAttachmentFlag == "y": downloadAttachmentFlag = True
                    else: downloadAttachmentFlag = False

                    if type(urlInput) == list: numOfPosts = len(urlInput)
                    else: numOfPosts = 1
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.YELLOW}Please wait as auto downloading files from pixiv can take quite a while if the file size is large...{END}",
                            f"{F.YELLOW}The program will automatically download files from {numOfPosts} posts.{END}",
                            f"{F.YELLOW}If it freezes, fret not! It's in the midst of downloading large files.\nJust let it run and do not terminate the program! Otherwise you will have to restart the download again.{END}"
                        ),
                        jp=(
                            f"{F.YELLOW}pixivからのファイルの自動ダウンロードは、ファイルサイズが大きい場合、かなり時間がかかるので、お待ちください...{END}",
                            f"{F.YELLOW}このプログラムは、{numOfPosts}投稿の中からファイルを自動的にダウンロードします。{END}",
                            f"{F.YELLOW}フリーズしても大丈夫! 大きなファイルをダウンロードしている最中なのです。\nそのまま実行させ、プログラムを終了させないでください! そうしないと、またダウンロードを再開しなければならなくなります。{END}"
                        )
                    )
                    print("\n")
                    if type(urlInput) == list:
                        counter = 1
                        for url in urlInput:
                            downloadDirectoryFolder = imagePath.joinpath(f"Post_{counter}")
                            download(url, "Pixiv", downloadDirectoryFolder, attachments=downloadAttachmentFlag)
                            counter += 1
                    else:
                        download(urlInput, "Pixiv", imagePath, attachments=downloadAttachmentFlag)
        
        elif cmdInput == "4":
            imagePath = create_subfolder("pixiv")
            if imagePath != "X":
                startDownloadingFlag = True
                print("\n")
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}This option is for URL such as https://www.fanbox.cc/@creator_name/posts{END}"), 
                    jp=(f"{F.LIGHTYELLOW_EX}このオプションは、https://www.fanbox.cc/@creator_name/posts のようなURLのためのものです。{END}")
                )
                while True:
                    print_in_both_en_jp(
                        en=(
                            f"{F.LIGHTYELLOW_EX}However, please enter the base URL first! (e.g. https://www.fanbox.cc/@creator_name/posts){END}",
                            f"{F.LIGHTYELLOW_EX}For multiple inputs, please add a comma in between the urls.\n(e.g. https://www.fanbox.cc/@creator_name_one/posts, https://www.fanbox.cc/@creator_name_two/posts){END}",
                            f"{F.LIGHTYELLOW_EX}Afterwards, you will be prompted to enter the number of pages in this format, \"1-5\" or \"5\" to indicate page 1 to 5 or page 5 respectively.{END}"
                        ), 
                        jp=(
                            f"{F.LIGHTYELLOW_EX}ただし、最初にベースURLを入力してください (例: https://www.fanbox.cc/@creator_name/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}複数のURLを入力する場合は、URLの後にコンマを入力してください。\n(例: https://www.fanbox.cc/@creator_name_one/posts、https://www.fanbox.cc/@creator_name_two/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}その後、ページ数を入力する画面になるので、1～5ページを示す \"1-5\"やページ5を示す\"5\"を入力下さい。{END}"
                        )
                    )
                    if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of the pixiv Fanbox all posts page (X to cancel): "))
                    else: urlInput = split_inputs_to_possible_multiple_inputs(input("pixivファンボックスの全投稿ページのURLを入力下さい (Xでキャンセル)： "))

                    if urlInput == "x" or urlInput == "X": 
                        startDownloadingFlag = False
                        break

                    if (urlInput == "") or (check_if_input_is_url(urlInput, "pixivFanboxPostPage") == False):
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: No URL entered or URL entered is/are invalid.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： URLが入力されていない、または入力されたURLが無効である。{END}"
                            )
                        )
                    else: break
                
                # asking the user for the number of pages to download
                if startDownloadingFlag:
                    pageInput = get_page_num(urlInput)
                    if not pageInput: startDownloadingFlag = False

                if startDownloadingFlag:
                    pixivPostPreviewURLArray = []
                    if type(pageInput) == str and type(urlInput) == str:
                        try:
                            pageNum = int(pageInput)
                            pixivPostPreviewURLArray.append("".join([urlInput, "?page=", str(pageNum)]))
                        except:
                            pageNumList = pageInput.split("-")
                            pageNumList.sort()
                            for i in range(int(pageNumList[0]), int(pageNumList[1]) + 1):
                                pixivPostPreviewURLArray.append("".join([urlInput, "?page=", str(i)]))
                    elif type(pageInput) == list and type(urlInput) == list:
                        arrayPointer = 0
                        for pageNumInput in pageInput:
                            try:
                                pageNum = int(pageNumInput)
                                pixivPostPreviewURLArray.append("".join([urlInput[arrayPointer], "?page=", str(pageNum)]))
                            except:
                                pageNumList = pageNumInput.split("-")
                                pageNumList.sort()
                                for i in range(int(pageNumList[0]), int(pageNumList[1]) + 1):
                                    pixivPostPreviewURLArray.append("".join([urlInput[arrayPointer], "?page=", str(i)]))
                            
                            arrayPointer += 1
                    else:
                        raise Exception("pixiv Fanbox posts download's variables are not in correct format...")

                    if lang == "en": attachmentPrompt = "Would you like to download attachments such as psd files, videos, gifs (if found)? (y/n): "
                    else: attachmentPrompt = "psdファイルや動画ファイルやgifファイルをダウンロードしますか (見つかった場合)？ (y/n): "
                    downloadAttachmentFlag = get_input_from_user(prompt=attachmentPrompt, command=("y", "n"))

                    if downloadAttachmentFlag == "y": downloadAttachmentFlag = True
                    else: downloadAttachmentFlag = False

                    if type(urlInput) == list: numOfPostPage = len(urlInput)
                    else: numOfPostPage = 1
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.YELLOW}Please wait as auto downloading files from pixiv can take quite a while if the file size is large...{END}",
                            f"{F.YELLOW}The program will automatically download files from {numOfPostPage} all posts preview pages.{END}",
                            f"{F.YELLOW}If it freezes, fret not! It's in the midst of downloading large files.\nJust let it run and do not terminate the program! Otherwise you will have to restart the download again.{END}"
                        ),
                        jp=(
                            f"{F.YELLOW}pixivからのファイルの自動ダウンロードは、ファイルサイズが大きい場合、かなり時間がかかるので、お待ちください...{END}",
                            f"{F.YELLOW}このプログラムは、{numOfPostPage}件の投稿プレビューページから自動的にファイルをダウンロードする。{END}",
                            f"{F.YELLOW}フリーズしても大丈夫! 大きなファイルをダウンロードしている最中なのです。\nそのまま実行させ、プログラムを終了させないでください! そうしないと、またダウンロードを再開しなければならなくなります。{END}"
                        )
                    )
                    print("\n")
                    postURLToDownloadArray = []
                    for postURL in pixivPostPreviewURLArray: 
                        driver.get(postURL)
                        sleep(3)
                        try: posts = driver.find_elements(by=By.XPATH, value="//a[@class='sc-1bjj922-0 gwbPAH']")
                        except: posts = []

                        for postAnchorEl in posts:
                            postURLToDownloadArray.append(postAnchorEl.get_attribute("href"))

                    if postURLToDownloadArray:
                        counter = 0
                        for postURL in postURLToDownloadArray:
                            downloadDirectoryFolder = imagePath.joinpath(f"Post_{counter}")
                            download(postURL, "Pixiv", downloadDirectoryFolder, attachments=downloadAttachmentFlag)
                            counter += 1
                    else:
                        print_in_both_en_jp(
                            en=(
                                f"{F.RED}Error: No posts found on the given URL.{END}"
                            ),
                            jp=(
                                f"{F.RED}エラー： 指定されたURLに投稿が見つかりませんでした。{END}"
                            )
                        )

        elif cmdInput == "5":
            with open(jsonPath, "r") as f:
                config = json.load(f)

            set_default_download_directory(config, setDefaultLocationUponCancellation=False)
            
        elif cmdInput == "6":
            defaultBrowser = check_browser_config()
            if defaultBrowser != None:
                newDefaultBrowser = get_user_browser_preference()
                save_browser_config(newDefaultBrowser)
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Error: No default browser found.{END}"),
                    jp=(f"{F.RED}エラー： デフォルトのブラウザが見つかりませんでした。{END}")
                )

                if lang == "en": browserPrompt = "Would you like to save a browser as your default browser for this program? (y/n): "
                else: browserPrompt = "このプログラムのデフォルトのブラウザを保存しますか？ (y/n): "
                saveBrowser = get_input_from_user(prompt=browserPrompt, command=("y", "n"))

                if saveBrowser == "y":
                    newDefaultBrowser = get_user_browser_preference()
                    save_browser_config(newDefaultBrowser)
                else: print_in_both_en_jp(
                        en=(f"{F.LIGHTRED_EX}Note: Default Browser is empty in config.json{END}"),
                        jp=(f"{F.LIGHTRED_EX}注意： config.jsonのデフォルトブラウザが空です。{END}")
                    )

        elif cmdInput == "7":
            lang = update_lang()

        elif cmdInput == "8":
            if not check_if_user_is_logged_in():
                pixivCookieExist = appPath.joinpath("configs", "pixiv_cookies").is_file()
                if not pixivCookieLoaded and not pixivCookieExist:
                    pixivCookieLoaded, pixivSessionID = save_and_load_cookie(driver, "pixiv", getID=True)
                    if pixivCookieLoaded: pixivSession = get_cookie_for_session("pixiv", sessionID=pixivSessionID)
                elif not pixivCookieLoaded and pixivCookieExist:
                    pixivCookieLoaded = save_and_load_cookie(driver, "pixiv")
                    if pixivCookieLoaded: pixivSession = get_cookie_for_session("pixiv")

                if not fantiaCookieLoaded:
                    fantiaCookieLoaded = save_and_load_cookie(driver, "fantia")
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )

        elif cmdInput == "d":
            if check_if_directory_has_files(appPath.joinpath("configs")):
                for folderPath in appPath.iterdir():
                    if folderPath.is_dir():
                        rmtree(folderPath)
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}Deleted folders in {appPath}{END}"),
                    jp=(f"{F.LIGHTYELLOW_EX}{appPath} 内のフォルダーを削除しました。{END}")
                )
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )
                
        elif cmdInput == "dc":
            if pixivCookiePath.exists() or fantiaCookiePath.exists():
                pixivCookiePath = appPath.joinpath("configs", "pixiv_cookies")
                if pixivCookiePath.is_file():
                    pixivCookiePath.unlink()
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTYELLOW_EX}Deleted Pixiv Fanbox cookies{END}"),
                        jp=(f"{F.LIGHTYELLOW_EX}Pixivファンボックスのクッキーが削除されました。{END}")
                    )
                
                fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
                if fantiaCookiePath.is_file():
                    fantiaCookiePath.unlink()
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTYELLOW_EX}Deleted Fantia cookies{END}"),
                        jp=(f"{F.LIGHTYELLOW_EX}Fantiaのクッキーが削除されました。{END}")
                    )
    
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )

        elif cmdInput == "y": webbrowser.open("https://github.com/KJHJason/Cultured-Downloader/issues", new=2)
        elif cmdInput == "x": driver.quit()

"""--------------------------- End of Main Codes ---------------------------"""

if __name__ == "__main__":
    coloramaInit(autoreset=False, convert=True)
    global END
    END = Style.RESET_ALL

    global fantiaPostRegex
    global fantiaImageURLRegex
    global fantiaPostPageRegex
    global pixivFanboxPostRegex
    global pixivFanboxPostPageRegex
    global pageNumRegex

    fantiaPostRegex = re.compile(r"(https://fantia.jp/posts/)\d{1,}")
    fantiaImageURLRegex = re.compile(r"(https://fantia.jp/posts/)\d{1,}(/post_content_photo/)\d{1,}")
    fantiaPostPageRegex = re.compile(r"(https://fantia.jp/fanclubs/)\d{1,}(/posts)")
    pixivFanboxPostRegex = re.compile(r"(https://www.fanbox.cc/@)\w{1,}(/posts/)\d{1,}")
    pixivFanboxPostPageRegex = re.compile(r"(https://www.fanbox.cc/@)\w{1,}(/posts)") 
    pageNumRegex = re.compile(r"\d{1,}(-)\d{1,}|\d{1,}")

    introMenu = f"""
=========================================== {F.LIGHTBLUE_EX}CULTURED DOWNLOADER v{__version__ }{END} ===========================================
================================ {F.LIGHTBLUE_EX}https://github.com/KJHJason/Cultured-Downloader{END} =================================
===================================== {F.LIGHTBLUE_EX}Author/開発者: {__author__}, aka Dratornic{END} =====================================
{F.LIGHTYELLOW_EX}
Purpose/目的: Allows you to download multiple images from Fantia or Pixiv Fanbox automatically.
              FantiaやPixivファンボックスから複数の画像を自動でダウンロードできるようにします。

Note/注意: Requires the user to login via this program for images that requires a membership.
           This program is not affiliated with Pixiv or Fantia.
           会員登録が必要な画像は、本プログラムによるログインが必要です。
           このプログラムはPixivやFantiaとは関係ありません。{END}
{F.LIGHTRED_EX}
For English-speaking users:
If you have noticed the weird "?" text, it means that your PC do not have Japanese language support.
You can simply ignore it or install the Japanese language pack via Settings on your PC.{END}
{F.RED}
Warning/警告:
Please read the term of use at https://github.com/KJHJason/Cultured-Downloader before using this program.
本プログラムをご利用になる前に、https://github.com/KJHJason/Cultured-Downloader の利用規約をお読みください。{END}
"""
    print(introMenu)
    try:
        main()
    except SystemExit:
        try: driver.quit()
        except: pass
        
        print(f"{F.RED}Exiting/終了しています...{END}")
        osExit(1)
    except KeyboardInterrupt:
        print(f"\n{F.RED}Program Terminated/プログラムが終了しました{END}")
        print(f"{F.RED}Exiting/終了しています...{END}")
        try: driver.quit()
        except: pass
        
        sleep(1)
        osExit(0)
    except (EncryptionKeyError, DecryptError):
        try: driver.quit()
        except: pass
        
        delete_encrypted_data()
        osExit(1)
    except (SessionError, EOFError):
        try: driver.quit()
        except: pass

        # deletes any saved files created by this program
        remove_any_files_in_directory(get_saved_config_data_folder().joinpath("configs"))

        print_in_both_en_jp(
            en=(f"{F.RED}Error: Unable to read saved files...{END}", f"Please restart this program.{END}", "Please enter any key to exit..."),
            jap=(f"{F.RED}エラー：  保存したファイルを読み込めない...{END}", "このプログラムを再起動してください。{END}", "何か入力すると終了します...")
        )
        input()
        osExit(1)
    except:
        try: driver.quit()
        except: pass

        print_error_log_notification()
        log_error()

        input("Please enter any key to exit/何か入力すると終了します...")
        osExit(1)

    shutdown()