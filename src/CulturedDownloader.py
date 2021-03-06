# Import Standard Library, os, to close the program
from os import _exit as osExit

try:
    import Header
    __author__ = Header.__author__
    __copyright__ = Header.__copyright__
    __license__ = Header.__license__
    __version__ = Header.__version__
except (ImportError, ModuleNotFoundError):
    print("Could not import Header module/Header モジュールのインポートに失敗しました...")
    input("Please enter any key to exit/何か入力すると終了します...")
    osExit()

# Import Third-party Libraries
try:
    import requests, dill, gdown
    from colorama import init as coloramaInit
    from colorama import Style
    from colorama import Fore as F
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
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
    from os import devnull
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

def check_for_new_ver():
    """
    Checks for a new update and if the program is up to date.
    
    Will print out some messages for the user to inform them of the update.
    """
    res = requests.get("https://api.github.com/repos/KJHJason/Cultured-Downloader/releases/latest").json()
    latestVer = res["tag_name"]
    print("-" * 100)
    print(f"\n{F.LIGHTYELLOW_EX}Checking for updates/更新を確認しています...{END}")
    if latestVer != __version__:
        print(f"\n{F.RED}New version of Cultured Downloader is available/新しいバージョンのCultured Downloaderが利用可能です{END}\n")
        print(f"{F.RED}Current version/現在のバージョン: {__version__}{END}")
        print(f"{F.RED}Latest version/最新のバージョン: {latestVer}{END}\n")
        print(f"{F.RED}Please update the program/プログラムを更新してください{END}\n")
        print(f"{F.RED}Link to the latest version/最新バージョンへのリンク:{END}")
        print(f"{F.RED}{res['html_url']}{END}\n")
    else: 
        print(f"{F.GREEN}You are using the latest version/最新バージョンを使用しています{END}\n")
    print("-" * 100)
    print()

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

def print_error_log_notification():
    """
    Used for alerting the user of where the log file is located at and to report this bug to the developer.
    """
    logFolderPath = get_saved_config_data_folder().joinpath("logs")
    print(f"\n{F.RED}Unknown Error Occurred/不明なエラーが発生した{END}")
    print(f"{F.RED}Please provide the developer with a error text file generated in {logFolderPath}\n{logFolderPath}に生成されたエラーテキストファイルを開発者に提供してください。\n{END}")

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
            f.write("\n\n")

    logging.basicConfig(filename=fullFilePath, filemode="a", format="%(asctime)s - %(message)s")
    logging.error("Error Details: ", exc_info=True)

def error_shutdown(**errorMessages):
    """
    Params:
    - en for English error messages
    - jp for Japanese error messages

    Used for printing out error messages defined in the params before shutting down the program when an error occurs.
    """
    log_error()
    if "en" in errorMessages and lang == "en":
        enErrorMessages = errorMessages.get("en")
        if isinstance(enErrorMessages, tuple):
            for line in enErrorMessages:
                print(f"{F.RED}{line}{END}")
        else: print(f"{F.RED}{enErrorMessages}{END}")
        input("Please enter any key to exit...")
        print(f"{F.LIGHTYELLOW_EX}Thank you for your understanding.{END}")
        
    elif "jp" in errorMessages and lang == "jp":
        jpErrorMessages = errorMessages.get("jp")
        if isinstance(jpErrorMessages, tuple):
            for line in jpErrorMessages:
                print(f"{F.RED}{line}{END}")
        else: print(f"{F.RED}{jpErrorMessages}{END}")
        input("何か入力すると終了します。。。")
        print(f"{F.LIGHTYELLOW_EX}ご理解頂き誠にありがとうございます。{END}")

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
        if isinstance(enMessages, tuple):
            for enLine in enMessages:
                print(enLine)
        else: print(enMessages)
    elif lang == "jp":
        if isinstance(jpMessages, tuple):
            for jpLine in jpMessages:
                print(jpLine)
        else: print(jpMessages)
    else:
        if isinstance(enMessages, tuple):
            for enLine in enMessages:
                print(enLine)
        else: print(enMessages)
        if isinstance(jpMessages, tuple):
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
        if isinstance(prints, tuple):
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
        dataDirectory = pathlib.Path.home().joinpath("AppData/Roaming/Cultured-Downloader")
    elif osPlatform == "Linux":
        dataDirectory = pathlib.Path.home().joinpath(".config/Cultured-Downloader")
    elif osPlatform == "Darwin": # macOS
        dataDirectory = pathlib.Path.home().joinpath("Library/Preferences/Cultured-Downloader")
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
    - headless --> True or False, defaults to True
    - blockImg --> a number, defaults to 2
    - windowSize --> Tuple of int, defaults to (1920, 1080)
    - quiet --> True or False, defaults to False

    For numbers, use the definition below:
    - 0 is default
    - 1 is to allow
    - 2 is to block
    """
    headlessOption = additionalOptions.get("headless")
    if headlessOption == None: headlessOption = True 

    blockImages = additionalOptions.get("blockImg")
    if blockImages == None: blockImages = 2 # set to 2 by default to block all images

    windowSize = additionalOptions.get("windowSize")
    if windowSize == None: windowSize = (1920, 1080) 

    quietFlag = additionalOptions.get("quiet")
    if quietFlag == None: quietFlag = False

    if not quietFlag:
        print_in_both_en_jp(
            en=(f"\n{F.LIGHTYELLOW_EX}Initialising Browser...{END}"),
            jp=(f"\n{F.LIGHTYELLOW_EX}ブラウザの初期化中です...{END}")
        )

    if browserType == "chrome":
        options = chromeOptions()
    elif browserType == "edge":
        options = edgeOptions()
        options.use_chromium = True

    # run browser in headless mode and hides unnecessary text output
    options.headless = headlessOption
    options.add_argument("--log-level=3")

    # performance settings for webdriver
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage") # from https://stackoverflow.com/questions/62898801/selenium-headless-chrome-runs-much-slower

    # change default download location
    options.add_experimental_option("prefs", {
        "download.default_directory": str(browserDownloadLocation),
        "profile.managed_default_content_settings.images": blockImages,
        "download.prompt_for_download": False
    })

   
    # remove DevTools msg
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if browserType == "chrome":
        gService = chromeService(ChromeDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Chrome(service=gService, options=options)
    elif browserType == "edge":
        eService = edgeService(EdgeChromiumDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Edge(service=eService, options=options)
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

    driver.set_window_size(windowSize[0], windowSize[1])
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
        en=(
            f"{F.GREEN}{selectedBrowser.title()} has been loaded and will be automatically loaded in future runs!{END}",
            f"{F.LIGHTRED_EX}However, you will have to login again by manually logging in or loading in your cookies.{END}"
        ),
        jp=(
            f"{F.GREEN}{selectedBrowser.title()}はロードされており、今後の実行でもロードされます！{END}",
            f"{F.LIGHTRED_EX}ただし、手動でログインするか、Cookieを読み込んで再ログインする必要があります。{END}"
        )
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
    defaultDownloadFolderPath = pathlib.Path.home().joinpath("Desktop", "Cultured-Downloader")
    jsonConfig["Download_Directory"] = str(defaultDownloadFolderPath)
    with open(jsonPath, "w") as f:
        json.dump(jsonConfig, f, indent=4)

    print_in_both_en_jp(
        en=(
            f"{F.LIGHTYELLOW_EX}Note: The default download folder will be defaulted to your desktop folder.{END}",
            f"{F.LIGHTYELLOW_EX}Default Download Folder Path: {defaultDownloadFolderPath}{END}"
        ),
        jp=(
            f"{F.LIGHTYELLOW_EX}注意： デフォルトのダウンロードフォルダをデスクトップに設定しました。{END}",
            f"{F.LIGHTYELLOW_EX}ダウンロードフォルダのフルパス： {defaultDownloadFolderPath}{END}"
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
    - printSuccessMsg (bool): If True, it will print a success message after setting the default download directory.
    --> Default: True
    """
    setDefaultLocationCondition = options.get("setDefaultLocationUponCancellation")
    if setDefaultLocationCondition == None: setDefaultLocationCondition = True

    printSuccessMsg = options.get("printSuccessMsg")
    if printSuccessMsg == None: printSuccessMsg = True

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

                if printSuccessMsg:
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
    
    data = json.dumps(data) # converts the python object to a string

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
        else: raise SessionError(f"Saved {website} cookies did not have the corresponding value needed for the session object in the function, get_cookie_for_session.")
    else:
        if definedSessionID:
            sessionObject = requests.session()
            sessionIDCookie = requests.cookies.create_cookie(domain=domain, name=cookieName, value=definedSessionID)
            sessionObject.cookies.set_cookie(sessionIDCookie)
            return sessionObject
        else: raise SessionError(f"{website} cookies did not have the corresponding value in the defined session ID needed for the session object in the function, get_cookie_for_session.")

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

    print_in_both_en_jp(
        en=(
            f"{F.LIGHTYELLOW_EX}A new browser should have opened. However, please do not close it at all times!{END}",
            f"{F.LIGHTYELLOW_EX}Please enter your username and password and login to {website.title()} manually.{END}",
            f"{F.LIGHTRED_EX}If you would like to skip this login process, please just press enter and ignore the login failure message and enter \"n\" for the login retry prompt.{END}"
        ),
        jp=(
            f"{F.LIGHTYELLOW_EX}新しいブラウザが起動したはずです。ただし、常に閉じないようにしてください！{END}", 
            f"{F.LIGHTYELLOW_EX}ユーザー名とパスワードを入力し、手動で{website.title()}にログインしてください。{END}",
            f"{F.LIGHTRED_EX}このログイン処理を省略したい場合は、Enterキーを押してログイン失敗のメッセージを無視し、ログイン再試行のプロンプトに \"n\" を入力してください。{END}"
        )
    )

    newDriver = get_driver(selectedBrowser, headless=False, blockImg=1, windowSize=(800, 800))
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
        try: 
            loggedIn = login(newDriver, website)
        except WebDriverException: 
            # if the user had accidentally closed the browser by accident, it will open a new browser
            print_in_both_en_jp(
                en=(
                    f"{F.LIGHTRED_EX}Note: Please do not close the browser!{END}"
                ),
                jp=(
                    f"{F.LIGHTRED_EX}注意： ブラウザを閉じないでください!{END}"
                )
            )
            newDriver = get_driver(selectedBrowser, headless=False, blockImg=1, windowSize=(800, 800))

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
                jp=(f"{F.RED}{website.title()}のセッションクッキーの保存は、ユーザーの要求に応じて中止されます。{END}")
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

def load_cookies():
    """
    To load in the saved cookies into the webdriver browser session.

    Will return two boolean true or false values:
    --> First value for pixiv Fanbox and second value for Fantia
    """
    pixivCookieLoadedLocal = fantiaCookieLoadedLocal = False

    fantiaCookieExist = appPath.joinpath("configs", "fantia_cookies").is_file()
    pixivCookieExist = appPath.joinpath("configs", "pixiv_cookies").is_file()

    if fantiaCookieExist or pixivCookieExist:    
        if lang == "en": cookiePrompt = "Would you like to login using your saved cookies? (y/n): "
        elif lang == "jp": cookiePrompt = "保存されているクッキーを使用してログインしますか？ (y/n): "

        userCookieInput = get_input_from_user(prompt=cookiePrompt, command=("y", "n"))
        if userCookieInput == "y":
            if pixivCookieExist: pixivCookieLoadedLocal = load_cookie("pixiv")
            if fantiaCookieExist: fantiaCookieLoadedLocal = load_cookie("fantia")
        else:
            print_in_both_en_jp(
                en=(f"{F.LIGHTYELLOW_EX}Saved cookies will not be loaded into the webdriver...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}その場合、保存されたクッキーは読み込まれません...{END}")
            )

    return pixivCookieLoadedLocal, fantiaCookieLoadedLocal

def check_if_input_is_url(inputString, website):
    """
    Validates if the user's inputs is a valid URL and is a URL for Fantia posts, Fantia image URL, and Pixiv Fanbox posts using regex.

    Requires two arguments to be defined:
    - User's input (string or list)
    - The website, either "fantiaPost", "fantiaImage", "pixivFanbox", "fantiaPostPage", or "pixivFanboxPostPage" (string)
    """
    if not isinstance(inputString, list):
        try:
            result = urlparse(inputString)
            if all([result.scheme, result.netloc]):
                if website == "fantiaPost":
                    if re.fullmatch(fantiaPostRegex, inputString):
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
                elif website == "pixivFanbox":
                    if not re.match(pixivFanboxPostRegex, url): return False
                elif website == "fantiaPostPage":
                    if not re.fullmatch(fantiaPostPageRegex, url): return False
                elif website == "pixivFanboxPostPage":
                    if not re.fullmatch(pixivFanboxPostPageRegex, url): return False
            except:
                return False

        return True

def split_inputs_to_possible_multiple_inputs(userInput, **options):
    """
    Removes all whitespaces including Japanese whitespaces and splits the user's inputs into a list of possible inputs based on the delimiters, "," or "、".

    Note: this function will also remove any duplicate elements in the user's input so if there is no need to remove duplicate elements, please add in the optional param below.

    Requires one argument to be defined:
    - A string

    Optional param:
    - removeDuplicates (bool): If True, this function will remove duplicate elements in the user's input. However, if the user enters "d-", it will not remove duplicate elements anymore. Defaults to True if not defined.
    - allowDupeCommand (bool): If True, this function will allow the user to enter "d-" in the input to prevent duplicate element(s) removal. Note that this will only work if removeDuplicates param is also true. Defaults to False if not defined.
    """
    userInput = userInput.replace(" ", "")
    userInput = userInput.replace("　", "")
    if "," in userInput: userInput = userInput.split(",")
    elif "、" in userInput: userInput = userInput.split("、")

    if "removeDuplicates" in options: removeDuplicates = options["removeDuplicates"]
    else: removeDuplicates = True

    if "allowDupeCommand" in options and removeDuplicates: 
        allowDupeCommand = options["allowDupeCommand"]
    else: allowDupeCommand = False

    if isinstance(userInput, list):
        if "d-" in userInput and allowDupeCommand:
            removeDuplicates = False
            userInput.remove("d-")

        if removeDuplicates:
            removedDuplicatedUrls = list(dict.fromkeys(userInput))

            removedDuplicatedUrlsLen = len(removedDuplicatedUrls)
            if removedDuplicatedUrlsLen != len(userInput):
                print_in_both_en_jp(
                    en=(
                        "\n",
                        f"{F.LIGHTRED_EX}Warning: Duplicate input(s) have been removed from your input.{END}",
                        f"{F.LIGHTYELLOW_EX}Entered input(s) with duplicates removed: \n" + ", ".join(url for url in removedDuplicatedUrls) + f"{END}",
                        f"{F.LIGHTYELLOW_EX}\nIf you would like to keep the duplicate inputs, please type \"d-,\" in your input as well!{END}",
                        f"{F.LIGHTYELLOW_EX}For example: d-, input1, input1, input2{END}",
                        "\n"
                    ),
                    jp=(
                        "\n",
                        f"{F.LIGHTRED_EX}ご注意： 重複する入力は入力から削除されました。{END}",
                        f"{F.LIGHTYELLOW_EX}重複を排除して入力した： \n" + "、".join(url for url in removedDuplicatedUrls) + f"{END}",
                        f"{F.LIGHTYELLOW_EX}\n重複入力を避けたい場合は、入力の際にも\"d-、\"と入力してください!{END}",
                        f"{F.LIGHTYELLOW_EX}例： d-、インプット1、インプット1、インプット2{END}",
                        "\n"
                    )
                )
            else:
                print_in_both_en_jp(
                    en=(
                        "\n",
                        f"{F.LIGHTYELLOW_EX}Your entered input: \n" + ", ".join(url for url in userInput) + f"{END}",
                        "\n"
                    ),
                    jp=(
                        "\n",
                        f"{F.LIGHTYELLOW_EX}入力された内容: \n" + "、".join(url for url in userInput) + f"{END}",
                        "\n"
                    )
                )

            if removedDuplicatedUrlsLen > 1:
                return removedDuplicatedUrls
            else:
                return removedDuplicatedUrls[0]
        else:
            print_in_both_en_jp(
                en=(
                    "\n",
                    f"{F.LIGHTYELLOW_EX}Your entered input: \n" + ", ".join(url for url in userInput) + f"{END}",
                    "\n"
                ),
                jp=(
                    "\n",
                    f"{F.LIGHTYELLOW_EX}入力された内容: \n" + "、".join(url for url in userInput) + f"{END}",
                    "\n"
                )
            )
            return userInput
    elif isinstance(userInput, str):
        print_in_both_en_jp(
            en=(
                "\n",
                f"{F.LIGHTYELLOW_EX}Your entered input: {userInput}{END}",
                "\n"
            ),
            jp=(
                "\n",
                f"{F.LIGHTYELLOW_EX}入力された内容: {userInput}{END}",
                "\n"
            )
        )
        return userInput
    else:
        raise Exception("Invalid data type in the function, split_inputs_to_possible_multiple_inputs...")

def get_page_num(userURLInput):
    """
    Used for retreiving the number of pages to go through from the user's input.

    Note: It uses the compiled regex to check for input validity such as "1-2", or "1".

    Requires one argument to be defined:
    - The user's URL input (string or list)
    """
    while True:
        print_in_both_en_jp(
            en=(f"{F.LIGHTYELLOW_EX}Note: If you have entered multiple urls previously, please enter in this format, \"1-3, 5, 2-10\"{END}"),
            jp=(f"{F.LIGHTYELLOW_EX}注意： 以前に複数のURLを入力したことがある場合は、このフォーマットで入力してください。\"1-3、5、2-10\"{END}")
        )
        if lang == "en": pageInput = split_inputs_to_possible_multiple_inputs(input("Enter the number of pages (X to cancel): "), removeDuplicates=False)
        else: pageInput = split_inputs_to_possible_multiple_inputs(input("ページ数を入力します (Xでキャンセル)： "), removeDuplicates=False)

        if pageInput == "x" or pageInput == "X": 
            return False
            
        if (pageInput == ""):
            print_in_both_en_jp(
                en=(
                    f"{F.RED}Error: No URL entered or URL entered.{END}\n"
                ),
                jp=(
                    f"{F.RED}エラー： URLが入力されていない。{END}\n"
                )
            )
        else: 
            if lang == "en": pageNumConfirmationPrompt = "Are you sure that the number of pages entered are correct? (y/n): "
            else: pageNumConfirmationPrompt = "入力されたページ数は正しいですか？ (y/n)： "

            pageNumConfirmation = get_input_from_user(prompt=pageNumConfirmationPrompt, command=("y", "n"))
            if pageNumConfirmation == "y":
                if isinstance(pageInput, list):
                    validPageNumInputs = True
                    for pageNum in pageInput:
                        if re.fullmatch(pageNumRegex, pageNum) == None:
                            validPageNumInputs = False
                    if validPageNumInputs:
                        if isinstance(userURLInput, list):
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
                elif isinstance(pageInput, str):
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
                        if isinstance(userURLInput, str):
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

def get_url_inputs(urlValidationType, promptTuple):
    """
    To get the user's URL inputs.

    Requires two arguments to be defined:
    - urlValidationType --> The type of URL validation to be done with the global regex variables.
    - promptTuple --> The prompt tuple to be used for the input prompt, first index for English and second index for Japanese in the tuple.
    """
    while True:
        if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input(promptTuple[0]), allowDupeCommand=True)
        else: urlInput = split_inputs_to_possible_multiple_inputs(input(promptTuple[1]), allowDupeCommand=True)

        if urlInput == "x" or urlInput == "X":
            return False

        if lang == "en": confirmationPrompt = "Are/Is the entered URL(s) correct? (y/n): "
        elif lang == "jp": confirmationPrompt = "入力されたURLは正しいですか？ (y/n)： "
        else: raise Exception(f"Invalid language, {lang}, in function, get_url_inputs...")

        confirmation = get_input_from_user(prompt=confirmationPrompt, command=("y", "n"))

        if confirmation == "y":
            break
        else:
            return "invalid"

    if (urlInput == "") or (check_if_input_is_url(urlInput, urlValidationType) == False): 
        print_in_both_en_jp(
            en=(
                f"{F.RED}Error: No URL entered or URL entered is/are invalid.{END}\n"
            ),
            jp=(
                f"{F.RED}エラー： URLが入力されていない、または入力されたURLが無効である。{END}\n"
            )
        )
        return "invalid"
    else: return urlInput

def get_download_flags(website):
    """
    Retrieves the download flags for executing the download logic.

    Requires one argument to be defined:
    - website --> "fantia" or "pixiv"

    Returns a tuple of the download flags in the order of 
    imageFlag, downloadAttachmentFlag, downloadThumbnailFlag, gdriveFlag

    If user plans to cancel the entire download process and return to menu, it will return a tuple of None values.
    """
    while True:
        if lang == "en": 
            imagePrompt = "Would you like to download images from each post? (y/n/x to cancel and return to menu): "
        elif lang == "jp": 
            imagePrompt = "投稿ごとに画像をダウンロードしますか？ (y/n/xでキャンセルしてメニューに戻る): "
            
        imageFlag = get_input_from_user(prompt=imagePrompt, command=("y", "n", "x"))
        if imageFlag == "y": imageFlag = True
        elif imageFlag == "n": imageFlag = False
        else: return None, None, None, None

        if website == "pixiv":
            if lang == "en": 
                gdrivePrints = "\nNote: If one of the gdrive files from a post is locked due to exceeding its download quota,\nthis program will halt the gdrive download for that post and will generate a text file for you to manually download."
                gdrivePrompt = "Would you like to download any gdrive links if found? (y/n/x to cancel and return to menu): "
            elif lang == "jp":
                gdrivePrints = "\n注意：ある投稿のgdriveファイルがダウンロード枠を超えてロックされている場合、\nこのプログラムはその投稿のgdriveダウンロードを停止し、\n手動でダウンロードするためのテキストファイルを生成します。"
                gdrivePrompt = "gdriveのリンクが見つかったら、ダウンロードしますか？ (y/n/xでキャンセルしてメニューに戻る): "

            gdriveFlag = get_input_from_user(prompt=gdrivePrompt, command=("y", "n", "x"), prints=gdrivePrints)
            if gdriveFlag == "y": gdriveFlag = True
            elif gdriveFlag == "n": gdriveFlag = False
            else: return None, None, None, None

        elif website == "fantia":
            gdriveFlag = False

        if lang == "en": attachmentPrompt = "Would you like to download attachments such as psd files, videos, gifs (if found)? (y/n/x to cancel and return to menu): "
        elif lang == "jp": attachmentPrompt = "psdファイルや動画ファイルやgifファイルをダウンロードしますか (見つかった場合)？ (y/n/xでキャンセルしてメニューに戻る): "
        downloadAttachmentFlag = get_input_from_user(prompt=attachmentPrompt, command=("y", "n", "x"))

        if downloadAttachmentFlag == "y": downloadAttachmentFlag = True
        elif downloadAttachmentFlag == "n": downloadAttachmentFlag = False
        else: return None, None, None, None

        if lang == "en": thumbnailPrompt = "Would you like to download the thumbnail for each post? (y/n/x to cancel and return to menu): "
        elif lang == "jp": thumbnailPrompt = "投稿ごとにサムネイルをダウンロードしますか？ (y/n/xでキャンセルしてメニューに戻る): "
        downloadThumbnailFlag = get_input_from_user(prompt=thumbnailPrompt, command=("y", "n", "x"))

        if downloadThumbnailFlag == "y": downloadThumbnailFlag = True
        elif downloadThumbnailFlag == "n": downloadThumbnailFlag = False
        else: return None, None, None, None

        if not imageFlag and not gdriveFlag and not downloadAttachmentFlag and not downloadThumbnailFlag:
            print_in_both_en_jp(
                en=(
                    f"{F.RED}Error: Please select at least one download option.{END}\n"
                ),
                jp=(
                    f"{F.RED}エラー： ダウンロードを1つ以上選択してください。{END}\n"
                )
            )
        else: 
            return imageFlag, downloadAttachmentFlag, downloadThumbnailFlag, gdriveFlag

def get_creator_from_url(url):
    """
    Extract the creator's pixiv creator name ID or fantia ID from the URL.
    
    Requires one argument to be defined:
    - url (string)
    """
    urlUnwantedParts = ("https:", "www", "fanbox", "cc", "", "fantia", "jp", "fanclubs")
    for urlParts in url.replace(".", "/").split("/")[:-1]:
        if urlParts not in urlUnwantedParts:
            if "@" in urlParts: urlParts = urlParts.replace("@", "")
            return urlParts

def execute_download_process(urlInput, imagePath, downloadType, website, **options):
    """
    For executing the logic behind downloading images or attachments.

    Requires four argument to be defined:
    - urlInput (str or list) - The URL(s) to download from
    - imagePath (pathlib Path object) - The path to save the downloaded images to
    - downloadType (str) - "postPreviewPage" or "postPage"
    - website (str) - "pixiv" or "fantia"

    Optional param depending on the downloadType:
    - pageInput (str or list) - The page number(s) to download from, must be defined if the download type is "postPreviewPage"
    """
    if downloadType == "postPreviewPage":
        if "pageInput" in options: pageInput = options["pageInput"]
        else: raise Exception("pageInput variable for downloading post preview page is not defined...")
        
        postPreviewURLArray = []
        if isinstance(pageInput, str)and isinstance(urlInput, str):
            try:
                pageNum = int(pageInput)
                postPreviewURLArray.append("".join([urlInput, "?page=", str(pageNum)]))
            except:
                pageNumList = [int(num) for num in pageInput.split("-")]
                pageNumList.sort()
                for i in range(pageNumList[0], pageNumList[1] + 1):
                    postPreviewURLArray.append("".join([urlInput, "?page=", str(i)]))
        elif isinstance(pageInput, list) and isinstance(urlInput, list):
            arrayPointer = 0
            pagePostOffsetArr = []
            for pageNumInput in pageInput:
                try:
                    pageNum = int(pageNumInput)
                    postPreviewURLArray.append("".join([urlInput[arrayPointer], "?page=", str(pageNum)]))
                except:
                    pageNumList = [int(num) for num in pageNumInput.split("-")]
                    pageNumList.sort()
                    for i in range(pageNumList[0], pageNumList[1] + 1):
                        postPreviewURLArray.append("".join([urlInput[arrayPointer], "?page=", str(i)]))

                pagePostOffsetArr.append(len(postPreviewURLArray))
                arrayPointer += 1
        else:
            raise Exception(f"{website} posts download's variables are not in correct format...")
        
        imageFlag, downloadAttachmentFlag, downloadThumbnailFlag, gdriveFlag = get_download_flags(website)
        if imageFlag == None: 
            print_in_both_en_jp(
                en=(
                    f"{F.LIGHTYELLOW_EX}Download cancelled...{END}"
                ),
                jp=(
                    f"{F.LIGHTYELLOW_EX}ダウンロードはキャンセルされました...{END}"
                )
            )
            return

        if isinstance(urlInput, list): numOfPostPage = len(urlInput)
        else: numOfPostPage = 1
        print("\n")
        print_in_both_en_jp(
            en=(
                f"{F.LIGHTYELLOW_EX}Please wait as auto downloading files from {website.title()} can take quite a while if the file size is large...{END}",
                f"{F.LIGHTYELLOW_EX}The program will automatically download files from {numOfPostPage} all posts preview pages.{END}",
                f"{F.LIGHTYELLOW_EX}If it freezes, fret not! It's in the midst of downloading large files.\nJust let it run and do not terminate the program! Otherwise you will have to restart the download again.{END}"
            ),
            jp=(
                f"{F.LIGHTYELLOW_EX}{website.title()}からのファイルの自動ダウンロードは、ファイルサイズが大きい場合、かなり時間がかかるので、お待ちください...{END}",
                f"{F.LIGHTYELLOW_EX}このプログラムは、{numOfPostPage}件の投稿プレビューページから自動的にファイルをダウンロードする。{END}",
                f"{F.LIGHTYELLOW_EX}フリーズしても大丈夫! 大きなファイルをダウンロードしている最中なのです。\nそのまま実行させ、プログラムを終了させないでください! そうしないと、またダウンロードを再開しなければならなくなります。{END}"
            )
        )
        print("\n")
        print_in_both_en_jp(
            en=(f"{F.LIGHTYELLOW_EX}Please wait as the program is retrieving multiple posts...{END}"),
            jp=(f"{F.LIGHTYELLOW_EX}このプログラムが複数の投稿を取得しているため、しばらくお待ちください...{END}")
        )
        print("\n")
        postURLToDownloadArray = []
        
        if website == "fantia": xpathValue = "//a[@class='link-block']"
        elif website == "pixiv": xpathValue = "//a[@class='sc-1bjj922-0 gwbPAH']"

        if isinstance(urlInput, list): 
            offSetArr = []
            postCount = 0
            pageCount = 0
            arrayOffsetPointer = 0
            
            creatorNameArr = []
        elif isinstance(urlInput, str):
            count = 0

        for postURL in postPreviewURLArray: 
            driver.get(postURL)
            sleep(3)
            try: posts = driver.find_elements(by=By.XPATH, value=xpathValue)
            except: posts = []

            for postAnchorEl in posts:
                postURLToDownloadArray.append(postAnchorEl.get_attribute("href"))

                if isinstance(urlInput, list):
                    postCount += 1

            # if downloading from multiple creators
            if isinstance(urlInput, list):     
                pageCount += 1
                if pageCount == pagePostOffsetArr[arrayOffsetPointer]:
                    arrayOffsetPointer += 1
                    offSetArr.append(postCount)
                    creatorNameArr.append(get_creator_from_url(driver.current_url))

            # if downloading from one creator
            elif isinstance(urlInput, str) and count == 0:
                count += 1
                creatorName = get_creator_from_url(driver.current_url)

        # iterate in reversed when downloading such that the latest one will be the highest post number
        if postURLToDownloadArray and isinstance(urlInput, str):
            counter = get_latest_post_num(imagePath)
            for postURL in reversed(postURLToDownloadArray):
                downloadDirectoryFolder = imagePath.joinpath(creatorName, f"Post-{counter}")
                download(postURL, f"{website.title()}", downloadDirectoryFolder, attachments=downloadAttachmentFlag, thumbnails=downloadThumbnailFlag, images=imageFlag, gdrive=gdriveFlag)
                counter += 1
        elif postURLToDownloadArray and isinstance(urlInput, list):
            counter = creatorPostPointer = 0
            creatorNamePointer = -1
            downloadDirectoryFolder = imagePath.joinpath(creatorNameArr[creatorNamePointer])
            postNum = get_latest_post_num(downloadDirectoryFolder)
            
            # calculate the number of posts to download before moving on to a new folder for the next creator
            postsToDownloadArr = []
            for i, n in reversed(list(enumerate(offSetArr[:-1]))):
                postsToDownloadArr.append(abs(n - offSetArr[i + 1]))
            postsToDownloadArr.append(offSetArr[0])

            for postURL in reversed(postURLToDownloadArray):
                downloadSubDirectoryFolder = downloadDirectoryFolder.joinpath(f"Post-{postNum}")
                download(postURL, f"{website.title()}", downloadSubDirectoryFolder, attachments=downloadAttachmentFlag, thumbnails=downloadThumbnailFlag, images=imageFlag, gdrive=gdriveFlag)
                counter += 1
                postNum += 1
                if (postURL != postURLToDownloadArray[0] and counter == postsToDownloadArr[creatorPostPointer]):
                    creatorNamePointer -= 1
                    counter = 0
                    creatorPostPointer += 1
                    downloadDirectoryFolder = imagePath.joinpath(creatorNameArr[creatorNamePointer])
                    postNum = get_latest_post_num(downloadDirectoryFolder)
        else:
            print_in_both_en_jp(
                en=(
                    f"{F.RED}Error: No posts found on the given URL.{END}"
                ),
                jp=(
                    f"{F.RED}エラー： 指定されたURLに投稿が見つかりませんでした。{END}"
                )
            )
    elif downloadType == "postPage":
        imageFlag, downloadAttachmentFlag, downloadThumbnailFlag, gdriveFlag = get_download_flags(website)
        if imageFlag == None: 
            print_in_both_en_jp(
                en=(
                    f"{F.LIGHTYELLOW_EX}Download cancelled...{END}"
                ),
                jp=(
                    f"{F.LIGHTYELLOW_EX}ダウンロードはキャンセルされました...{END}"
                )
            )
            return

        if isinstance(urlInput, list): numOfPosts = len(urlInput)
        else: numOfPosts = 1
        print("\n")
        print_in_both_en_jp(
            en=(
                f"{F.LIGHTYELLOW_EX}Please wait as auto downloading files from {website.title()} can take quite a while if the file size is large...{END}",
                f"{F.LIGHTYELLOW_EX}The program will automatically download files from {numOfPosts} posts.{END}",
                f"{F.LIGHTYELLOW_EX}If it freezes, fret not! It's in the midst of downloading large files.\nJust let it run and do not terminate the program! Otherwise you will have to restart the download again.{END}"
            ),
            jp=(
                f"{F.LIGHTYELLOW_EX}{website.title()}からのファイルの自動ダウンロードは、ファイルサイズが大きい場合、かなり時間がかかるので、お待ちください...{END}",
                f"{F.LIGHTYELLOW_EX}このプログラムは、{numOfPosts}投稿の中からファイルを自動的にダウンロードします。{END}",
                f"{F.LIGHTYELLOW_EX}フリーズしても大丈夫! 大きなファイルをダウンロードしている最中なのです。\nそのまま実行させ、プログラムを終了させないでください! そうしないと、またダウンロードを再開しなければならなくなります。{END}"
            )
        )
        print("\n")
        if isinstance(urlInput, list):
            if lang == "en": reversePrompt = "Do you want to download in reverse order? (y/n): "
            else: reversePrompt = "逆順でダウンロードしますか？ (y/n)： "
            downloadInReversedFlag = get_input_from_user(prompt=reversePrompt, command=("y", "n"))
            counter = get_latest_post_num(imagePath)
            
            if downloadInReversedFlag == "y": dl = reversed(urlInput)
            else: dl = urlInput
            
            for url in dl: 
                downloadDirectoryFolder = imagePath.joinpath(f"Post-{counter}")
                download(url, f"{website.title()}", downloadDirectoryFolder, attachments=downloadAttachmentFlag, thumbnails=downloadThumbnailFlag, images=imageFlag, gdrive=gdriveFlag)
                counter += 1
        else:
            imagePath = imagePath.joinpath(f"Post-{get_latest_post_num(imagePath)}")
            download(urlInput, f"{website.title()}", imagePath, attachments=downloadAttachmentFlag, thumbnails=downloadThumbnailFlag, images=imageFlag, gdrive=gdriveFlag)
    else:
        raise Exception(f"Download type given: {downloadType} is not valid!")

def check_for_incomplete_download():
    """
    To check for any incomplete downloads by the webdriver's browser in its default download location.
    """
    sleep(2) # some delays to make sure every files has been downloaded.
    while True:
        browserDownloadLocation.mkdir(parents=True, exist_ok=True)
        hasIncompleteDownloads = False
        sleep(2)
        for filePath in browserDownloadLocation.iterdir():
            if filePath.is_file():
                if filePath.suffix == ".crdownload": # crdownload for chrome and edge 
                    hasIncompleteDownloads = True # since edge is set to use chromium, hence not checking for .partial files for edge.

        if not hasIncompleteDownloads: 
            sleep(1.5)
            return

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

def check_if_directory_has_files(dirPath):
    """
    Returns True if there is any files or folders in the argument given.

    Otherwise, it will return False.

    Requires one argument to be defined:
    - A pathlib Path object
    """
    hasFiles = any(dirPath.iterdir())
    return hasFiles

def get_file_name(imageURL, website):
    """
    Returns the file name based on the URL given.

    Requires two arguments to be defined:
    - A URL (string)
    - The website name (string), "Pixiv" or "Fantia"
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    if "session" in requestSession:
        req = requestSession["session"]
    else:    
        req = requests

    try:
        with req.get(imageURL, stream=True, headers=headers, timeout=10) as r:
            with open(pathToSave, "wb") as f:
                copyfileobj(r.raw, f)
    except requests.exceptions.ReadTimeout:
        print_in_both_en_jp(
            en=f"\n{F.LIGHTRED_EX}Error: Request timeout, retrying...{END}\n",
            jp=f"\n{F.LIGHTRED_EX}エラー： リクエストタイムアウト、再試行します。{END}\n"
        )
        save_image(imageURL, pathToSave, **requestSession)

def print_progress_bar(prog, totalEl, caption):
    """
    For printing a progress bar such as the one below.

    [============] 100% Downloading 2 out of 2 images...

    Requires three arguments to be defined:
    - The current progress (int)
    - The max progress or max number of elements (int)
    - A caption such as "Downloading 2 out of 2 images..." (string)
    """
    barLength = 30 #size of progress bar
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
    - images (bool) if True, will print out the corresponding message to alert of the images that have already being downloaded
    - attachments (bool) if True, will print out the corresponding message instead of just alerting the user that the program have downloaded all the images. 
    - thumbnailNotice (bool) if True, will print out the corresponding message to alert the user that the thumbnail has been downloaded.
    - gdriveNotice (bool) if True, will print out the corresponding message to alert the user that the file has been downloaded from gdrive
    --> default: False if not defined
    """
    if "images" in options: images = options["images"]
    else: images = False

    if "attachments" in options: attachments = options["attachments"]
    else: attachments = False

    if "thumbnailNotice" in options: thumbnailNotice = options["thumbnailNotice"]
    else: thumbnailNotice = False

    if "gdriveNotice" in options: gdriveNotice = options["gdriveNotice"]
    else: gdriveNotice = False

    completionMsg = "\n"

    if totalImage > 0:
        if lang == "en": completionMsg += f"{F.LIGHTYELLOW_EX}Main download location: {subFolderPath}{END}\n"
        elif lang == "jp": completionMsg += f"{F.LIGHTYELLOW_EX}メインダウンロードの場所： {subFolderPath}{END}\n"

        if thumbnailNotice:
            if lang == "en": completionMsg += f"{F.GREEN}The thumbnail of the post has been downloaded.{END}"
            elif lang == "jp": completionMsg += f"{F.GREEN}投稿のサムネイルがダウンロードされました。{END}"
            completionMsg += "\n"

        if gdriveNotice:
            if lang == "en": completionMsg += f"{F.GREEN}{totalImage} files has been successfully downloaded from gdrive{END}"
            elif lang == "jp": completionMsg += f"{F.GREEN}gdriveから{totalImage}個のファイルがダウンロードされました。{END}"
            completionMsg += "\n"

        if attachments and images:
            if lang == "en": 
                completionMsg += f"{F.GREEN}Successfully downloaded {totalImage} images and attachments{END}"
            elif lang == "jp": 
                completionMsg += f"{F.GREEN}{totalImage}個のイメージとファイルのダウンロードに成功しました。{END}"
        elif images:
            if lang == "en":
                completionMsg += f"{F.GREEN}Successfully downloaded {totalImage} images{END}"
            elif lang == "jp":
                completionMsg += f"{F.GREEN}{totalImage}枚の画像をダウンロードしました!{END}"
        elif attachments:
            if lang == "en":
                completionMsg += f"{F.GREEN}Successfully downloaded {totalImage} attachments{END}"
            elif lang == "jp":
                completionMsg += f"{F.GREEN}{totalImage}個のファイルをダウンロードしました。{END}"
    else:
        if thumbnailNotice:
            thumbnailPath = subFolderPath.joinpath("thumbnail")
            if lang == "en": completionMsg += f"{F.GREEN}The thumbnail of the post has been downloaded to\n{thumbnailPath}{END}"
            elif lang == "jp": completionMsg += f"{F.GREEN}投稿のサムネイルが\n{thumbnailPath} にダウンロードされました。{END}"
            completionMsg += "\n"

        if lang == "en": completionMsg += f"{F.LIGHTRED_EX}Note: There is no main content to download from the post.{END}"
        elif lang == "jp": completionMsg += f"{F.LIGHTRED_EX}注意：投稿からダウンロードするメインコンテンツはありません。{END}"
    
    print(completionMsg, "\n")

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

def get_gdrive_id(url):
    """
    Returns the gdrive ID by splitting with the delimiter "/" and getting the element on index 5 which is usually the gdrive ID for a file or folder

    Requires one argument to be defined:
    - The gdrive link (string)
    """
    url = url.split("/")[5]
    if "?" in url: url = url.split("?")[0]
    return url

def get_data_for_request(gdriveID, gdriveType):
    """
    Returns the data for the request to retrieve information about the gdrive files/folders.

    Requires two arguments to be defined:
    - The gdrive ID (string)
    - The gdrive type (string) --> "file" or "folder"
    """
    data = {
        "data": {
            "id": gdriveID,
            "type": gdriveType
        }
    }
    return data

def execute_gdrive_download(gdriveURL, directoryPath):
    """
    Function for downloading files from gdrive based on the given url.

    Requires two argument to be defined:
    - The gdrive link (string)
    - The directory path (pathlib Path Object)
    """
    class HiddenPrints: # https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout
            
    if "file" in gdriveURL:
        fileID = get_gdrive_id(gdriveURL)

        gReq = requests.post(queryWebsite, json=get_data_for_request(fileID, "file")).json()

        if "error" not in gReq:
            fullDownloadPath = directoryPath.joinpath(gReq["name"])
            directoryPath.mkdir(parents=True, exist_ok=True)
            with HiddenPrints():
                downloaded = gdown.download(id=fileID, output=str(fullDownloadPath), quiet=True)
            if downloaded == None: return False
        else:
            return False
    elif "folder" in gdriveURL:
        folderID = get_gdrive_id(gdriveURL)

        gReq = requests.post(queryWebsite, json=get_data_for_request(folderID, "folder")).json()

        nestedFolderIDArr = []
        if "error" not in gReq:
            gFiles = gReq["files"]
            for file in gFiles:
                if file["mimeType"] != "application/vnd.google-apps.folder":
                    fullDownloadPath = directoryPath.joinpath(file["name"])
                    directoryPath.mkdir(parents=True, exist_ok=True)
                    fileID = file["id"]
                    with HiddenPrints():
                        downloaded = gdown.download(id=fileID, output=str(fullDownloadPath), quiet=True)
                    if downloaded == None: return False
                else:
                    nestedFolderIDArr.append(file["id"])
        else:
            return False

        while nestedFolderIDArr:
            nestedFolderID = nestedFolderIDArr.pop()
            gReq = requests.post(queryWebsite, json=get_data_for_request(nestedFolderID, "folder")).json()

            if "error" not in gReq:
                gFiles = gReq["files"]
                for file in gFiles:
                    if file["mimeType"] != "application/vnd.google-apps.folder":
                        fullDownloadPath = directoryPath.joinpath(file["name"])
                        directoryPath.mkdir(parents=True, exist_ok=True)
                        fileID = file["id"]
                        with HiddenPrints():
                            downloaded = gdown.download(id=fileID, output=str(fullDownloadPath), quiet=True)
                        if downloaded == None: return False
                    else:
                        nestedFolderIDArr.append(file["id"])
            else:
                return False
    else:
        raise Exception(f"Unknown gdrive url, {gdriveURL} ,please report to this to the developer(s)...")
    
    return True

def download(urlInput, website, subFolderPath, **options):
    """
    To download images from Fantia or pixiv Fanbox.

    Requires three arguments to be defined:
    - The url of the Fantia/pixiv posts or the Fantia image url (string)
    - The website which is either "FantiaPost", or "Pixiv" (string)
    - The path to the folder where the images are saved or a string which will be the latest post num for pixiv downloads (pathlib Path object or a string)

    Optional param:
    - images (boolean). If True, will download images from the post (Default: False if not defined)
    - attachments (boolean). If True, will download any attachments from the given url (default: False if not defined)
    - thumbnails (boolean). If True, will download the thumbnail of the post (default: False if not defined)
    - gdrive (boolean). If True, will scan the post page for any gdrive links and downloads them (default: False if not defined)
    """
    driver.get(urlInput)
    sleep(4)

    downloadImageFlag = options.get("images")
    if downloadImageFlag == None: downloadImageFlag = False

    downloadAttachmentFlag = options.get("attachments")
    if downloadAttachmentFlag == None: downloadAttachmentFlag = False

    downloadThumbnailFlag = options.get("thumbnails")
    if downloadThumbnailFlag == None: downloadThumbnailFlag = False

    downloadGdriveLinks = options.get("gdrive")
    if downloadGdriveLinks == None: downloadGdriveLinks = False

    if website == "Fantia":
        totalEl = 0
        thumbnailDownloadedCondition = False
        if downloadThumbnailFlag:
            try: thumbnailSrc = driver.find_element(by=By.XPATH, value="//img[contains(@class, 'img-default')]").get_attribute("src")
            except: thumbnailSrc = None

            if thumbnailSrc:
                subFolderPath.mkdir(parents=True, exist_ok=True)
                imagePath = subFolderPath.joinpath(get_file_name(thumbnailSrc, "Fantia"))
                # no session needed since it's displayed regardless of membership status
                save_image(thumbnailSrc, imagePath) 
                thumbnailDownloadedCondition = True
        
        imagesURLToDownloadArray = []
        if downloadImageFlag:
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

            anchorURLArray = []
            if attachmentAnchors: 
                for anchor in attachmentAnchors:
                    anchorURLArray.append(anchor.get_attribute("href"))
                open_new_tab()
            
            del attachmentAnchors

            if downloadImageFlag: totalEl += len(imagesURLToDownloadArray) + len(anchorURLArray)
            else: totalEl += len(anchorURLArray)

            remove_any_files_in_directory(browserDownloadLocation)
            for attachmentURL in anchorURLArray:
                if downloadImageFlag:
                    if lang == "en": downloadMessage = f"Downloading image/attachment no.{totalImageProgress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"画像やファイル {totalImageProgress} / {totalEl} をダウンロード中"
                else:
                    if lang == "en": downloadMessage = f"Downloading attachment no.{totalImageProgress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"ファイル {totalImageProgress} / {totalEl} をダウンロード中"

                if totalImageProgress == 0:
                    print_progress_bar(totalImageProgress, totalEl, downloadMessage)
                    totalImageProgress += 1

                driver.get(attachmentURL) # getting the url which in turns downloads the attachments
                sleep(3) # for the browser to download the attachment
                
                if downloadImageFlag:
                    if lang == "en": downloadMessage = f"Downloading image/attachment no.{totalImageProgress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"画像やファイル {totalImageProgress} / {totalEl} をダウンロード中"
                else:
                    if lang == "en": downloadMessage = f"Downloading attachment no.{totalImageProgress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"ファイル {totalImageProgress} / {totalEl} をダウンロード中"

                print_progress_bar(totalImageProgress, totalEl, downloadMessage)
                totalImageProgress += 1
            
            if anchorURLArray:
                close_new_tab()
                check_for_incomplete_download()
                # moves all the files to the corresponding folder based on the user's input.
                attachmentFolderPath = subFolderPath.joinpath("attachments")
                for file in browserDownloadLocation.iterdir():
                    attachmentFolderPath.mkdir(parents=True, exist_ok=True)
                    move(file, attachmentFolderPath.joinpath(file.name)) 
            else:
                totalImageProgress += 1 # since the for loop won't be executed, plus one for the next loop
        else:
            if downloadImageFlag:
                totalEl += len(imagesURLToDownloadArray)

                if lang == "en": downloadMessage = f"Downloading image no.{totalImageProgress} out of {totalEl}{END}"
                elif lang == "jp":  downloadMessage = f"画像 {totalImageProgress} / {totalEl} をダウンロード中"

                print_progress_bar(totalImageProgress, totalEl, downloadMessage)
                totalImageProgress += 1

        if downloadImageFlag:
            # Downloading all the retrieved images' URL
            if fantiaImageClassOffset > 0: 
                downloadFolder = subFolderPath.joinpath("website_displayed_images")
            else:
                downloadFolder = subFolderPath.joinpath("downloaded_images")
            
            counter = 0
            for imageURL in imagesURLToDownloadArray:
                downloadFolder.mkdir(parents=True, exist_ok=True)

                if downloadAttachmentFlag:
                    if lang == "en": downloadMessage = f"Downloading image/attachment no.{totalImageProgress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"画像やファイル {totalImageProgress} / {totalEl} をダウンロード中"
                else:
                    if lang == "en": downloadMessage = f"Downloading image no.{totalImageProgress} out of {totalEl}{END}"
                    elif lang == "jp":  downloadMessage = f"画像 {totalImageProgress} / {totalEl} をダウンロード中"

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

                print_progress_bar(totalImageProgress, totalEl, downloadMessage)
                totalImageProgress += 1

        print_download_completion_message(totalEl, subFolderPath, attachments=downloadAttachmentFlag, thumbnailNotice=thumbnailDownloadedCondition, images=downloadImageFlag)

    elif website == "Pixiv":
        totalEl = totalGdriveEl = 0
        gdriveLinks = []
        gdriveMessageInfo = 0
        if downloadGdriveLinks:
            gdriveFolder = subFolderPath.joinpath("gdrive-files")
            try:
                gdriveAnchors = driver.find_elements(by=By.XPATH, value="//a[starts-with(@href, 'https://drive.google.com/')]")
            except:
                gdriveAnchors = []

            try:
                potentialPasswords = driver.find_elements(by=By.XPATH, value="//div[@id='root']//*[text()[contains(., 'パス') or contains(., 'Pass') or contains(., 'pass') or contains(., '密码')]]")
            except:
                potentialPasswords = []
            
            if potentialPasswords and gdriveAnchors:
                gdriveFolder.mkdir(parents=True, exist_ok=True)
                with open(gdriveFolder.joinpath("password.txt"), "w") as f:
                    if lang == "en":
                        f.write(f"Post link: {urlInput}\n")
                        f.write("Passwords found potentially for the gdrive files!\n\n")
                    elif lang == "jp":
                        f.write(f"投稿リンク: {urlInput}\n")
                        f.write("gdriveファイルのパスワードの可能性が見つかりました！\n\n")
                    
                    f.writelines(el.text + "\n" for el in potentialPasswords)
            
            gdriveProgress = 0
            totalGdriveEl = len(gdriveAnchors)
            if gdriveAnchors: 
                gdriveLinks = [el.get_attribute("href") for el in gdriveAnchors]
                gdriveMessageInfo = len(gdriveLinks)

            for gdriveLink in gdriveLinks:
                if lang == "en": downloadMessage = f"Downloading gdrive file no.{gdriveProgress} out of {totalGdriveEl}{END}"
                elif lang == "jp": downloadMessage = f"gdriveファイル {gdriveProgress} / {totalGdriveEl} をダウンロード中"

                if gdriveProgress == 0:
                    print_progress_bar(gdriveProgress, totalGdriveEl, downloadMessage)
                    gdriveProgress += 1

                successCondition = execute_gdrive_download(gdriveLink, gdriveFolder)

                if not successCondition:
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.LIGHTRED_EX}Note: If there is a message above, please ignore the message above as it is printed by another library used by this program.\nThank you for your understanding.\n",
                            f"{F.LIGHTRED_EX}Error: Unable to download file from gdrive {END}",
                            f"{F.LIGHTRED_EX}This could be due to exceeding the gdrive API's quota limit for the day or the file being blocked for public downloads due to many views/downloads for that particular file. Please wait and try again later the next day.{END}",
                            f"{F.LIGHTRED_EX}A text file has been generated at\n{pixivDownloadLocation} for the gdrive urls that have yet to be downloaded by this program for the post, {urlInput}.{END}"
                        ),
                        jp=(
                            f"{F.LIGHTRED_EX}注意：上記のメッセージがある場合、このプログラムが使用している別のライブラリから出力されているため、無視してください。\nご理解のほど、よろしくお願いいたします。\n",
                            f"{F.LIGHTRED_EX}エラー: gdriveファイルのダウンロードに失敗しました。{END}",
                            f"{F.LIGHTRED_EX}これは、今日のgdrive APIのクオータリミットに達したか、ファイルが公開ダウンロードによってブロックされているかのいずれかです。次の日に再度お試しください。{END}",
                            f"{F.LIGHTRED_EX}このプログラムでダウンロードされていないgdriveファイルのURLを保存したテキストファイルは\n{pixivDownloadLocation}にあります。{END}"
                        )
                    )

                    pixivDownloadLocation.mkdir(parents=True, exist_ok=True)
                    textFilePath = pixivDownloadLocation.joinpath("gdrive-urls.txt")
                    if not textFilePath.is_file():
                        if lang == "en": heading = "List of incomplete gdrive links that have yet to be downloaded.\nYou are likely to be able to download these files manually if you're logged in.\n"
                        elif lang == "jp": heading = "まだダウンロードされていないgdriveファイルのリストです。\nログインしている場合、手動でダウンロードすることが可能です。\n"
                        with open(textFilePath, "w") as f:
                            f.write(heading)
                            f.write("\n")

                    timing = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                    if lang == "en": postLinkHeader = f"pixiv Fanbox post link: {urlInput}\n"
                    elif lang == "jp": postLinkHeader = f"pixivファンボックス投稿リンク: {urlInput}\n"
                    with open(textFilePath, "a") as f:
                        f.write(f"{timing}\n")
                        f.write(f"{postLinkHeader}")
                        for i in range(gdriveProgress-1, len(gdriveAnchors)):
                            f.write(f"{gdriveLinks[i]}\n")
                        f.write("\n")

                    gdriveMessageInfo = 0 # to prevent the success msg from being printed later
                    break

                if lang == "en": downloadMessage = f"Downloading gdrive file no.{gdriveProgress} out of {totalGdriveEl}{END}"
                elif lang == "jp": downloadMessage = f"gdriveファイル {gdriveProgress} / {totalGdriveEl} をダウンロード中"

                print_progress_bar(gdriveProgress, totalGdriveEl, downloadMessage)
                gdriveProgress += 1
            
            if gdriveLinks: 
                print("\n")
            
        thumbnailDownloadedCondition = False
        if downloadThumbnailFlag:
            try:
                thumbnailURL = driver.find_element(by=By.XPATH, value="//div[contains(@class, 'sc-1ryrgzm-2 ktnxOz')]").value_of_css_property("background-image").split('"')[1] # splitting the url by " since the value of the css property will return 'url("https://...")'
            except: 
                thumbnailURL = None
            
            if thumbnailURL:
                subFolderPath.mkdir(parents=True, exist_ok=True)
                imagePath = subFolderPath.joinpath(get_file_name(thumbnailURL, "Pixiv"))
                # no session needed since it's displayed regardless of membership status
                save_image(thumbnailURL, imagePath) 
                thumbnailDownloadedCondition = True

        urlToDownloadArray = []
        if downloadImageFlag:
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

            anchorURLArray = []
            if attachmentAnchors: 
                for anchor in attachmentAnchors:
                    anchorURLArray.append(anchor.get_attribute("href"))
                if gdriveLinks: print("\n")
                open_new_tab()
            
            del attachmentAnchors

            if downloadImageFlag: totalEl += len(urlToDownloadArray) + len(anchorURLArray)
            else: totalEl += len(anchorURLArray)

            remove_any_files_in_directory(browserDownloadLocation)
            for attachmentURL in anchorURLArray:
                if downloadImageFlag:
                    if lang == "en": downloadMessage = f"Downloading image/attachment no.{progress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"画像やファイル {progress} / {totalEl} をダウンロード中"
                else:
                    if lang == "en": downloadMessage = f"Downloading attachment no.{progress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"ファイル {progress} / {totalEl} をダウンロード中"

                if progress == 0:
                    print_progress_bar(progress, totalEl, downloadMessage)
                    progress += 1

                driver.get(attachmentURL) # getting the url which in turns downloads the attachments
                sleep(3) # for the browser to download the attachment

                if downloadImageFlag:
                    if lang == "en": downloadMessage = f"Downloading image/attachment no.{progress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"画像やファイル {progress} / {totalEl} をダウンロード中"
                else:
                    if lang == "en": downloadMessage = f"Downloading attachment no.{progress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"ファイル {progress} / {totalEl} をダウンロード中"

                print_progress_bar(progress, totalEl, downloadMessage)
                progress += 1

            if anchorURLArray:
                close_new_tab()
                check_for_incomplete_download()
                
                # moves all the files to the corresponding folder based on the user's input
                attachmentFolderPath = subFolderPath.joinpath("attachments")
                for file in browserDownloadLocation.iterdir():
                    attachmentFolderPath.mkdir(parents=True, exist_ok=True)
                    move(file, attachmentFolderPath.joinpath(file.name)) 
            else:
                progress += 1 # since the for loop won't be executed, plus one for the next loop
        else:
            if urlToDownloadArray: 
                if gdriveLinks: print("\n")

            if downloadImageFlag:
                totalEl += len(urlToDownloadArray)
                if lang == "en": downloadMessage = f"Downloading image no.{progress} out of {totalEl}{END}"
                elif lang == "jp":  downloadMessage = f"画像 {progress} / {totalEl} をダウンロード中"
                print_progress_bar(progress, totalEl, downloadMessage)
                progress += 1
        
        if downloadImageFlag:
            downloadFolder = subFolderPath.joinpath("downloaded_images")
            for url in urlToDownloadArray:
                downloadFolder.mkdir(parents=True, exist_ok=True)
                
                if pixivSession == None:
                    save_image(url, downloadFolder.joinpath(get_file_name(url, "Pixiv")))
                else:
                    save_image(url, downloadFolder.joinpath(get_file_name(url, "Pixiv")), session=pixivSession)

                if downloadAttachmentFlag:
                    if lang == "en": downloadMessage = f"Downloading image/attachment no.{progress} out of {totalEl}"
                    elif lang == "jp": downloadMessage = f"画像やファイル {progress} / {totalEl} をダウンロード中"
                else:
                    if lang == "en": downloadMessage = f"Downloading image no.{progress} out of {totalEl}{END}"
                    elif lang == "jp":  downloadMessage = f"画像 {progress} / {totalEl} をダウンロード中"

                print_progress_bar(progress, totalEl, downloadMessage)
                progress += 1
                
        print_download_completion_message(totalEl + totalGdriveEl, subFolderPath, attachments=downloadAttachmentFlag, thumbnailNotice=thumbnailDownloadedCondition, images=downloadImageFlag, gdriveNotice=gdriveMessageInfo)

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

def check_if_valid_folder_name(userFolderName):
    """
    Check if the folder name is according to the pattern of "Post-1"
    """
    if re.fullmatch(postNumFolderNameRegex, userFolderName): return True
    return False

def get_latest_post_num(folderPath):
    """
    Returns the highest post num folder name in the given folder path.
    
    Requires one argument to be defined:
    - A folder path (pathlib Path object)
    """
    postNumList = []
    try:
        for dirPath in folderPath.iterdir():
            if dirPath.is_dir():
                dirName = dirPath.name
                if check_if_valid_folder_name(dirName):
                    dirPath = str(dirName).split("-")
                    postNumList.append(int(dirPath[-1]))
        return max(postNumList) + 1
    except: return 0

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
                        en=(f"{F.RED}Warning: Folder already exists with files inside.\nAre you sure that you would like to download into the folder, {folderName}?{END}"),
                        jp=(f"{F.RED}警告： すでにファイルがあるフォルダーです。\n{folderName} にダウンロードしますか？{END}")
                    )
                    print("\n")
                    if lang == "en": prompt = f"Enter \"Y\" to continue or \"N\" to cancel: "
                    else: prompt = f"\"Y\"を入力して続行、\"N\"を入力してキャンセルします： "
                    
                    confirm = get_input_from_user(prompt=prompt, command=("y", "n"))
                    if confirm.lower() == "y": return imagePath
                    else: print("\n")
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
        print(f"""{F.LIGHTYELLOW_EX}
> ログイン・ステータス...
> Fantia: {fantiaStatus}
> Pixiv: {pixivStatus}
{END}
--------------------- {F.LIGHTYELLOW_EX}ダウンロードのオプション{END} ---------------------
      {F.GREEN}1. Fantia投稿URLから画像をダウンロードする{END}
      {F.GREEN}2. 全投稿ページのURLからFantiaの全投稿をダウンロードする。{END}
      {F.LIGHTCYAN_EX}3. Pixivファンボックスの投稿URLから画像をダウンロードする{END}
      {F.LIGHTCYAN_EX}4. 全投稿ページのURLからPixivファンボックスの全投稿をダウンロードする。{END}

---------------------- {F.LIGHTYELLOW_EX}コンフィグのオプション{END} ----------------------
      {F.LIGHTBLUE_EX}5. デフォルトのダウンロードフォルダを変更する{END}
      {F.LIGHTBLUE_EX}6. ブラウザを変更する{END}
      {F.LIGHTBLUE_EX}7. 言語を変更する{END}""")

        if fantiaStatus == "ゲスト（ログインしていない）" or pixivStatus == "ゲスト（ログインしていない）":
            print(f"      {F.LIGHTBLUE_EX}8. ログインする{END}")

        print(f"\n-------------------------- {F.LIGHTYELLOW_EX}他のオプション{END} ---------------------------")
        if appPath.joinpath("configs", "pixiv_cookies").is_file() or appPath.joinpath("configs", "fantia_cookies").is_file(): 
            print(f"      {F.LIGHTRED_EX}DC. 保存されたクッキーを削除する{END}")

        if check_if_directory_has_files(appPath.joinpath("configs")): 
            print(f"      {F.RED}D. Cultured Downloaderで作成されたデータをすべて削除します。{END}")

        print(f"      {F.LIGHTRED_EX}Y. バグを報告する{END}")
        print(f"      {F.RED}X. プログラムを終了する{END}")
        print()
    else:
        print(f"""{F.LIGHTYELLOW_EX}
> Login Status...
> Fantia: {fantiaStatus}
> Pixiv: {pixivStatus}
{END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{END} --------------------
      {F.GREEN}1. Download images from a Fantia post URL{END}
      {F.GREEN}2. Download all Fantia posts from an all posts page URL{END}
      {F.LIGHTCYAN_EX}3. Download images from a pixiv Fanbox post URL{END}
      {F.LIGHTCYAN_EX}4. Download all pixiv Fanbox posts from an all posts page URL{END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{END} ----------------------
      {F.LIGHTBLUE_EX}5. Change Default Download Folder{END}
      {F.LIGHTBLUE_EX}6. Change Default Browser{END}
      {F.LIGHTBLUE_EX}7. Change Language{END}""")
        
        if fantiaStatus == "Guest (Not logged in)" or pixivStatus == "Guest (Not logged in)":
            print(f"      {F.LIGHTBLUE_EX}8. Login{END}")

        print(f"\n---------------------- {F.LIGHTYELLOW_EX}Other Options{END} ----------------------")
        if appPath.joinpath("configs", "pixiv_cookies").is_file() or appPath.joinpath("configs", "fantia_cookies").is_file(): 
            print(f"      {F.LIGHTRED_EX}DC. Delete saved cookies{END}")

        if check_if_directory_has_files(appPath.joinpath("configs")): 
            print(f"      {F.RED}D. Delete all data created by Cultured Downloader{END}")

        print(f"      {F.LIGHTRED_EX}Y. Report a bug{END}")
        print(f"      {F.RED}X. Shutdown the program{END}")
        print()

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

    # checks if config.json exists and if it's readable
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
        driver = get_driver(selectedBrowser, quiet=True)
    else: 
        selectedBrowser = loadBrowser
        driver = get_driver(loadBrowser, quiet=True)

    # retrieve cookie if exists
    pixivCookieLoaded, fantiaCookieLoaded = load_cookies()
    pixivCookieExist = appPath.joinpath("configs", "pixiv_cookies").is_file()
            
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
    else: pixivSession = None

    cmdInput = ""
    cmdCommands = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11" "d", "dc", "x", "y")
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

                    urlInput = get_url_inputs("fantiaPost", (
                        "Enter the URL of the Fantia post (X to cancel): ",
                        "Fantiaの投稿のURLを入力します (Xでキャンセル)： "
                    ))
                    if not urlInput:
                        startDownloadingFlag = False
                        break
                    elif urlInput != "invalid":
                        break

                if startDownloadingFlag:
                    try:
                        execute_download_process(urlInput, imagePath, "postPage", "fantia")
                    except KeyboardInterrupt:
                        print("\n")
                        print_in_both_en_jp(
                            en=(f"{F.LIGHTYELLOW_EX}Download cancelled by user...{END}"),
                            jp=(f"{F.LIGHTYELLOW_EX}ダウンロードがキャンセルされました...{END}")
                        )

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
                            f"{F.LIGHTYELLOW_EX}Please enter the base URL first! (e.g. https://fantia.jp/fanclubs/5744/posts){END}",
                            f"{F.LIGHTYELLOW_EX}For multiple inputs, please add a comma in between the urls.\n(e.g. https://fantia.jp/fanclubs/5744/posts, https://fantia.jp/fanclubs/14935/posts){END}",
                            f"{F.LIGHTYELLOW_EX}Afterwards, you will be prompted to enter the number of pages in this format, \"1-5\" or \"5\" to indicate page 1 to 5 or page 5 respectively.{END}"
                        ), 
                        jp=(
                            f"{F.LIGHTYELLOW_EX}最初にベースURLを入力してください (例: https://fantia.jp/fanclubs/5744/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}複数のURLを入力する場合は、URLの後にコンマを入力してください。\n(例: https://fantia.jp/fanclubs/5744/posts、https://fantia.jp/fanclubs/14935/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}その後、ページ数を入力する画面になるので、1～5ページを示す \"1-5\"やページ5を示す\"5\"を入力下さい。{END}"
                        )
                    )
                    urlInput = get_url_inputs("fantiaPostPage", (
                        "Enter the URL of Fantia's all posts page (X to cancel): ",
                        "Fantiaの全投稿ページのURLを入力下さい (Xでキャンセル)： "
                    ))
                    if not urlInput:
                        startDownloadingFlag = False
                        break
                    elif urlInput != "invalid":
                        break
                
                # asking the user for the number of pages to download
                if startDownloadingFlag:
                    pageInput = get_page_num(urlInput)
                    if not pageInput: startDownloadingFlag = False

                if startDownloadingFlag:
                    try:
                        execute_download_process(urlInput, imagePath, "postPreviewPage", "fantia", pageInput=pageInput)
                    except KeyboardInterrupt:
                        print("\n")
                        print_in_both_en_jp(
                            en=(f"{F.LIGHTYELLOW_EX}Download cancelled by user...{END}"),
                            jp=(f"{F.LIGHTYELLOW_EX}ダウンロードがキャンセルされました...{END}")
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
                    
                    urlInput = get_url_inputs("pixivFanbox", (
                        "Enter the URL of the Pixiv Fanbox post (X to cancel): ",
                        "Pixivファンボックスの投稿URLを入力してください (Xでキャンセル)： "
                    ))
                    if not urlInput:
                        startDownloadingFlag = False
                        break
                    elif urlInput != "invalid":
                        break

                if startDownloadingFlag:
                    try:
                        execute_download_process(urlInput, imagePath, "postPage", "pixiv")
                    except KeyboardInterrupt:
                        print("\n")
                        print_in_both_en_jp(
                            en=(f"{F.LIGHTYELLOW_EX}Download cancelled by user...{END}"),
                            jp=(f"{F.LIGHTYELLOW_EX}ダウンロードがキャンセルされました...{END}")
                        )
        
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
                            f"{F.LIGHTYELLOW_EX}Please enter the base URL first! (e.g. https://www.fanbox.cc/@creator_name/posts){END}",
                            f"{F.LIGHTYELLOW_EX}For multiple inputs, please add a comma in between the urls.\n(e.g. https://www.fanbox.cc/@creator_name_one/posts, https://www.fanbox.cc/@creator_name_two/posts){END}",
                            f"{F.LIGHTYELLOW_EX}Afterwards, you will be prompted to enter the number of pages in this format, \"1-5\" or \"5\" to indicate page 1 to 5 or page 5 respectively.{END}"
                        ), 
                        jp=(
                            f"{F.LIGHTYELLOW_EX}最初にベースURLを入力してください (例: https://www.fanbox.cc/@creator_name/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}複数のURLを入力する場合は、URLの後にコンマを入力してください。\n(例: https://www.fanbox.cc/@creator_name_one/posts、https://www.fanbox.cc/@creator_name_two/posts)。{END}",
                            f"{F.LIGHTYELLOW_EX}その後、ページ数を入力する画面になるので、1～5ページを示す \"1-5\"やページ5を示す\"5\"を入力下さい。{END}"
                        )
                    )

                    urlInput = get_url_inputs("pixivFanboxPostPage", (
                        "Enter the URL of the pixiv Fanbox all posts page (X to cancel): ",
                        "pixivファンボックスの全投稿ページのURLを入力下さい (Xでキャンセル)： "
                    ))
                    if not urlInput:
                        startDownloadingFlag = False
                        break
                    elif urlInput != "invalid":
                        break
                
                # asking the user for the number of pages to download
                if startDownloadingFlag:
                    pageInput = get_page_num(urlInput)
                    if not pageInput: startDownloadingFlag = False

                if startDownloadingFlag:
                    try:
                        execute_download_process(urlInput, imagePath, "postPreviewPage", "pixiv", pageInput=pageInput)
                    except KeyboardInterrupt:
                        print("\n")
                        print_in_both_en_jp(
                            en=(f"{F.LIGHTYELLOW_EX}Download cancelled by user...{END}"),
                            jp=(f"{F.LIGHTYELLOW_EX}ダウンロードがキャンセルされました...{END}")
                        )

        elif cmdInput == "5":
            print_in_both_en_jp(
                en=(f"\n{F.LIGHTRED_EX}Note: You will have to re-login again after changing your default download location.{END}"),
                jp=(f"\n{F.LIGHTRED_EX}注意: デフォルトのダウンロード先を変更した後は、再度ログインする必要があります。{END}")
            )
            try:
                with open(jsonPath, "r") as f:
                    config = json.load(f)
            except JSONDecodeError:
                config = {}
                with open(jsonPath, "w") as f:
                    json.dump(config, f)

            set_default_download_directory(config, setDefaultLocationUponCancellation=False, printSuccessMsg=False)
            newDirectoryPath = get_default_download_directory()
            if directoryPath != newDirectoryPath:
                directoryPath = newDirectoryPath

                fantiaDownloadLocation = directoryPath.joinpath("fantia_downloads")
                fantiaDownloadLocation.mkdir(parents=True, exist_ok=True)

                pixivDownloadLocation = directoryPath.joinpath("pixiv_downloads")
                pixivDownloadLocation.mkdir(parents=True, exist_ok=True)

                browserDownloadLocation = directoryPath.joinpath("browser_downloads")
                browserDownloadLocation.mkdir(parents=True, exist_ok=True)

                print_in_both_en_jp(
                    en=(f"{F.GREEN}The default folder has been changed to {newDirectoryPath}{END}"),
                    jp=(f"{F.GREEN}デフォルトフォルダを {newDirectoryPath} に変更しました。{END}")
                )

                driver.quit()
                driver = get_driver(selectedBrowser, quiet=True)

                print_in_both_en_jp(
                    en=(f"\n{F.LIGHTRED_EX}You will now have to login again by manually logging in or loading in your cookies.{END}"),
                    jp=(f"\n{F.LIGHTRED_EX}手動でログインするか、クッキーを読み込んで再度ログインする必要があります。{END}")
                )

                pixivCookieLoaded, fantiaCookieLoaded = load_cookies()
                if pixivCookieLoaded: 
                    pixivSession = get_cookie_for_session("pixiv")
            else:
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}No changes were made to the default download location.{END}"),
                    jp=(f"{F.LIGHTYELLOW_EX}デフォルトのダウンロード先は変更されませんでした。{END}")
                )
            
        elif cmdInput == "6":
            print_in_both_en_jp(
                en=(f"\n{F.LIGHTRED_EX}Note: You will have to re-login again after changing your browser.{END}"),
                jp=(f"\n{F.LIGHTRED_EX}注意: ブラウザを変更した後に再度ログインする必要があります。{END}")
            )
            defaultBrowser = check_browser_config()
            if defaultBrowser != None:
                newDefaultBrowser = get_user_browser_preference()
                if newDefaultBrowser == defaultBrowser:
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTYELLOW_EX}No changes were made to the default browser.{END}"),
                        jp=(f"{F.LIGHTYELLOW_EX}デフォルトブラウザは変更されませんでした。{END}")
                    )
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Error: No default browser found.{END}"),
                    jp=(f"{F.RED}エラー： デフォルトのブラウザが見つかりませんでした。{END}")
                )
                defaultBrowser = selectedBrowser

                if lang == "en": browserPrompt = "Would you like to save a browser as your default browser for this program? (y/n): "
                else: browserPrompt = "このプログラムのデフォルトのブラウザを保存しますか？ (y/n): "
                saveBrowser = get_input_from_user(prompt=browserPrompt, command=("y", "n"))

                if saveBrowser == "y":
                    newDefaultBrowser = get_user_browser_preference()
                    if newDefaultBrowser == defaultBrowser:
                        print_in_both_en_jp(
                            en=(f"{F.LIGHTYELLOW_EX}No changes were made to the default browser.{END}"),
                            jp=(f"{F.LIGHTYELLOW_EX}デフォルトブラウザは変更されませんでした。{END}")
                        )
                else: 
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTRED_EX}Note: Default Browser is empty in config.json{END}"),
                        jp=(f"{F.LIGHTRED_EX}注意： config.jsonのデフォルトブラウザが空です。{END}")
                    )
                    newDefaultBrowser = selectedBrowser

            if newDefaultBrowser != defaultBrowser: 
                save_browser_config(newDefaultBrowser)
                driver.quit()
                driver = get_driver(newDefaultBrowser, quiet=True)

                pixivCookieLoaded, fantiaCookieLoaded = load_cookies()
                if pixivCookieLoaded: 
                    pixivSession = get_cookie_for_session("pixiv")

                selectedBrowser = newDefaultBrowser
            
        elif cmdInput == "7":
            lang = update_lang()

        elif cmdInput == "8":
            if not check_if_user_is_logged_in():
                pixivCookieExist = appPath.joinpath("configs", "pixiv_cookies").is_file()
                fantiaCookieExist = appPath.joinpath("configs", "fantia_cookies").is_file()

                if pixivCookieExist or fantiaCookieExist:
                    pixivCookieLoaded, fantiaCookieLoaded = load_cookies()
                    if pixivCookieLoaded: 
                        pixivSession = get_cookie_for_session("pixiv")

                if not pixivCookieLoaded:
                    pixivCookieLoaded, pixivSessionID = save_and_load_cookie(driver, "pixiv", getID=True)
                    if pixivCookieLoaded:
                        pixivSession = get_cookie_for_session("pixiv", sessionID=pixivSessionID)

                if not fantiaCookieLoaded:
                    fantiaCookieLoaded = save_and_load_cookie(driver, "fantia")
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )

        elif cmdInput == "d":
            if check_if_directory_has_files(appPath):
                for folderPath in appPath.iterdir():
                    if folderPath.is_dir():
                        rmtree(folderPath)
                print_in_both_en_jp(
                    en=(f"{F.LIGHTRED_EX}Deleted folders in {appPath}{END}"),
                    jp=(f"{F.LIGHTRED_EX}{appPath} 内のフォルダーを削除しました。{END}")
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
                        en=(f"{F.LIGHTRED_EX}Deleted Pixiv Fanbox cookies{END}"),
                        jp=(f"{F.LIGHTRED_EX}Pixivファンボックスのクッキーが削除されました。{END}")
                    )
                
                fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
                if fantiaCookiePath.is_file():
                    fantiaCookiePath.unlink()
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTRED_EX}Deleted Fantia cookies{END}"),
                        jp=(f"{F.LIGHTRED_EX}Fantiaのクッキーが削除されました。{END}")
                    )
    
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )

        elif cmdInput == "y": webbrowser.open("https://github.com/KJHJason/Cultured-Downloader/issues", new=2)

"""--------------------------- End of Main Codes ---------------------------"""

if __name__ == "__main__":
    coloramaInit(autoreset=False, convert=True)
    global END
    END = Style.RESET_ALL

    global queryWebsite
    queryWebsite = "https://cultureddownloader.com/query"

    global postNumFolderNameRegex
    global fantiaPostRegex
    global fantiaPostPageRegex
    global pixivFanboxPostRegex
    global pixivFanboxPostPageRegex
    global pageNumRegex

    postNumFolderNameRegex = re.compile(r"^(Post-)(\d+)$")
    fantiaPostRegex = re.compile(r"(https://fantia.jp/posts/)\d+")
    fantiaPostPageRegex = re.compile(r"(https://fantia.jp/fanclubs/)\d+(/posts)")
    pixivFanboxPostRegex = re.compile(r"(https://www.fanbox.cc/@)[\w&.-]+(/posts/)\d+|(https://)[\w&.-]+(.fanbox.cc/posts/)\d+") # [\w&.-]+ regex from https://stackoverflow.com/questions/13946651/matching-special-characters-and-letters-in-regex
    pixivFanboxPostPageRegex = re.compile(r"(https://www.fanbox.cc/@)[\w&.-]+(/posts)|(https://)[\w&.-]+(.fanbox.cc/posts)") 
    pageNumRegex = re.compile(r"[1-9][0-9]{0,}(-)[1-9][0-9]{0,}|[1-9][0-9]{0,}") # ensures that the user cannot enter page 0 or negative numbers

    introMenu = f"""
=========================================== {F.LIGHTBLUE_EX}CULTURED DOWNLOADER v{__version__ }{END} ===========================================
================================ {F.LIGHTBLUE_EX}https://github.com/KJHJason/Cultured-Downloader{END} =================================
===================================== {F.LIGHTBLUE_EX}Author/開発者: {__author__}, aka Dratornic{END} =====================================
====================================== {F.LIGHTBLUE_EX}License/ライセンス: {__license__}{END} =======================================

{F.LIGHTYELLOW_EX}
Purpose/目的: Allows you to download multiple images from Fantia or Pixiv Fanbox automatically.
              FantiaやPixivファンボックスから複数の画像を自動でダウンロードできるようにします。

Note/注意:    Requires the user to login via this program for images that requires a membership.
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
    code = 0
    try:
        check_for_new_ver()
        main()
        shutdown()
    except KeyboardInterrupt:
        print(f"\n{F.RED}Program Terminated/プログラムが終了しました{END}")
        sleep(1)
    except (EncryptionKeyError, DecryptError):
        delete_encrypted_data()
        code = 1
    except (SessionError, EOFError):
        # deletes any saved files created by this program
        remove_any_files_in_directory(get_saved_config_data_folder().joinpath("configs"))

        print_in_both_en_jp(
            en=(f"{F.RED}Error: Unable to read saved files...{END}", f"Please restart this program.{END}", "Please enter any key to exit..."),
            jap=(f"{F.RED}エラー：  保存したファイルを読み込めない...{END}", "このプログラムを再起動してください。{END}", "何か入力すると終了します...")
        )
        input()
        code = 1
    except:
        log_error()
        print_error_log_notification()

        input("Please enter any key to exit/何か入力すると終了します...")
        code = 1
    finally:
        print(f"{F.RED}Exiting/終了しています...{END}")
        # shuts down the webdriver session
        try: driver.quit()
        except: pass
        osExit(code)