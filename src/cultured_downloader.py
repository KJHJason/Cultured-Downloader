__author__ = "KJHJason"
__copyright__ = "Copyright 2022 KJHJason"
__credits__ = ["KJHJason"]
__license__ = "MIT License"
__version__ = "2.0.0"

# Import Third-party Libraries
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

# Import Standard Libraries
import pathlib, json, sys, logging, webbrowser
from urllib.parse import urlparse
from json.decoder import JSONDecodeError
from time import sleep
from datetime import datetime
from shutil import rmtree, copyfileobj
from base64 import b64encode, b64decode

# Importing my Python Files as Modules
from ChaChaData import ChaChaData

"""--------------------------- Config Codes ---------------------------"""

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

def shutdown():
    """
    Shutdown the program via sys.exit() and closes any webdriver session.
    """
    if lang == "en":
        print(f"{F.LIGHTYELLOW_EX}Thank you for using Cultured Downloader.{END}")
        input("Please enter any key to exit...")
    else:
        print(f"{F.LIGHTYELLOW_EX}Cultured Downloaderをご利用いただきありがとうございます。{END}")
        input("何か入力すると終了します。。。")
    try: driver.close()
    except: pass
    sys.exit()

def print_error_log_notification():
    """
    Used for alerting the user of where the log file is located at and to report this bug to the developer.
    """
    logFolderPath = get_saved_config_data_folder().joinpath("logs")
    print(f"\n{F.RED}Unknown Error Occurred/不明なエラーが発生した{END}")
    print(f"{F.RED}Please provide the developer with a error text file generated in {logFolderPath}\n{logFolderPath}に生成されたエラーテキストファイルを開発者に提供してください。\n{END}")
    try: driver.close()
    except: pass

def log_error():
    """
    Used for writing the error to a log file usually located in the Cultured Downloader folder in the AppData LocalLow folder.
    """
    filePath = get_saved_config_data_folder().joinpath("logs")
    if not filePath.is_dir(): filePath.mkdir(parents=True)

    fileName = "".join([f"error-", datetime.now().strftime("%d-%m-%Y"), ".log"])
    fullFilePath = filePath.joinpath(fileName)
    
    if not fullFilePath.is_file():
        with open(fullFilePath, "w") as f:
            f.write(f"Cultured Downloader v{__version__ } Error Logs\n\n")
    else:
        with open(fullFilePath, "a") as f:
            f.write(f"\n")

    logging.basicConfig(filename=fullFilePath, filemode="a", format="%(asctime)s - %(message)s")
    logging.error("Error Details: ", exc_info=True)

def error_shutdown(**errorMessages):
    """
    Param:
    - en for English error messages
    - jp for Japanese error messages

    Used for shutting down the program when an error occurs.
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

    driver.close()
    log_error()
    sleep(2)
    raise SystemExit

def print_in_both_en_jp(**message):
    """
    Used for printing either English or Japanese messages.

    Param:
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

    Param:
    - prompt: The prompt to be displayed to the user.
    - prints: The message to be printed to the user.
    - command: The input to be accepted by the program.
    - warning: Used for displaying a custom error message.

    Defaults:
    - command: None but must be defined at all time as it will raise a ValueError if not defined
    - prompt: "", an input without any prompt
    - prints: None, will not print out any messages
    - warning: None, will not display any error messages
    """
    prints = kwargs.get("prints")

    prompt = kwargs.get("prompt")
    if prompt == None: prompt = ""

    commands = kwargs.get("command")
    if commands == None: raise ValueError("command parameter must be defined in the function, get_input_from_user")

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
    if not jsonFolderPath.is_dir(): jsonFolderPath.mkdir(parents=True)
    if not jsonPath.is_file():
        print(f"{F.RED}Error: config.json does not exist.{END}", f"{F.LIGHTYELLOW_EX}Creating config.json file...{END}"),
        print(f"{F.RED}エラー: config.jsonが存在しません。{END}", f"{F.LIGHTYELLOW_EX}config.jsonファイルを作成しています...{END}")
        
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
    Returns a pathlib Path object of the saved config data folder which is in the AppData LocalLow folder.
    """
    dataDirectory = pathlib.Path.home().joinpath("AppData", "LocalLow", "Cultured Downloader")
    if not dataDirectory.is_dir(): dataDirectory.mkdir(parents=True)
    return dataDirectory

def get_driver(browserType, **additionalOptions):
    """
    Requires one argument to be defined:: 
    - "chrome"
    - "edge"

    Optional param:
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
            "download.default_directory": str(pixivDownloadLocation),
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
            "download.default_directory": str(pixivDownloadLocation),
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

    # driver.minimize_window()
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
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
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
    defaultDownloadFolderPath = pathlib.Path.home().joinpath("Desktop", "Cultured Downloader")
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

def set_default_download_directory(jsonConfig):
    """
    To set the user's default download directory by prompting to enter the full path on their pc and save it to config.json

    Requires one argument to be defined:
    - the config dictionary obtained from reading config.json
    """
    if lang == "en": 
        downloadFolderPrompt = "Would you like to change the default download location? (y/n): "
        downloadFolderChangePrompt = "Enter the FULL path of the download folder (X to cancel): "
    elif lang == "jp": 
        downloadFolderPrompt = "デフォルトのダウンロード場所を変更しますか？(y/n)： "
        downloadFolderChangePrompt = "ダウンロードフォルダのフルパスを入力してください (\"X\"でキャンセル)： "

    else: downloadFolderPrompt = "Would you like to change the default download location?/デフォルトのダウンロード場所を変更しますか？ (y/n):"

    downloadFolderChangeInput = get_input_from_user(prompt=downloadFolderPrompt, command=("y", "n"))

    if downloadFolderChangeInput == "n": return set_default_download_directory_to_desktop(jsonConfig)
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
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
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
    """
    keyPath = appPath.joinpath("configs", "key")
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

        encryptedData = json.dumps(dict(zip(dictKeys, valuesList))) # converts both lists to a dictionary then serialises it to a string

        return ChaChaData(encryptedData)
    else:
        raise Exception("Data to be encrypted is not a dictionary...")

def decrypt_data(encryptedData):
    """
    To decrypt the data using the global variable ChaChaKey obtained from the function get_key as the encryption key

    Requires one argument to be defined:
    - A dictionary containing the encrypted values
    """
    try:
        b64encodedDict = json.loads(encryptedData.get_encrypted_data()) # a dictionary of b64encoded values
        b64decodedDict = {key:b64decode(b64encodedDict[key]) for key in b64encodedDict.keys()}

        cipher = Cha.new(key=ChaChaKey, nonce=b64decodedDict["nonce"])
        cipher.update(b64decodedDict["header"])

        plaintext = cipher.decrypt_and_verify(b64decodedDict["cipherText"], b64decodedDict["tag"])
        return json.loads(plaintext.decode())
    except (ValueError, KeyError, TypeError):
        raise DecryptError

"""--------------------------- End of Config Codes ---------------------------"""

"""--------------------------- Start of Functions Codes ---------------------------"""

def check_if_input_is_url(inputString):
    """
    Validates if the user's inputs is a valid URL

    Requires one argument to be defined:
    - A string or a list
    """
    if type(inputString) != list:
        try:
            result = urlparse(inputString)
            return all([result.scheme, result.netloc])
        except:
            return False
    else:
        for url in inputString:
            try:
                result = urlparse(url)
                if not all([result.scheme, result.netloc]): return False
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
def get_pixiv_cookie():
    """
    For Pixiv, it will return the cookie of the pixiv account needed for the login session used for the download of the images via the requests library.

    Will return a requests session object with the pixiv cookie data if the cookie file exists.

    Otherwise, it will return an empty string, "".
    """
    cookiePath = appPath.joinpath("configs", "pixiv_cookies")

    if cookiePath.is_file():
        pixivSessionID = ""
        with open(cookiePath, 'rb') as f:
            pixivCookie = decrypt_data(dill.load(f))
            if pixivCookie["name"] == "FANBOXSESSID":
                pixivSessionID = pixivCookie["value"]
        
        if pixivSessionID != "":
            pixivSessionObject = requests.session()
            pixivSessionIDCookie = requests.cookies.create_cookie(domain="fanbox.cc", name="FANBOXSESSID", value=pixivSessionID)
            pixivSessionObject.cookies.set_cookie(pixivSessionIDCookie)
            return pixivSessionObject
        else: return ""
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

        sleep(5)

        with open(cookiePath, 'rb') as f:
            cookie = decrypt_data(dill.load(f))

        driver.delete_all_cookies()
        driver.add_cookie(cookie)

        if website == "fantia": websiteURL = "https://fantia.jp/mypage/users/plans"
        else: websiteURL = "https://www.fanbox.cc/messages"

        driver.get(websiteURL)
        sleep(5)
        if driver.current_url == websiteURL: 
            print_in_both_en_jp(
                en=(f"{F.GREEN}{website.title()} cookied loaded successfully!{END}"),
                jp=(f"{F.GREEN}{website.title()}のクッキーが正常に読み込まれました！{END}")
            )
            return True
        else: return False
    else: return False

def get_image_name(imageURL, website):
    """
    Returns the image file name based on the URL given.

    Requires two arguments to be defined:
    - The image's URL (string)
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
    currentProg = prog / totalEl
    sys.stdout.write("\r")
    sys.stdout.write(f"{F.LIGHTYELLOW_EX}[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}{END}")
    sys.stdout.flush()

def print_download_completion_message(totalImage, subFolderPath):
    """
    For printing the completion message to alert the user that all the images have been downloaded.

    Requires two arguments to be defined:
    - The total number of images (int)
    - The path to the folder where the images are saved (pathlib Path object or a string)
    """
    if totalImage > 0:
        print_in_both_en_jp(
            en=(
                f"\n{F.GREEN}Successfully downloaded {totalImage} images at\n{subFolderPath}{END}"
            ),
            jp=(
                f"\n{F.GREEN}{subFolderPath} に{totalImage}枚の画像をダウンロードしました!{END}"
            )
        )
        print("\n")
    else:
        print_in_both_en_jp(
            en=(f"\n{F.RED}Error: No images to download.{END}"),
            jp=(f"\n{F.RED}エラー： ダウンロードする画像がありません。{END}")
        )
        print("\n")

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

def get_latest_post_num_from_file_name():
    """
    To retrieve the latest/highest post_num from all the files in the pixiv_downloads folder.

    This is used when the requests session object is not defined and is equal to "".

    Returns the latest/highest post_num (int)
    """
    postNumList = []
    try:
        for filePath in pixivDownloadLocation.iterdir():
            if filePath.is_file():
                filePath = str(filePath.name).split("_")
                postNumList.append(int(filePath[1]))
        return max(postNumList) + 1
    except:
        return 0

# a failsafe function if pixivSession is equal to ""
def download_image_javascript(imageSrcURL, imageName):
    """
    Returns a javascript code to be executed for downloading pixiv images on the webdriver browser.

    Requires two arguments to be defined:
    - The image's URL (string)
    - The image's name (string)
    """
    downloadImageHeaderJS = """function download(imageURL) {"""
    downloadImageFooterJS = f"""
    const fileName = "{imageName}"  + imageURL.split('/').pop();
    var el = document.createElement("a");
    el.setAttribute("href", imageURL);
    el.setAttribute("download", fileName);
    document.body.appendChild(el);
    el.click();
    el.remove();
"""
    downloadImageExecuteFn = f"download('{imageSrcURL}');"
    
    return "".join([downloadImageHeaderJS, downloadImageFooterJS, "}\n", downloadImageExecuteFn])

def download(urlInput, website, subFolderPath):
    """
    To download images from Fantia or pixiv Fanbox.

    Requires three arguments to be defined:
    - The url of the Fantia/pixiv posts or the Fantia image url (string)
    - The website which is either "FantiaImageURL", "FantiaPost", or "Pixiv" (string)
    - The path to the folder where the images are saved or a string which will be the latest post num for pixiv downloads (pathlib Path object or a string)
    """
    driver.get(urlInput)

    if website == "FantiaImageURL":
        # downloading nth num of images based on the Fantia image given
        # e.g. https://fantia.jp/posts/*/post_content_photo/*
        imageSrc = driver.find_element(by=By.XPATH, value="/html/body/img").get_attribute("src")
        imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Fantia"))
        save_image(imageSrc, imagePath)

    elif website == "FantiaPost":
        sleep(5)
        try: fullyDisplayedImageAnchor = driver.find_elements(by=By.XPATH, value="//a[@class='image-container clickable']")
        except: fullyDisplayedImageAnchor = []

        totalFullyDisplayedImages = len(fullyDisplayedImageAnchor)

        if totalFullyDisplayedImages > 0:
            downloadFolder = subFolderPath.joinpath("stage_1")
            downloadFolder.mkdir(parents=True, exist_ok=True)
        else:
            print_in_both_en_jp(
                en=(f"{F.LIGHTYELLOW_EX}\nSkipping stage 1...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}\nステージ1をスキップします...{END}")
            )

        fullyDisplayedImageContainerArray = []
        for anchor in fullyDisplayedImageAnchor:
            anchor.click()
            sleep(0.5)
            fullyDisplayedImageURL = driver.find_element(by=By.XPATH, value="//a[contains(text(),'オリジナルサイズを表示 ')]").get_attribute("href")
            fullyDisplayedImageContainerArray.append(fullyDisplayedImageURL)
            driver.find_element(by=By.XPATH, value="//a[@class='btn btn-dark btn-sm']").click()
            sleep(0.5)

        fullyDisplayedImagesProgress = 0
        for imageURL in fullyDisplayedImageContainerArray:
            if fullyDisplayedImagesProgress == 0:
                if lang == "en":
                    print_progress_bar(fullyDisplayedImagesProgress, totalFullyDisplayedImages, f"Stage 1: Downloading image no.{fullyDisplayedImagesProgress} out of {totalFullyDisplayedImages}")
                elif lang == "jp":
                    print_progress_bar(fullyDisplayedImagesProgress, totalFullyDisplayedImages, f"ステージ 1: 画像 {fullyDisplayedImagesProgress} / {totalFullyDisplayedImages} をダウンロード中")
                fullyDisplayedImagesProgress += 1

            driver.get(imageURL)
            sleep(1)
            image = driver.find_element(by=By.XPATH, value="/html/body/img")
            imageSrc = image.get_attribute("src")
            imagePath = downloadFolder.joinpath(get_image_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)

            if lang == "en":
                print_progress_bar(fullyDisplayedImagesProgress, totalFullyDisplayedImages, f"Stage 1: Downloading image no.{fullyDisplayedImagesProgress} out of {totalFullyDisplayedImages}")
            elif lang == "jp":
                print_progress_bar(fullyDisplayedImagesProgress, totalFullyDisplayedImages, f"ステージ 1: 画像 {fullyDisplayedImagesProgress} / {totalFullyDisplayedImages} をダウンロード中")
            
            fullyDisplayedImagesProgress += 1
            close_new_tab()

        try: imagePosts = driver.find_elements(by=By.CLASS_NAME, value="fantiaImage")
        except: imagePosts = []

        totalImagePosts = len(imagePosts)

        if totalImagePosts > 0:
            downloadFolder = subFolderPath.joinpath("stage_2")
            downloadFolder.mkdir(parents=True, exist_ok=True)
        else:
            print_in_both_en_jp(
                en=(f"{F.LIGHTYELLOW_EX}\nSkipping stage 2...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}\nステージ2をスキップします...{END}")
            )

        # downloading Fantia blog images that are may be locked by default due to membership restrictions
        if totalFullyDisplayedImages > 0: print("\n")
        imagePostsProgress = 0
        for imagePost in imagePosts:
            if imagePostsProgress == 0:
                if lang == "en":
                    print_progress_bar(imagePostsProgress, totalImagePosts, f"Stage 2: Downloading image no.{imagePostsProgress} out of {totalImagePosts}")
                elif lang == "jp":
                    print_progress_bar(imagePostsProgress, totalImagePosts, f"ステージ 2: 画像 {imagePostsProgress} / {totalImagePosts} をダウンロード中")
                imagePostsProgress += 1

            imageHREFLink = imagePost.get_attribute("href")
            open_new_tab()
            driver.get(imageHREFLink)
            image = driver.find_element(by=By.XPATH, value="/html/body/img")
            imageSrc = image.get_attribute("src")
            imagePath = downloadFolder.joinpath(get_image_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)

            if lang == "en":
                print_progress_bar(imagePostsProgress, totalImagePosts, f"Stage 2: Downloading image no.{imagePostsProgress} out of {totalImagePosts}")
            elif lang == "jp":
                print_progress_bar(imagePostsProgress, totalImagePosts, f"ステージ2: 画像 {imagePostsProgress} / {totalImagePosts} をダウンロード中")
            
            imagePostsProgress += 1
            close_new_tab()

        # downloading Fantia images that are locked by default unless the user has a monthly subscription to the artist
        driver.get(urlInput)
        sleep(5)
        try: premiumImages = driver.find_elements(by=By.XPATH, value="//a[@class='image-container force-square clickable']")
        except: premiumImages = []
        
        totalPremiumImages = len(premiumImages)

        if totalPremiumImages > 0:
            downloadFolder = subFolderPath.joinpath("stage_3")
            downloadFolder.mkdir(parents=True, exist_ok=True)
        else:
            print_in_both_en_jp(
                en=(f"{F.LIGHTYELLOW_EX}\nSkipping stage 3...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}\nステージ3をスキップします...{END}")
            )
        
        paidImageContainerArray = []
        for paidImageContainer in premiumImages:
            paidImageContainer.click()
            sleep(0.5)
            paidImageURL = driver.find_element(by=By.XPATH, value="//a[contains(text(),'オリジナルサイズを表示 ')]").get_attribute("href")
            paidImageContainerArray.append(paidImageURL)
            driver.find_element(by=By.XPATH, value="//a[@class='btn btn-dark btn-sm']").click()
            sleep(0.5)
        
        if totalPremiumImages > 0: print("\n")
        premiumImagesProgress = 0
        for imageURL in paidImageContainerArray:
            if premiumImagesProgress == 0:
                if lang == "en":
                    print_progress_bar(premiumImagesProgress, totalPremiumImages, f"Stage 3: Downloading image no.{premiumImagesProgress} out of {totalPremiumImages}")
                elif lang == "jp":
                    print_progress_bar(premiumImagesProgress, totalPremiumImages, f"ステージ 3: 画像 {premiumImagesProgress} / {totalPremiumImages} をダウンロード中")
                premiumImagesProgress += 1

            driver.get(imageURL)
            sleep(1)
            image = driver.find_element(by=By.XPATH, value="/html/body/img")
            imageSrc = image.get_attribute("src")
            imagePath = downloadFolder.joinpath(get_image_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)

            if lang == "en":
                print_progress_bar(premiumImagesProgress, totalPremiumImages, f"{F.LIGHTYELLOW_EX}Stage 3: Downloading image no.{premiumImagesProgress} out of {totalPremiumImages}{END}")
            else:
                print_progress_bar(premiumImagesProgress, totalPremiumImages, f"ステージ3: 画像 {premiumImagesProgress} / {totalPremiumImages} をダウンロード中")

            premiumImagesProgress += 1
            close_new_tab()

        totalImages = totalFullyDisplayedImages + totalImagePosts + totalPremiumImages
        print_download_completion_message(totalImages, subFolderPath)

    elif website == "Pixiv":
        sleep(5)
        # downloads gifs or static images based on a pixiv post
        try: imagesAnchors = driver.find_elements(by=By.XPATH, value="//a[contains(@class, 'iyApTb')]")
        except: imagesAnchors = []

        totalImages = len(imagesAnchors)
        progress = 0
        for anchor in imagesAnchors:
            if progress == 0:
                if lang == "en":
                    print_progress_bar(progress, totalImages, f"Downloading image no.{progress} out of {totalImages}")
                elif lang == "jp":
                    print_progress_bar(progress, totalImages, f"画像 {progress} / {totalImages} をダウンロード中")
                progress += 1

            imageHREF = anchor.get_attribute("href")
            open_new_tab()
            driver.get(imageHREF)
            image = driver.find_element(by=By.XPATH, value="/html/body/img")
            imageSrc = image.get_attribute("src")
            if pixivSession == "":
                driver.execute_script(download_image_javascript(imageSrc, f"post_{subFolderPath}_")) # subFolderPath here will be the latest post num in the driver's default download folder for easier management when downloading images from multiple pixiv Fanbox posts
            else:
                save_image(imageSrc, subFolderPath.joinpath(get_image_name(imageSrc, "Pixiv")), session=pixivSession) # subFolderPath will be a valid path on the user's PC
            
            if lang == "en":
                print_progress_bar(progress, totalImages, f"Downloading image no.{progress} out of {totalImages}")
            else:
                print_progress_bar(progress, totalImages, f"画像 {progress} / {totalImages} をダウンロード中")
          
            progress += 1
            close_new_tab()

        if pixivSession == "": print_download_completion_message(totalImages, pixivDownloadLocation)
        else: print_download_completion_message(totalImages, subFolderPath)
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

                if not imagePath.is_dir(): imagePath.mkdir(parents=True)

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
            f"{F.LIGHTYELLOW_EX}A new browser should have opened.{END}",
            f"{F.LIGHTYELLOW_EX}Please enter your username and password and login to {website.title()} manually.{END}",
        ),
        jp=(
            f"{F.LIGHTYELLOW_EX}新しいブラウザが起動したはずです。{END}", 
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

def save_and_load_cookie(originalDriver, website):
    """
    To save the cookie needed for the login session into the configs folder and encrypts the cookie data.

    Returns True if user is successfully logged in but does not necessarily mean that 
    the cookie is saved into the configs folder as the user can choose to save it or not.

    Requires two arguments to be defined:
    - The current driver (WebDriver)
    - The website the user is downloading images from, either "fantia" or "pixiv" (string)
    """
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
        if newDriver.current_url != websiteURL: newDriver.get(websiteURL)

        if lang == "en": cookiePrompt = f"Would you like to save your {website.title()} session cookie for a faster login next time? (y/n): "
        else: cookiePrompt = f"{website.title()}のセッションクッキーを保存して、次回のログインを早くしたいですか？ (y/n): "
        saveCookieCondition = get_input_from_user(prompt=cookiePrompt, command=("y", "n"))

        configFolder = appPath.joinpath("configs")
        if not configFolder.is_dir(): configFolder.mkdir(parents=True)
        with open(cookiePath, 'wb') as f:
            cookies = newDriver.get_cookies()
            for cookie in cookies:
                if cookie["name"] == cookieName:
                    if saveCookieCondition == "y":
                        dill.dump(encrypt_data(cookie), f)
                        print_in_both_en_jp(
                            en=(f"{F.GREEN}The cookie saved to {cookiePath}\nThe cookie will be automatically loaded in next time in Cultured Downloader for a faster login process!{END}"),
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
                    break

        newDriver.close()
        return True
    else: 
        newDriver.close()
        return False


def print_menu():
    """
    To print out the menu which will reflects any changes based on certain conditions such as whether the user is logged in, etc.
    """
    if not fantiaCookieLoaded: 
        if lang == "en": emailFantia = "Guest (Not logged in)"
        elif lang == "jp": emailFantia = "ゲスト（ログインしていない）"
    else:
        if lang == "en": emailFantia = "Logged in via cookies"
        elif lang == "jp": emailFantia = "クッキーでログイン"
        
    if not pixivCookieLoaded: 
        if lang == "en": usernamePixiv = "Guest (Not logged in)"
        elif lang == "jp": usernamePixiv = "ゲスト（ログインしていない）"
    else:
        if lang == "en": usernamePixiv = "Logged in via cookies"
        elif lang == "jp": usernamePixiv = "クッキーでログイン"

    if lang == "jp": 
        menuHead = f"""{F.LIGHTYELLOW_EX}
> あなたのログイン情報...
> FantiaEメール: {emailFantia}
> Pixiv ID: {usernamePixiv}
{END}
--------------------- {F.LIGHTYELLOW_EX}ダウンロードのオプション{END} ---------------------
      {F.GREEN}1. 画像URLでFantiaから画像をダウンロードする{END}
      {F.GREEN}2. Fantia投稿URLから画像をダウンロードする{END}
      {F.CYAN}3. Pixivファンボックスの投稿URLから画像をダウンロードする{END}

---------------------- {F.LIGHTYELLOW_EX}コンフィグのオプション{END} ----------------------
      {F.LIGHTBLUE_EX}4. デフォルトのダウンロードフォルダを変更する{END}
      {F.LIGHTBLUE_EX}5. ブラウザを変更する{END}
      {F.LIGHTBLUE_EX}6. 言語を変更する{END}
"""
        if emailFantia == "ゲスト（ログインしていない）" or usernamePixiv == "ゲスト（ログインしていない）":
            menuAdditionalOptions = f"""      {F.LIGHTBLUE_EX}7. ログインする{END}\n"""
        else:
            menuAdditionalOptions = ""

        menuFooterStart = f"""
-------------------------- {F.LIGHTYELLOW_EX}他のオプション{END} ---------------------------"""
        if pixivCookieLoaded or fantiaCookieLoaded: menuFooterAdditionalOptions = f"""\n      {F.LIGHTRED_EX}DC. 保存されたクッキーを削除する{END}"""
        else: menuFooterAdditionalOptions = ""

        menuFooterEnd = f"""
        {F.RED}D. Cultured Downloaderで作成されたデータをすべて削除します。{END}
        {F.LIGHTRED_EX}Y. バグを報告する{END}
        {F.RED}X. プログラムを終了する{END}
 """
    else:
        menuHead = f"""{F.LIGHTYELLOW_EX}
> You are currently logged in as...
> Fantia Email: {emailFantia}
> Pixiv ID: {usernamePixiv}
{END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{END} --------------------
      {F.GREEN}1. Download images from Fantia using an image URL{END}
      {F.GREEN}2. Download images from a Fantia post URL{END}
      {F.CYAN}3. Download images from a Pixiv Fanbox post URL{END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{END} ----------------------
      {F.LIGHTBLUE_EX}4. Change Default Download Folder{END}
      {F.LIGHTBLUE_EX}5. Change Default Browser{END}
      {F.LIGHTBLUE_EX}6. Change Language{END}
"""
        if emailFantia == "Guest (Not logged in)" or usernamePixiv == "Guest (Not logged in)":
            menuAdditionalOptions = f"""      {F.LIGHTBLUE_EX}7. Login{END}\n"""
        else:
            menuAdditionalOptions = ""

        menuFooterStart = f"""
---------------------- {F.LIGHTYELLOW_EX}Other Options{END} ----------------------"""
    if pixivCookieLoaded or fantiaCookieLoaded: menuFooterAdditionalOptions = f"""\n      {F.LIGHTRED_EX}DC. Delete saved cookies{END}"""
    else: menuFooterAdditionalOptions = ""

    menuFooterEnd = f"""
      {F.RED}D. Delete all data created by Cultured Downloader{END}
      {F.LIGHTRED_EX}Y. Report a bug{END}
      {F.RED}X. Shutdown the program{END}
 """
        
    print("".join([menuHead, menuAdditionalOptions, menuFooterStart, menuFooterAdditionalOptions, menuFooterEnd]))

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

    # declare global variables
    global appPath
    global jsonPath
    global decKey
    global driver
    global lang
    global fantiaDownloadLocation
    global pixivDownloadLocation
    global pixivCookieLoaded
    global fantiaCookieLoaded
    global pixivSession
    global selectedBrowser
    global ChaChaKey

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
    if not fantiaDownloadLocation.is_dir(): fantiaDownloadLocation.mkdir(parents=True)

    pixivDownloadLocation = directoryPath.joinpath("pixiv_downloads")
    if not pixivDownloadLocation.is_dir(): pixivDownloadLocation.mkdir(parents=True)

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
                if save_and_load_cookie(driver, "pixiv"): 
                    pixivCookieLoaded = True
            if not fantiaCookieLoaded:
                fantiaCookieLoaded = save_and_load_cookie(driver, "fantia")

    if pixivCookieLoaded: pixivSession = get_pixiv_cookie()

    cmdInput = ""
    cmdCommands = ("1", "2", "3", "4", "5", "6", "7", "d", "dc", "x", "y")
    while cmdInput != "x":
        print_menu()
        if lang == "en":
            cmdInput = get_input_from_user(prompt="Enter command: ", command=cmdCommands, warning="Invalid command input, please enter a valid command from the menu above.")
        else:
            cmdInput = get_input_from_user(prompt="コマンドを入力してください： ", command=cmdCommands, warning="不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。")
        if cmdInput == "1":
            imagePath = create_subfolder("fantia")
            startDownloadingFlag = True
            if imagePath != "X":
                if lang == "en": autoDetectPrompt = "Would you like to automatically detect the number of images to download? (y/n/X to cancel): """
                else: autoDetectPrompt = "ダウンロードする画像の枚数を自動的に検出しますか？ (y/n/Xでキャンセル): "
                autoDetectNumOfImages = get_input_from_user(prompt=autoDetectPrompt, command=("y", "n", "x"))

                if autoDetectNumOfImages != "x":
                    print("\n")
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTYELLOW_EX}This option is for URL such as\nhttps://fantia.jp/posts/1234567/post_content_photo/1234567{END}"), 
                        jp=(f"{F.LIGHTYELLOW_EX}このオプションは、\nhttps://fantia.jp/posts/1234567/post_content_photo/1234567 のようなURLのためのものです。{END}")
                    )
                    while True:
                        print_in_both_en_jp(
                            en=(
                                f"{F.LIGHTYELLOW_EX}You can put multiple urls as well by entering a comma in between each urls...{END}",
                                f"{F.LIGHTYELLOW_EX}For example,\n\"https://fantia.jp/posts/1234567/post_content_photo/1234567, https://fantia.jp/posts/1147606/post_content_photo/7194106\"{END}"
                            ), 
                            jp=(
                                f"{F.LIGHTYELLOW_EX}各URLの間にカンマを入力することで、複数のURLを入れることも可能です...{END}"
                                f"{F.LIGHTYELLOW_EX}例えば、\n\"https://fantia.jp/posts/1234567/post_content_photo/1234567, https://fantia.jp/posts/1147606/post_content_photo/7194106\"{END}"
                            )
                        )
                        if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of the first image (X to cancel): "))
                        else: urlInput = split_inputs_to_possible_multiple_inputs(input("最初の画像のURLを入力してください (Xでキャンセル)： "))

                        if urlInput == "x" or urlInput == "X":
                            startDownloadingFlag = False
                            break

                        if (urlInput == "") or (check_if_input_is_url(urlInput) == False): 
                            print_in_both_en_jp(
                                en=(f"{F.RED}Error: No URL entered or URL entered is/are invalid.{END}", f"{F.RED}Please enter a valid URL.{END}"),
                                jp=(f"{F.RED}エラー： URLが入力されていない、または入力されたURLが無効である。{END}", f"{F.RED}URLを入力してください。{END}")
                            )
                        else: break

                    if startDownloadingFlag:
                        allValidNum = True
                        urlArray = []
                        numOfImagesToDownload = []
                        if autoDetectNumOfImages == "y":
                            if type(urlInput) == list:
                                for url in urlInput:
                                    imageCounter = 0
                                    while True:
                                        driver.get(url)
                                        logs = driver.get_log("performance")
                                        if get_status(logs) != 200: break

                                        imageCounter += 1
                                        urlArray.append(url)

                                        # increment the url by one to retrieve the next image
                                        splitURL = url.split("/")
                                        urlNum = str(int(splitURL[-1]) + 1)
                                        urlPartsArray = splitURL[0:-1]
                                        urlPartsArray.append(urlNum)
                                        url = "/".join(urlPartsArray)
                                        del urlPartsArray
                                    numOfImagesToDownload.append(imageCounter)
                            else:
                                while True:
                                    driver.get(urlInput)
                                    logs = driver.get_log("performance")
                                    if get_status(logs) != 200: break

                                    urlArray.append(urlInput)

                                    # increment the urlInput by one to retrieve the next image
                                    splitURL = urlInput.split("/")
                                    urlNum = str(int(splitURL[-1]) + 1)
                                    urlPartsArray = splitURL[0:-1]
                                    urlPartsArray.append(urlNum)
                                    urlInput = "/".join(urlPartsArray)
                                    del urlPartsArray
                                numOfImagesToDownload.append(len(urlArray))
                        else:
                            while True:
                                print_in_both_en_jp(
                                    en=(f"{F.YELLOW}Note: If you have entered multiple urls previously, please enter in this format, \"1, 2, 30, 1\"{END}"),
                                    jp=(f"{F.YELLOW}注意： 以前に複数のURLを入力したことがある場合は、このフォーマットで入力してください。\"1、2、30、1\"{END}")
                                )
                                if lang == "en":
                                    numOfImagesToDownloadInput = split_inputs_to_possible_multiple_inputs(input("Enter the number of images to download (X to cancel): "))
                                else:
                                    numOfImagesToDownloadInput = split_inputs_to_possible_multiple_inputs(input("ダウンロードする画像の枚数を入力してください (Xでキャンセル)： "))
                                if numOfImagesToDownloadInput == "x" or numOfImagesToDownloadInput == "X": 
                                    allValidNum = False
                                    break

                                if type(numOfImagesToDownloadInput) == list:
                                    for number in numOfImagesToDownloadInput:
                                        try: int(number)
                                        except: 
                                            allValidNum = False
                                            break
                                else:
                                    try: 
                                        int(numOfImagesToDownloadInput)
                                        numOfImagesToDownload.append(numOfImagesToDownloadInput)
                                    except: allValidNum = False
                                
                                if allValidNum: 
                                    addToArray = True
                                    if type(urlInput) == list and type(numOfImagesToDownloadInput) == list:
                                        if len(numOfImagesToDownloadInput) != len(urlInput):
                                            print_in_both_en_jp(
                                                en=(f"{F.RED}Error: The number of images to download is not the same as the number of urls entered previously.{END}"),
                                                jp=(f"{F.RED}エラー： ダウンロードする画像の枚数が、以前に入力したURLの枚数と異なります。{END}")
                                            )
                                            addToArray = False
                                    else:
                                        if type(urlInput) == list and type(numOfImagesToDownloadInput) != list: 
                                            print_in_both_en_jp(
                                                en=(f"{F.RED}Error: The number of images to download is not the same as the number of urls entered previously.{END}"),
                                                jp=(f"{F.RED}エラー： ダウンロードする画像の枚数が、以前に入力したURLの枚数と異なります。{END}")
                                            )
                                            addToArray = False
                                        elif type(urlInput) != list and type(numOfImagesToDownloadInput) == list: 
                                            print_in_both_en_jp(
                                                en=(f"{F.RED}Error: The number of images to download is not the same as the number of urls entered previously.{END}"),
                                                jp=(f"{F.RED}エラー： ダウンロードする画像の枚数が、以前に入力したURLの枚数と異なります。{END}")
                                            )
                                            addToArray = False

                                    if addToArray:
                                        if type(urlInput) == list:
                                            arrayPointer = 0
                                            for url in urlInput:
                                                imageCounter = 0
                                                for i in range(int(numOfImagesToDownload[arrayPointer])):
                                                    driver.get(url)
                                        
                                                    imageCounter += 1
                                                    urlArray.append(url)

                                                    # increment the url by one to retrieve the next image
                                                    splitURL = url.split("/")
                                                    urlNum = str(int(splitURL[-1]) + 1)
                                                    urlPartsArray = splitURL[0:-1]
                                                    urlPartsArray.append(urlNum)
                                                    url = "/".join(urlPartsArray)
                                                    del urlPartsArray
                                                        
                                                arrayPointer += 1
                                        else:
                                            for i in range(int(numOfImagesToDownload[0])):
                                                driver.get(urlInput)
                            
                                                urlArray.append(urlInput)

                                                # increment the urlInput by one to retrieve the next image
                                                splitURL = urlInput.split("/")
                                                urlNum = str(int(splitURL[-1]) + 1)
                                                urlPartsArray = splitURL[0:-1]
                                                urlPartsArray.append(urlNum)
                                                urlInput = "/".join(urlPartsArray)
                                                del urlPartsArray

                                            numOfImagesToDownload.append(len(urlArray))

                                        break
                                else:
                                    print_in_both_en_jp(
                                        en=(f"{F.RED}Error: The number of images to download is not valid.{END}"),
                                        jp=(f"{F.RED}エラー： ダウンロードする画像の枚数が無効です。{END}")
                                    )

                        if allValidNum:
                            totalImages = len(urlArray)
                            print("\n")
                            print_in_both_en_jp(
                                en=(
                                    f"{F.YELLOW}Please wait as auto downloading images from Fantia can take quite a while if the image size is large...{END}",
                                    f"{F.YELLOW}The program will automatically download {totalImages} images.{END}"
                                ),
                                jp=(
                                    f"{F.YELLOW}Fantiaからの画像の自動ダウンロードは、画像サイズが大きい場合、かなり時間がかかるので、お待ちください...{END}"
                                    f"{F.YELLOW}プログラムが自動的に{totalImages}枚の画像をダウンロードします。{END}"
                                )
                            )
                            if totalImages != 0:
                                imageCounter = 0
                                arrayPointer = 0
                                progress = 0
                                
                                imageFolderPath = imagePath.joinpath(str(arrayPointer))
                                for url in urlArray:
                                    if progress == 0:
                                        if lang == "en":
                                            print_progress_bar(progress, totalImages, f"{F.LIGHTYELLOW_EX}Downloading image no.{progress} out of {totalImages}{END}")
                                        else:
                                            print_progress_bar(progress, totalImages, f"画像 {progress} / {totalImages} をダウンロード中")
                                        progress += 1

                                    imageFolderPath.mkdir(parents=True, exist_ok=True)
                                    imageCounter += 1

                                    download(url, "FantiaImageURL", imageFolderPath)

                                    if imageCounter == int(numOfImagesToDownload[arrayPointer]):
                                        arrayPointer += 1
                                        imageFolderPath = imagePath.joinpath(str(arrayPointer))
                                        imageCounter = 0

                                    if lang == "en":
                                        print_progress_bar(progress, totalImages, f"{F.LIGHTYELLOW_EX}Downloading image no.{progress} out of {totalImages}{END}")
                                    else:
                                        print_progress_bar(progress, totalImages, f"画像 {progress} / {totalImages} をダウンロード中")
                                    
                                    progress += 1

                            print_download_completion_message(totalImages, imagePath)
                            print("\n")
                            print_in_both_en_jp(
                                en=(
                                    f"\n{F.LIGHTRED_EX}However, please do not close/shutdown the program as the program might still be downloading the images!{END}",
                                    f"\n{F.LIGHTRED_EX}After checking that all the images has been successfully downloaded, you can then choose to shutdown/close the program.{END}"
                                ),
                                jp=(
                                    f"{F.LIGHTRED_EX}ただし、プログラムがまだ画像をダウンロードしている可能性がありますので、プログラムを終了/シャットダウンしないでください。{END}",
                                    f"{F.LIGHTRED_EX}その後、すべての画像が正常にダウンロードされたことを確認してから、プログラムを終了/シャットダウンができます。{END}"
                                    )
                            )

        elif cmdInput == "2":
            imagePath = create_subfolder("fantia")
            startDownloadingFlag = True
            if imagePath != "X":
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
                            f"{F.LIGHTYELLOW_EX}各URLの間にカンマを入力することで、複数のURLを入れることも可能です...{END}"
                            f"{F.LIGHTYELLOW_EX}例えば、\n\"https://fantia.jp/posts/1147606, https://fantia.jp/posts/1086639\"{END}"
                        )
                    )
                    if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of the Fantia post (X to cancel): "))
                    else: urlInput = split_inputs_to_possible_multiple_inputs(input("Fantiaの投稿のURLを入力します (Xでキャンセル)： "))

                    if urlInput == "x" or urlInput == "X": 
                        startDownloadingFlag = False
                        break

                    if (urlInput == "") or (check_if_input_is_url(urlInput) == False):
                        print_in_both_en_jp(
                            en=(f"{F.RED}Error: No URL entered.{END}", f"{F.RED}Please enter a valid URL.{END}"),
                            jp=(f"{F.RED}エラー： URLが入力されていません。{END}", f"{F.RED}URLを入力してください。{END}")
                        )
                    else: break

                if startDownloadingFlag:
                    if type(urlInput) == list: numOfPosts = len(urlInput)
                    else: numOfPosts = 1
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.YELLOW}Please wait as auto downloading images from Fantia can take quite a while if the image size is large...{END}",
                            f"{F.YELLOW}The program will automatically download images from {numOfPosts} posts.{END}"
                        ),
                        jp=(
                            f"{F.YELLOW}Fantiaからの画像の自動ダウンロードは、画像サイズが大きい場合、かなり時間がかかるので、お待ちください...{END}"
                            f"{F.YELLOW}このプログラムは、{numOfPosts}投稿の中から画像を自動的にダウンロードします。{END}"
                        )
                    )
                    
                    if type(urlInput) == list:
                        counter = 0
                        for url in urlInput: 
                            downloadDirectoryFolder = imagePath.joinpath(f"Post_{counter}")
                            downloadDirectoryFolder.mkdir(parents=True, exist_ok=True)
                            download(url, "FantiaPost", downloadDirectoryFolder)
                            counter += 1
                    else: download(urlInput, "FantiaPost", imagePath)
                
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"\n{F.LIGHTRED_EX}However, please do not close/shutdown the program as the program might still be downloading the images!{END}",
                            f"\n{F.LIGHTRED_EX}After checking that all the images has been successfully downloaded, you can then choose to shutdown/close the program.{END}"
                        ),
                        jp=(
                            f"{F.LIGHTRED_EX}ただし、プログラムがまだ画像をダウンロードしている可能性がありますので、プログラムを終了/シャットダウンしないでください。{END}",
                            f"{F.LIGHTRED_EX}その後、すべての画像が正常にダウンロードされたことを確認してから、プログラムを終了/シャットダウンができます。{END}"
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
                            f"{F.LIGHTYELLOW_EX}各URLの間にカンマを入力することで、複数のURLを入れることも可能です...{END}"
                            f"{F.LIGHTYELLOW_EX}例えば、\n\"https://www.fanbox.cc/@gmkj0324/posts/3103384, https://www.fanbox.cc/@gmkj0324/posts/3072263\"{END}"
                        )
                    )
                    if lang == "en": urlInput = split_inputs_to_possible_multiple_inputs(input("Enter the URL of the Pixiv Fanbox post (X to cancel): "))
                    else: urlInput = split_inputs_to_possible_multiple_inputs(input("Pixivファンボックスの投稿URLを入力してください (Xでキャンセル)： "))

                    if urlInput == "x" or urlInput == "X":
                        startDownloadingFlag = False
                        break

                    if (urlInput == "") or (check_if_input_is_url(urlInput) == False): 
                        print_in_both_en_jp(
                            en=(f"{F.RED}Error: No URL entered.{END}", f"{F.RED}Please enter a valid URL.{END}"),
                            jp=(f"{F.RED}エラー： URLが入力されていません。{END}", f"{F.RED}URLを入力してください。{END}")
                        )
                    else: break

                if startDownloadingFlag:
                    if type(urlInput) == list: numOfPosts = len(urlInput)
                    else: numOfPosts = 1
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"{F.YELLOW}Please wait as auto downloading images from pixiv can take quite a while if the image size is large...{END}",
                            f"{F.YELLOW}The program will automatically download images from {numOfPosts} posts.{END}"
                        ),
                        jp=(
                            f"{F.YELLOW}pixivからの画像の自動ダウンロードは、画像サイズが大きい場合、かなり時間がかかるので、お待ちください...{END}"
                            f"{F.YELLOW}このプログラムは、{numOfPosts}投稿の中から画像を自動的にダウンロードします。{END}"
                        )
                    )

                    if imagePath == "":
                        postNum = get_latest_post_num_from_file_name()
                        if type(urlInput) == list:
                            counter = 1
                            for url in urlInput:
                                print_in_both_en_jp(
                                    en=(f"{F.YELLOW}\nDownloading images from post {counter}...{END}"),
                                    jp=(f"{F.YELLOW}\n投稿番号{counter}の画像をダウンロードしています...{END}")
                                )
                                download(url, "Pixiv", postNum)
                                postNum += 1
                                counter += 1
                        else:
                            download(urlInput, "Pixiv", postNum)
                    else:
                        if type(urlInput) == list:
                            counter = 1
                            for url in urlInput:
                                downloadDirectoryFolder = imagePath.joinpath(f"Post_{counter}")
                                downloadDirectoryFolder.mkdir(parents=True, exist_ok=True)
                                download(url, "Pixiv", downloadDirectoryFolder)
                                counter += 1
                        else:
                            download(urlInput, "Pixiv", imagePath)
                    
                    print("\n")
                    print_in_both_en_jp(
                        en=(
                            f"\n{F.LIGHTRED_EX}However, please do not close/shutdown the program as the program might still be downloading the images!{END}",
                            f"\n{F.LIGHTRED_EX}After checking that all the images has been successfully downloaded, you can then choose to shutdown/close the program.{END}"
                        ),
                        jp=(
                            f"{F.LIGHTRED_EX}ただし、プログラムがまだ画像をダウンロードしている可能性がありますので、プログラムを終了/シャットダウンしないでください。{END}",
                            f"{F.LIGHTRED_EX}その後、すべての画像が正常にダウンロードされたことを確認してから、プログラムを終了/シャットダウンができます。{END}"
                            )
                    )

        elif cmdInput == "4":
            get_default_download_directory()
            with open(jsonPath, "r") as f:
                config = json.load(f)

            set_default_download_directory(config)
            
        elif cmdInput == "5":
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

        elif cmdInput == "6":
            lang = update_lang()

        elif cmdInput == "7":
            if not check_if_user_is_logged_in():
                if not pixivCookieLoaded:
                    if save_and_load_cookie(driver, "pixiv"): 
                        pixivCookieLoaded = True
                if not fantiaCookieLoaded:
                    fantiaCookieLoaded = save_and_load_cookie(driver, "fantia")
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )

        elif cmdInput == "d":
            print_in_both_en_jp(
                en=(f"{F.LIGHTYELLOW_EX}Deleting folders in {appPath}...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}{appPath} 内のフォルダーを削除します...{END}")
            )
            if check_if_directory_has_files(appPath):
                for folderPath in appPath.iterdir():
                    if folderPath.is_dir():
                        rmtree(folderPath)
                print_in_both_en_jp(
                    en=(f"{F.LIGHTYELLOW_EX}Deleted folders in {appPath}{END}"),
                    jp=(f"{F.LIGHTYELLOW_EX}{appPath} 内のフォルダーを削除しました。{END}")
                )
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Error: Nothing to delete in {appPath}{END}"),
                    jp=(f"{F.RED}エラー： {appPath} に削除するものはありません。{END}")
                )
                
        elif cmdInput == "dc":
            if pixivCookieLoaded or fantiaCookieLoaded:
                if pixivCookieLoaded:
                    pixivCookiePath = appPath.joinpath("configs", "pixiv_cookies")
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTYELLOW_EX}Deleting Pixiv Fanbox cookies...{END}"),
                        jp=(f"{F.LIGHTYELLOW_EX}Pixivファンボックスのクッキーを削除します...{END}")
                    )
                    if pixivCookiePath.exists():
                        if pixivCookiePath.is_file():
                            pixivCookiePath.unlink()
                            print_in_both_en_jp(
                                en=(f"{F.LIGHTYELLOW_EX}Deleted Pixiv Fanbox cookies{END}"),
                                jp=(f"{F.LIGHTYELLOW_EX}Pixivファンボックスのクッキーが削除されました。{END}")
                            )
                        else: raise Exception("Pixiv cookie is a directory and not a file...")
                    else:
                        print_in_both_en_jp(
                            en=(f"{F.RED}Error: Pixiv Fanbox cookie not found.{END}"),
                            jp=(f"{F.RED}エラー： pixivファンボックスのクッキーが見つかりません。{END}")
                        )
                if fantiaCookieLoaded:
                    fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
                    print_in_both_en_jp(
                        en=(f"{F.LIGHTYELLOW_EX}Deleting Fantia cookies...{END}"),
                        jp=(f"{F.LIGHTYELLOW_EX}Fantiaのクッキーを削除します...{END}")
                    )
                    if fantiaCookiePath.exists():
                        if fantiaCookiePath.is_file():
                            fantiaCookiePath.unlink()
                            print_in_both_en_jp(
                                en=(f"{F.LIGHTYELLOW_EX}Deleted Fantia cookies{END}"),
                                jp=(f"{F.LIGHTYELLOW_EX}Fantiaのクッキーが削除されました。{END}")
                            )
                        else: raise Exception("Fantia cookie is a directory and not a file...")
                    else:
                        print_in_both_en_jp(
                            en=(f"{F.RED}Error: Fantia cookie not found.{END}"),
                            jp=(f"{F.RED}エラー： Fantiaのクッキーが見つかりません。{END}")
                        )
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Invalid command input, please enter a valid command from the menu above.{END}"),
                    jp=(f"{F.RED}不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。{END}")
                )

        elif cmdInput == "y": webbrowser.open("https://github.com/KJHJason/Cultured-Downloader/issues", new=2)
        elif cmdInput == "x": driver.close()

"""--------------------------- End of Main Codes ---------------------------"""

if __name__ == "__main__":
    coloramaInit(autoreset=False, convert=True)
    global END
    END = Style.RESET_ALL

    introMenu = f"""
====================== {F.LIGHTBLUE_EX}CULTURED DOWNLOADER v{__version__ }{END} ======================
=========== {F.LIGHTBLUE_EX}https://github.com/KJHJason/Cultured-Downloader{END} ===========
================ {F.LIGHTBLUE_EX}Author/開発者: {__author__}, aka Dratornic{END} ================
{F.LIGHTYELLOW_EX}
Purpose/目的: Allows you to download multiple images from Fantia or Pixiv Fanbox automatically.
              FantiaやPixivファンボックスから複数の画像を自動でダウンロードできるようにします。

Note/注意: Requires the user to login via this program for images that requires a membership.
           This program is not affiliated with Pixiv or Fantia.
           会員登録が必要な画像は、本プログラムによるログインが必要です。
           このプログラムはPixivやFantiaとは関係ありません。{END}

{F.RED}Terms of Use/利用規約: 
1. This program, Cultured Downloader, is not liable for any damages caused. 
   This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually.
   本プログラム「Cultured Downloader」は、発生した損害について一切の責任を負いかねます。
   このプログラムは、個人的な使用と、pixiv FanboxとFantiaから画像を手動でダウンロードする時間を節約するためのものです。

2. As a user of this program, please do not use this program to 
   break any of Fantia's or pixiv Fanbox's Terms of Service/Terms of Use.
   本プログラムの利用者として、Fantiaおよびpixivファンボックスの利用規約を破るような利用はしないでください。

3. As a user of this program, you must never share any data such as your fantia_cookies file to other people.
   This is not permissible as it will cause damages to the artists that you are downloading from.
   If you have been found to be sharing YOUR data or using OTHER people's data, 
   this program and the developer(s) will not be liable for the damages caused but the user(s) involved will be.
   本プログラムのユーザーとして、fantia_cookiesファイルなどのデータは絶対に他人と共有しないでください。
   クッキーを共有することは、ダウンロード先のアーティストに損害を与えることになりますので、おやめください。
   自分のデータを共有したり、他人のデータを使用していることが判明した場合。
   このプログラムおよび開発者は損害賠償の責任を負いませんが、関係するユーザーは責任を負うものとします。

   (In an event of mistranslation, the English version will take priority and will be used/
   誤訳があった場合は、英語版を優先して使用します。)
{END}{F.LIGHTRED_EX}
Known Issues/既知のバグについて: 
1. Sometimes the program does not shutdown automatically. 
   In this case, please close the program manually or press CTRL + C to terminate the program.
   プログラムが自動的にシャットダウンしないことがあります。
   この場合、手動でプログラムを終了させるか、CTRL + Cキーを押してプログラムを終了させてください{END}
"""
    print(introMenu)
    try:
        main()
    except SystemExit:
        sys.exit()
    except KeyboardInterrupt:
        print(f"\n{F.RED}Program Terminated/プログラムが終了しました{END}")
        sleep(1)
        sys.exit()
    except (EncryptionKeyError, DecryptError):
        driver.quit()
        delete_encrypted_data()
        sys.exit(1)
    except:
        print_error_log_notification()
        log_error()
        sys.exit()

    shutdown()