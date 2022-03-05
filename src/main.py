version = "0.01"

# Import Third-party Libraries
import requests, dill
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.chrome.options import Options as chromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.firefox.options import Options as firefoxOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.edge.options import Options as edgeOptions

# Import Standard Libraries
import pathlib, json, sys, shutil
from time import sleep
from warnings import filterwarnings, catch_warnings

# Importing Custom Python Files as Modules
from Colour_Settings import TerminalColours as S
from Key import Key

"""--------------------------- Config Codes ---------------------------"""

def shutdown():
    if lang == "en":
        print(f"{S.YELLOW}Thank you for using Cultured Downloader.{END}")
        input("Please enter any key to exit...")
    else:
        print(f"{S.YELLOW}Cultured Downloaderをご利用いただきありがとうございます。{END}")
        input("何か入力すると終了します。。。")
    sys.exit(0)

def error_shutdown(**errorMessages):
    if "en" in errorMessages and lang == "en":
        enErrorMessages = errorMessages.get("en")
        if type(enErrorMessages) == tuple:
            for line in enErrorMessages:
                print(f"{S.RED}{line}{END}")
        else: print(f"{S.RED}{enErrorMessages}{END}")
        input("Please enter any key to exit...")
        print("Thank you for your understanding.")
        sleep(2)
        sys.exit(1)
    elif "jp" in errorMessages and lang == "jp":
        jpErrorMessages = errorMessages.get("jp")
        if type(jpErrorMessages) == tuple:
            for line in jpErrorMessages:
                print(f"{S.RED}{line}{END}")
        else: print(f"{S.RED}{jpErrorMessages}{END}")
        input("何か入力すると終了します。。。")
        print("ご理解頂き誠にありがとうございます。")
        sleep(2)
        sys.exit(1)

def print_in_both_en_jp(**message):
    enMessages = message.get("en")
    jpMessages = message.get("jp")

    if lang == "en":
        if type(enMessages) == tuple:
            for enLine in enMessages:
                print(enLine)
        else: print(enMessages)
    else:
        if type(jpMessages) == tuple:
            for jpLine in jpMessages:
                print(jpLine)
        else: print(jpMessages)

def get_input_from_user(**kwargs):
    prints = kwargs.get("prints")
    prompt = kwargs.get("prompt")
    commands = kwargs.get("command")
    warning = kwargs.get("warning")

    if prints != None:
        if type(prints) == tuple:
            for line in prints:
                print(f"{S.YELLOW}{line}{END}")
        else: print(f"{S.YELLOW}{prints}{END}")

    while True:
        userInput = input(prompt).lower().strip()
        if userInput in commands: return userInput
        else: 
            try:
                if warning and lang == "en": print(f"{S.RED}Error: {warning}.{END}")
                elif warning and lang == "jp": print(f"{S.RED}エラー: {warning}{END}")
                else: 
                    if lang == "en": commandToPrint = " or ".join(commands)
                    else: commandToPrint = "または".join(commands)
                    print_in_both_en_jp(
                        en=(f"{S.RED}Error: Invalid input. Please enter {commandToPrint}.{END}"),
                        jp=(f"{S.RED}エラー: 不正な入力です。{commandToPrint}を入力してください。{END}")
                    )
            except NameError:
                # if lang is not defined yet
                commandToPrintEn = " or ".join(commands)
                commandToPrintJp = "または".join(commands)
                if warning: 
                    print(f"{S.RED}Error: Invalid language prefix entered.{END}")
                    print(f"{S.RED}エラー: 入力された言語プレフィックスが無効です。{END}")
                else: 
                    print(f"{S.RED}Error: Invalid input. Please enter {commandToPrintEn}.{END}"),
                    print(f"{S.RED}エラー: 不正な入力です。{commandToPrintJp}を入力してください。{END}")

def check_if_json_file_exists():
    jsonFolderPath = pathlib.Path(__file__).resolve().parent.joinpath("configs")
    if not jsonFolderPath.is_dir(): jsonFolderPath.mkdir(parents=True)
    if not jsonPath.is_file():
        print(f"{S.RED}Error: config.json does not exist.{END}", f"{S.YELLOW}Creating config.json file...{END}"),
        print(f"{S.RED}エラー: config.jsonが存在しません。{END}", f"{S.YELLOW}config.jsonファイルを作成しています...{END}")
        
        with open(jsonPath, "w") as f:
            json.dump({}, f)
    else: 
        print(f"{S.GREEN}Loading configurations from config.json...{END}")
        print(f"{S.GREEN}config.jsonから設定を読み込みます...{END}")


def encrypt_string(inputString):
    return decKey.encrypt(inputString.encode()).decode()

def decrypt_string(inputString):
    try:
        return decKey.decrypt(inputString.encode()).decode()
    except:
        print_in_both_en_jp(
            en=(f"{S.RED}Fatal Error: Could not decrypt string.{END}", f"{S.RED}Resetting Key and encrypted values in config.json...{END}"),
            jp=(f"{S.RED}致命的なエラー: 文字列を復号化できませんでした。{END}", f"{S.RED}config.jsonのキーと暗号化された値をリセットしています...{END}")
        )
        keyPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "key.pik")
        if keyPath.is_file():
            keyPath.unlink()
            
        error_shutdown(en=("Please restart the program."), jp=("このプログラムを再起動してください。"))

def get_user_account():
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        fantiaEmail = config["Accounts"]["Fantia"]["User"]
        fantiaPassword = config["Accounts"]["Fantia"]["Password"]
        pixivUsername = config["Accounts"]["Pixiv"]["User"]
        pixivPassword = config["Accounts"]["Pixiv"]["Password"]
        if fantiaEmail == "" or fantiaPassword == "" or pixivUsername == "" or pixivPassword == "":
            raise Exception("Account details had empty values.")
        return fantiaEmail, decrypt_string(fantiaPassword), pixivUsername, decrypt_string(pixivPassword)
    except:
        print_in_both_en_jp(
            en=(f"{S.RED}Error: config.json does not have all the necessary account details.{END}"),
            jp=(f"{S.RED}エラー: config.jsonに必要なアカウントの詳細がありません。{END}")
        )

        if "Accounts" not in config:
            data = {"Accounts": {
                        "Fantia": {
                            "User": "",
                            "Password": ""
                            },
                        "Pixiv": {
                            "User": "",
                            "Password": ""
                            }
                        }
                    }
            configInput = get_input_from_user(prompt="Would you like to save your account details now? (y/n): ", command=("y", "n"))
        
            if configInput == "n": 
                print_in_both_en_jp(
                    en=(f"{S.RED}Warning: Since you have not added your account details yet,\nyou will not be able to download any images that requires a membership.\nFret not, you can add your account details later.{END}"),
                    jp=(f"{S.RED}ご注意： まだアカウント情報を追加していないため、\n会員登録が必要な画像をダウンロードすることはできません。\n後でアカウント情報を追加することができますので、ご安心ください。{END}")
                )

                config.update(data)
                with open(jsonPath, "w") as f:
                    json.dump(config, f, indent=4)
                return None, None, None, None
            else:
                print_in_both_en_jp(
                    en=(f"\n{S.YELLOW}Adding account details for Fantia...{END}"),
                    jp=(f"\n{S.YELLOW}Fantiaのアカウント情報を追加しています...{END}")
                )

                while True:
                    if lang == "en": fantiaEmail = input("Enter your email address for Fantia: ").lower().strip()
                    else: fantiaEmail = input("FantiaアカウントのEメールを入力してください： ").lower().strip()
                    if fantiaEmail != "":
                        data["Accounts"]["Fantia"]["User"] = fantiaEmail
                        break
                
                while True:
                    if lang == "en": fantiaPassword = input("Enter your password for Fantia: ")
                    else: fantiaPassword = input("Fantiaアカウントのパスワードを入力してください： ")
                    if fantiaPassword != "":
                        data["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)
                        break

                print_in_both_en_jp(
                    en=(f"{S.GREEN}Fantia Account successfully added!{END}"),
                    jp=(f"{S.GREEN}Fantiaのアカウント情報を追加しました！{END}")
                )

                print_in_both_en_jp(
                    en=(f"\n{S.YELLOW}Adding account details for Pixiv...{END}"),
                    jp=(f"\n{S.YELLOW}Pixivアカウント情報を追加しています...{END}")
                )

                while True:
                    if lang == "en": pixivUsername = input("Enter your Pixiv ID: ").strip()
                    else: pixivUsername = input("PixivアカウントのIDを入力してください： ").strip()
                    if pixivUsername != "":
                        data["Accounts"]["Pixiv"]["User"] = pixivUsername
                        break
                
                while True:
                    if lang == "en": pixivPassword = input("Enter your password for Pixiv: ")
                    else: pixivPassword = input("Pixivアカウントのパスワードを入力してください： ")
                    if fantiaPassword != "":
                        data["Accounts"]["Pixiv"]["Password"] = encrypt_string(pixivPassword)
                        break

                with open(jsonPath, "w") as f:
                    config.update(data)
                    json.dump(config, f, indent=4)

                print_in_both_en_jp(
                    en=(f"{S.GREEN}Pixiv Account successfully added!{END}"),
                    jp=(f"{S.GREEN}Pixivのアカウント情報を追加しました！{END}")
                )
                
                return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword
        else: 
            fantiaData = config["Accounts"]["Fantia"]
            pixivData = config["Accounts"]["Pixiv"]

            if fantiaData["User"] == "":
                print_in_both_en_jp(
                    en=(f"\n{S.YELLOW}Adding account details for Fantia...{END}"),
                    jp=(f"\n{S.YELLOW}Fantiaのアカウント情報を追加しています...{END}")
                )

                while True:
                    if lang == "en": fantiaEmail = input("Enter your email address for Fantia: ").lower().strip()
                    else: fantiaEmail = input("FantiaアカウントのEメールを入力してください： ").lower().strip()
                    if fantiaEmail != "":
                        fantiaData["Username"] = fantiaEmail
                        break

                print_in_both_en_jp(
                    en=(f"{S.GREEN}Email for Fantia Account successfully added!{END}"),
                    jp=(f"{S.GREEN}FantiaアカウントのEメール追加に成功しました！{END}")
                )
            if fantiaData["Password"] == "":
                print_in_both_en_jp(
                    en=(f"\n{S.YELLOW}Adding account details for Fantia...{END}"),
                    jp=(f"\n{S.YELLOW}Fantiaのアカウント情報を追加しています...{END}")
                )

                while True:
                    if lang == "en": fantiaPassword = input("Enter your password for Fantia: ")
                    else: fantiaPassword = input("Fantiaアカウントのパスワードを入力してください： ")
                    if fantiaPassword != "":
                        fantiaData["Password"] = encrypt_string(fantiaPassword)
                        break

                print_in_both_en_jp(
                    en=(f"{S.GREEN}Password for Fantia Account successfully added!{END}"),
                    jp=(f"{S.GREEN}Fantiaアカウントのパスワード追加に成功しました！{END}")
                )
            if pixivData["User"] == "":
                print_in_both_en_jp(
                    en=(f"\n{S.YELLOW}Adding account details for Pixiv...{END}"),
                    jp=(f"\n{S.YELLOW}Pixivアカウント情報を追加しています...{END}")
                )

                while True:
                    if lang == "en": pixivUsername = input("Enter your Pixiv ID: ").strip()
                    else: pixivUsername = input("PixivアカウントのIDを入力してください： ").strip()
                    if pixivUsername != "":
                        pixivData["Username"] = pixivUsername
                        break

                print_in_both_en_jp(
                    en=(f"{S.GREEN}Pixiv ID successfully added!{END}"),
                    jp=(f"{S.GREEN}PixivアカウントのID追加に成功しました！{END}")
                )
            if pixivData["Password"] == "":
                print_in_both_en_jp(
                    en=(f"\n{S.YELLOW}Adding account details for Pixiv fanbox...{END}"),
                    jp=(f"\n{S.YELLOW}Pixivアカウント情報を追加しています...{END}")
                )

                while True:
                    if lang == "en": pixivPassword = input("Enter your password for Pixiv: ")
                    else: pixivPassword = input("Pixivアカウントのパスワードを入力してください： ")
                    if pixivPassword != "":
                        pixivData["Password"] = encrypt_string(pixivPassword)
                        break

                print_in_both_en_jp(
                    en=(f"{S.GREEN}Password for Pixiv Account successfully added!{END}"),
                    jp=(f"{S.GREEN}Pixivアカウントのパスワード追加に成功しました！{END}")
                )
            
            with open(jsonPath, "w") as f:
                json.dump(config, f, indent=4)

            return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword

def change_account_details(typeToChange, **credToUpdate):
    credentialsToChangeList = credToUpdate.get("cred")
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        if typeToChange == "fantia":
            print_in_both_en_jp(
                en=(f"\n{S.YELLOW}Changing account details for Fantia...{END}"),
                jp=(f"\n{S.YELLOW}Fantiaアカウント情報を変更する...{END}")
            )

            if "username" in credentialsToChangeList:
                while True:
                    if lang == "en": fantiaEmail = input("Enter your new email address for Fantia (X to cancel): ").lower().strip()
                    else: fantiaEmail = input("新しいFantiaアカウントのEメールを入力してください（\"X\"でキャンセル）： ").lower().strip()
                    if fantiaEmail.upper() != "X" and fantiaEmail != "": 
                        config["Accounts"]["Fantia"]["User"] = fantiaEmail
                        break
                    elif fantiaEmail.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break

            if "password" in credentialsToChangeList:
                while True:
                    if lang == "en": fantiaPassword = input("Enter your password for Fantia (X to cancel): ")
                    else: fantiaPassword = input("新しいFantiaアカウントのパスワードを入力してください（\"X\"でキャンセル）： ")
                    if fantiaPassword.upper() != "X" and fantiaPassword != "": 
                        config["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)
                        break
                    elif fantiaPassword.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break

        elif typeToChange == "pixiv":
            print_in_both_en_jp(
                en=(f"\n{S.YELLOW}Changing Pixiv Account Details...{END}"),
                jp=(f"\n{S.YELLOW}Pixivアカウント情報を変更する...{END}")
            )

            if "username" in credentialsToChangeList:
                while True:
                    if lang == "en": pixivUsername = input("Enter your Pixiv ID (X to cancel): ").strip()
                    else: pixivUsername = input("新しいPixivアカウントのIDを入力してください（\"X\"でキャンセル）： ").strip()
                    if pixivUsername.upper() != "X" and pixivUsername != "": 
                        config["Accounts"]["Pixiv"]["User"] = pixivUsername
                        break
                    elif pixivUsername.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break

            if "password" in credentialsToChangeList:
                while True:
                    if lang == "en": pixivPassword = input("Enter your password for Pixiv: ")
                    else: pixivPassword = input("新しいPixivアカウントのパスワードを入力してください（\"X\"でキャンセル）： ")
                    if pixivPassword.upper() != "X" and pixivPassword != "": 
                        config["Accounts"]["Pixiv"]["Password"] = encrypt_string(pixivPassword)
                        break
                    elif pixivPassword.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break
                
        elif typeToChange == "all":
            print_in_both_en_jp(
                en=(f"\n{S.YELLOW}Changing account details for Fantia...{END}"),
                jp=(f"\n{S.YELLOW}Fantiaアカウント情報を変更する...{END}")
            )

            if "username" in credentialsToChangeList:
                while True:
                    if lang == "en": fantiaEmail = input("Enter your new email address for Fantia (X to cancel): ").lower().strip()
                    else: fantiaEmail = input("新しいFantiaアカウントのEメールを入力してください（\"X\"でキャンセル）： ").lower().strip()
                    if fantiaEmail.upper() != "X" and fantiaEmail != "": 
                        config["Accounts"]["Fantia"]["User"] = fantiaEmail
                        break
                    elif fantiaEmail.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break
            
            if "password" in credentialsToChangeList:
                while True:
                    if lang == "en": fantiaPassword = input("Enter your password for Fantia (X to cancel): ")
                    else: fantiaPassword = input("新しいFantiaアカウントのパスワードを入力してください（\"X\"でキャンセル）： ")
                    if fantiaPassword.upper() != "X" and fantiaPassword != "": 
                        config["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)
                        break
                    elif fantiaPassword.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break

            print_in_both_en_jp(
                en=(f"\n{S.YELLOW}Changing Pixiv Account Details...{END}"),
                jp=(f"\n{S.YELLOW}Pixivアカウント情報を変更する...{END}")
            )

            if "username" in credentialsToChangeList:
                while True:
                    if lang == "en": pixivUsername = input("Enter your Pixiv ID (X to cancel): ").strip()
                    else: pixivUsername = input("新しいPixivアカウントのIDを入力してください（\"X\"でキャンセル）： ").strip()
                    if pixivUsername.upper() != "X" and pixivUsername != "": 
                        config["Accounts"]["Pixiv"]["User"] = pixivUsername
                        break
                    elif pixivUsername.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break

            if "password" in credentialsToChangeList:
                while True:
                    if lang == "en": pixivPassword = input("Enter your password for Pixiv: ")
                    else: pixivPassword = input("新しいPixivアカウントのパスワードを入力してください（\"X\"でキャンセル）： ")
                    if pixivPassword.upper() != "X" and pixivPassword != "": 
                        config["Accounts"]["Pixiv"]["Password"] = encrypt_string(pixivPassword)
                        break
                    elif pixivPassword.upper() == "X":
                        print_in_both_en_jp(
                            en=(f"{S.GREEN}No changes made!{END}"),
                            jp=(f"{S.GREEN}変更は行われませんでした！{END}")
                        )
                        break
        else:
            error_shutdown(
                en=("Unexpected Error: Error when trying to change account details.", 
                    "Please report this error to the developer."),
                jap=("予期せぬエラー： アカウントの詳細を変更しようとしたときにエラーが発生しました。", "このエラーを開発者に報告してください。")
            )

        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)

    except KeyError:
        error_shutdown(
            en=("Error: Encountered a KeyError when trying to change account details.", "Please report this error to the developer."),
            jap=("エラー： アカウントの詳細を変更しようとすると、KeyErrorが発生しました。", "このエラーを開発者に報告してください。")
        )
    except:
        error_shutdown(
            en=("Unexpected Error: Error when trying to change account details.", "Please report this error to the developer."),
            jap=("予期せぬエラー： アカウントの詳細を変更しようとすると、エラーが発生します。", "このエラーを開発者に報告してください。")
        )

def get_driver(browserType):
    if browserType == "chrome":
        #minimise the browser window and hides unnecessary text output
        cOptions = chromeOptions()
        cOptions.headless = True
        cOptions.add_argument("--log-level=3")
        cOptions.add_argument("--disable-gpu")
        cOptions.add_argument('--disable-dev-shm-usage') # from https://stackoverflow.com/questions/62898801/selenium-headless-chrome-runs-much-slower

        # for checking response code
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        # auto downloads chromedriver.exe
        gService = chromeService(ChromeDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Chrome(service=gService, options=cOptions, desired_capabilities=capabilities)
    elif browserType == "firefox":
        #minimise the browser window and hides unnecessary text output
        fOptions = firefoxOptions()
        fOptions.headless = True
        fOptions.add_argument("--log-level=3")
        fOptions.add_argument("--disable-gpu")

        # for checking response code
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities["moz:loggingPrefs"] = {"performance": "ALL"}

        # auto downloads geckodriver.exe
        fService = firefoxService(GeckoDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        with catch_warnings():
            filterwarnings("ignore", category=DeprecationWarning)
            driver = webdriver.Firefox(service=fService, options=fOptions, capabilities=capabilities)
    elif browserType == "edge":
        # minimise the browser window and hides unnecessary text output
        eOptions = edgeOptions()
        eOptions.headless = True
        eOptions.use_chromium = True
        eOptions.add_argument("--log-level=3")
        eOptions.add_argument("--disable-gpu")

        # for checking response code
        capabilities = DesiredCapabilities.EDGE.copy()
        capabilities["ms:loggingPrefs"] = {"performance": "ALL"}

        # auto downloads msedgedriver.exe
        eService = edgeService(EdgeChromiumDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Edge(service=eService, options=eOptions, capabilities=capabilities)
    else:
        with open(jsonPath, "w") as f:
            config = json.load(f)
            config["Browser"] = ""
            json.dump(config, f, indent=4)
        error_shutdown(
            en=("Error: Unknown browser type in config.json", "Please restart this program."),
            jap=("エラー： config.jsonに不明なブラウザタイプがある。", "このプログラムを再起動してください。")
        )

    return driver

def get_user_browser_preference():
    if lang == "en":
        selectedBrowser = get_input_from_user(prompt="Select a browser from the available options: ", command=("chrome", "firefox", "edge"), prints=("What browser would you like to use?", "Available browsers: Chrome, Firefox, Edge."), warning="Error: Invalid browser, please enter a browser from the available browsers.")
    else:
        selectedBrowser = get_input_from_user(prompt="利用可能なオプションからブラウザを選択します： ", command=("chrome", "firefox", "edge"), prints=("どのブラウザを使用しますか？", "使用可能なブラウザ： Chrome, Firefox, Edge。"), warning="エラー： 不正なブラウザです。使用可能なブラウザから選んでください。")
    return selectedBrowser

def check_browser_config():
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

def save_browser_config(selectedBrowser):
    with open(jsonPath, "r") as f:
        config = json.load(f)
    config["Browser"] = selectedBrowser
    with open(jsonPath, "w") as f:
        json.dump(config, f, indent=4)
    print_in_both_en_jp(
        en=(f"{S.GREEN}{selectedBrowser.title()} will be automatically loaded next time!{END}"),
        jp=(f"{S.GREEN}{selectedBrowser.title()}は次回起動時に自動的にロードされます！{END}")
    )

def get_key():
    keyPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "key.pik")
    if keyPath.is_file():
        with open(keyPath, "rb") as f:
            keyObject = dill.load(f)
    else:
        keyObject = Key()
        with open(keyPath, "wb") as f:
            dill.dump(keyObject, f)

    return keyObject.get_decKey()

def set_lang(config):
    try:
        print_in_both_en_jp(
            en=(f"\n{S.RED}Error: Language is not defined in the config.json file.{END}"),
            jp=(f"\n{S.RED}エラー： config.jsonのLanguage（言語）が見当たらないです。{END}")
        )
    except:
        print(f"\n{S.RED}エラー： config.jsonのLanguage（言語）が見当たらないです。{END}")
        print(f"\n{S.RED}Error: Language is not defined in the config.json file.{END}")


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
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        prefLang = config["Language"]
        if prefLang == "": raise Exception("Key is empty.")
        return prefLang
    except:
        return set_lang(config)

def update_lang():
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
                en=(f"{S.YELLOW}Language change cancelled.{END}"),
                jp=(f"{S.YELLOW}言語変更中止。{END}")
            )

        return config["Language"]
    else:
        return set_lang(config)

def check_if_user_is_logged_in():
    fantiaLoggedIn = pixivLoggedIn = False

    if "Fantia" in loggedIn: fantiaLoggedIn = True
    if "Pixiv" in loggedIn: pixivLoggedIn = True

    if fantiaLoggedIn and pixivLoggedIn: return True
    else: return False

"""--------------------------- End of Config Codes ---------------------------"""

# function below from https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code
def get_status(logs):
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
    hasFiles = any(dirPath.iterdir())
    return hasFiles

def fantia_login(fantiaEmail, fantiaPassword):
    driver.get("https://fantia.jp/sessions/signin")
    driver.find_element(by=By.ID, value="user_email").send_keys(fantiaEmail)
    driver.find_element(by=By.ID, value="user_password").send_keys(fantiaPassword)
    driver.find_element(by=By.XPATH, value="//button[@class='btn btn-primary btn-block mb-10 p-15']").click()

    # checks if the user is authenticated and wait for a max of 15 seconds for the page to load
    try:
        sleep(3)
        driver.get("https://fantia.jp/mypage/cart")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
        if driver.title != "ショッピングカート｜ファンティア[Fantia]": raise Exception("Fantia login failed.")
        print_in_both_en_jp(
            en=(f"{S.GREEN}Successfully logged in to Fantia!{END}"),
            jp=(f"{S.GREEN}Fantiaへのログインに成功しました!{END}")
        )
        return True
    except Exception or TimeoutException:
        # if there is no element with a class name of "loggedin", it will raise a TimeoutException
        print_in_both_en_jp(
            en=(f"{S.RED}Error: Fantia login failed.{END}"),
            jp=(f"{S.RED}エラー： Fantiaのログインに失敗しました。{END}")
        )
        return False
    except:
        error_shutdown(
            en=("Unexpected Error: Error when trying to login to Fantia.", "Please report this error to the developer."),
            jap=("予期せぬエラー： Fantiaにログインしようとするとエラーが発生します。", "このエラーを開発者に報告してください。")
        )

def pixiv_login(pixivUsername, pixivPassword):
    driver.get("https://www.fanbox.cc/login")
    driver.find_element(by=By.XPATH, value="//input[@placeholder='E-mail address / pixiv ID']").send_keys(pixivUsername)
    driver.find_element(by=By.XPATH, value="//input[@placeholder='password']").send_keys(pixivPassword)
    driver.find_element(by=By.XPATH, value="//button[@class='signup-form__submit']").click()

    # checks if the user is authenticated and wait for a max of 15 seconds for the page to load
    try:
        sleep(3)
        driver.get("https://www.fanbox.cc/creators/supporting")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
        if driver.title == "Supported Creators｜pixivFANBOX" or driver.title == "支援中のクリエイター｜pixivFANBOX": pass
        else: raise Exception("Pixiv login failed.")

        print_in_both_en_jp(
            en=(f"{S.GREEN}Successfully logged in to Pixiv!{END}"),
            jp=(f"{S.GREEN}Pixivへのログインに成功しました!{END}")
        )
        return True
    except Exception or TimeoutException:
        # if there is no anchor tag element with a class of "sc-1mdohqc-0 ilARNI", it will raise a TimeoutException
        print_in_both_en_jp(
            en=(f"{S.RED}Error: Pixiv login failed.{END}"),
            jp=(f"{S.RED}エラー： Pixivのログインに失敗しました。{END}")
        )
        return False
    except:
        error_shutdown(
            en=("Unexpected Error: Error when trying to login to Pixiv.", "Please report this error to the developer."),
            jap=("予期せぬエラー： Pixivにログインしようとするとエラーが発生します。", "このエラーを開発者に報告してください。")
        )

def get_image_name(imageURL, website):
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

def get_pixiv_image_full_res_url(imageURL):
    if imageURL.split(".")[-1] == "gif": return imageURL
    else:
        urlArray = []
        for urlParts in imageURL.split("/"):
            if urlParts == "w" or urlParts == "1200": pass
            else: urlArray.append(urlParts)
        return "/".join(urlArray)

def save_image(imageURL, pathToSave):
    with requests.get(imageURL, stream=True) as r:
        with open(pathToSave, "wb") as f:
            shutil.copyfileobj(r.raw, f)

def print_progress_bar(prog, totalEl, caption):
    barLength = 20 #size of progress bar
    currentProg = prog / totalEl
    sys.stdout.write("\r")
    sys.stdout.write(f"{S.YELLOW}[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}{END}")
    sys.stdout.flush()

def print_download_completion_message(totalImage):
    if totalImage > 0:
        print_in_both_en_jp(
            en=f"\n{S.GREEN}Successfully downloaded {totalImage} images!{END}",
            jp=f"\n{S.GREEN}{totalImage}枚の画像をダウンロードしました!{END}"
        )
    else:
        print_in_both_en_jp(
            en=(f"\n{S.RED}Error: No images to download.{END}"),
            jp=(f"\n{S.RED}エラー： ダウンロードする画像がありません。{END}")
        )

def download(urlInput, website, subFolderPath):
    driver.get(urlInput)

    if website == "FantiaImageURL":
        # downloading nth num of images based on the Fantia image given
        # e.g. https://fantia.jp/posts/*/post_content_photo/*
        image = driver.find_element(by=By.TAG_NAME, value="img")
        imageSrc = image.get_attribute("src")
        imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Fantia"))
        save_image(imageSrc, imagePath)

    elif website == "FantiaPost":
        imagePosts = driver.find_elements(by=By.CLASS_NAME, value="fantiaImage")
        imagePostsProgress = 1
        totalImagePosts = len(imagePosts)

        # downloading Fantia blog images that are may be locked by default due to membership restrictions
        for imagePost in imagePosts:
            imageHREFLink = imagePost.get_attribute("href")
            driver.get(imageHREFLink)
            image = driver.find_element(by=By.TAG_NAME, value="img")
            imageSrc = image.get_attribute("src")
            imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)

            if lang == "en":
                print_progress_bar(imagePostsProgress, totalImagePosts, f"Stage 1: Downloading image no.{imagePostsProgress} out of {totalImagePosts}")
            elif lang == "jp":
                print_progress_bar(imagePostsProgress, totalImagePosts, f"ステージ 1: 画像 {imagePostsProgress} / {totalImagePosts} をダウンロード中")
            
            imagePostsProgress += 1
            driver.get(urlInput) # returns to the original page

        # downloading Fantia images that are locked by default unless the user has a monthly subscription to the artist
        premiumImages = driver.find_elements(by=By.XPATH, value="//a[@class='image-container force-square clickable']")
        premiumImagesProgress = 1
        totalPremiumImages = len(imagePosts)

        for paidImageContainer in premiumImages:
            paidImageContainer.click()
            fullSizeButton = driver.find_element(by=By.XPATH, value="//button[@class='btn btn-secondary btn-sm mr-10 ng-scope']")
            imageHREFLink = fullSizeButton.get_attribute("href")
            driver.get(imageHREFLink)
            image = driver.find_element(by=By.TAG_NAME, value="img")
            imageSrc = image.get_attribute("src")
            imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)

            if lang == "en":
                print_progress_bar(premiumImagesProgress, totalPremiumImages, f"{S.YELLOW}Stage 2: Downloading image no.{premiumImagesProgress} out of {totalPremiumImages}{END}")
            else:
                print_progress_bar(premiumImagesProgress, totalPremiumImages, f"ステージ 2: 画像 {premiumImagesProgress} / {totalPremiumImages} をダウンロード中")

            premiumImagesProgress += 1
            driver.get(urlInput) # returns to the original page

        totalImages = totalImagePosts + totalPremiumImages
        print_download_completion_message(totalImages)

    elif website == "Pixiv":
        # downloads gifs or static images based on a pixiv post
        images = driver.find_elements(by=By.XPATH, value="//img[@class='sc-14k46gk-1']")

        progress = 1
        totalImages = len(images)

        for image in images:
            imageSrc = get_pixiv_image_full_res_url(image.get_attribute("src"))
            imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Pixiv"))
            save_image(imageSrc, imagePath)

            if lang == "en":
                print_progress_bar(progress, totalImages, f"Downloading image no.{progress} out of {totalImages}")
            else:
                print_progress_bar(progress, totalImages, f"画像 {progress} / {totalImages} をダウンロード中")
          
            progress += 1
            driver.get(urlInput) # returns to the original page

        print_download_completion_message(totalImages)

def create_subfolder():
    while True:
        if lang == "en": folderName = input("Enter the name of the folder you want to save the images (X to cancel): ").strip()
        else: folderName = input("画像を保存するフォルダーの名前を入力してください (\"X\"でキャンセル): ").strip()
        if folderName.upper() == "X": return "X"
        if folderName != "":
            
            # main download folder
            if not directoryPath.is_dir():
                directoryPath.mkdir(parents=True)

            # subfolder
            imagePath = directoryPath.joinpath(folderName)
            if not imagePath.is_dir():
                imagePath.mkdir(parents=True)

            if check_if_directory_has_files(imagePath): 
                print_in_both_en_jp(
                    en=(f"{S.RED}Error: Folder already exists with images inside.\nPlease enter a different {END}{S.UNDERLINE}{S.BOLD}{S.RED}NEW{END} {S.RED}name for a new folder.{END}"),
                    jp=(f"{S.RED}エラー： フォルダはすでに存在し、その中に画像があります。{END}{S.UNDERLINE}{S.BOLD}{S.RED}新しい名前{END}{S.RED}を入力してください。{END}")
                )
            else: return imagePath
        else:
            print_in_both_en_jp(
                en=(f"{S.RED}Error: Please enter a name for the folder.{END}"),
                jp=(f"{S.RED}エラー： フォルダの名前を入力してください。{END}")
            )

def print_menu():
    if "Fantia" in loggedIn: emailFantia = loggedIn["Fantia"]["email"]
    else: emailFantia = "Guest (Not logged in)"
    if "Pixiv" in loggedIn: usernamePixiv = loggedIn["Pixiv"]["username"]
    else: usernamePixiv = "Guest (Not logged in)"

    if emailFantia == "Guest (Not logged in)" or usernamePixiv == "Guest (Not logged in)":
        if lang == "jp": 
            emailFantia = "ゲスト（ログインしていない）"
            usernamePixiv = "ゲスト（ログインしていない）"

        if lang == "en": menu = f"""{S.YELLOW}
> You are currently logged in as...
> Fantia Email: {emailFantia}
> Pixiv ID: {usernamePixiv}
{END}
--------------------- {S.YELLOW}Download Options{END} --------------------
      {S.GREEN}1. Download images from Fantia using an image URL{END}
      {S.GREEN}2. Download images from a Fantia post URL{END}
      {S.CYAN}3. Download images from a Pixiv Fanbox post URL{END}

---------------------- {S.YELLOW}Config Options{END} ----------------------
      {S.LIGHT_BLUE}4. Update Account Details{END}
      {S.LIGHT_BLUE}5. Change Default Browser{END}
      {S.LIGHT_BLUE}6. Change Language{END}
      {S.LIGHT_BLUE}7. Login{END}
      {S.RED}X. Shutdown the program{END}
 """
        else: menu = f"""{S.YELLOW}
> あなたのログイン情報...
> FantiaEメール: {emailFantia}
> Pixiv ID: {usernamePixiv}
{END}
--------------------- {S.YELLOW}ダウンロードのオプション{END} ---------------------
      {S.GREEN}1. 画像URLでFantiaから画像をダウンロードする{END}
      {S.GREEN}2. Fantia投稿URLから画像をダウンロードする{END}
      {S.CYAN}3. Pixivファンボックスの投稿URLから画像をダウンロードする{END}

---------------------- {S.YELLOW}コンフィグのオプション{END} ----------------------
      {S.LIGHT_BLUE}4. アカウント情報を更新する{END}
      {S.LIGHT_BLUE}5. ブラウザを変更する{END}
      {S.LIGHT_BLUE}6. 言語を変更する{END}
      {S.LIGHT_BLUE}7. ログインする{END}
      {S.RED}X. プログラムを終了する{END}
"""

    else:
        if lang == "en": menu = f"""{S.YELLOW}
> You are currently logged in as...
> Fantia Email: {emailFantia}
> Pixiv ID: {usernamePixiv}
{END}
--------------------- {S.YELLOW}Download Options{END} --------------------
      {S.GREEN}1. Download images from Fantia using an image URL{END}
      {S.GREEN}2. Download images from a Fantia post URL{END}
      {S.CYAN}3. Download images from a Pixiv Fanbox post URL{END}

---------------------- {S.YELLOW}Config Options{END} ----------------------
      {S.LIGHT_BLUE}4. Update Account Details{END}
      {S.LIGHT_BLUE}5. Change Default Browser{END}
      {S.LIGHT_BLUE}6. Change Language{END}
      {S.RED}X. Shutdown the program{END}
 """
        else: menu = f"""{S.YELLOW}
> あなたのログイン情報...
> FantiaEメール: {emailFantia}
> Pixiv ID: {usernamePixiv}
{END}
--------------------- {S.YELLOW}ダウンロードのオプション{END} ---------------------
      {S.GREEN}1. 画像URLでFantiaから画像をダウンロードする{END}
      {S.GREEN}2. Fantia投稿URLから画像をダウンロードする{END}
      {S.CYAN}3. Pixivファンボックスの投稿URLから画像をダウンロードする{END}

---------------------- {S.YELLOW}コンフィグのオプション{END} ----------------------
      {S.LIGHT_BLUE}4. アカウント情報を更新する{END}
      {S.LIGHT_BLUE}5. ブラウザを変更する{END}
      {S.LIGHT_BLUE}6. 言語を変更する{END}
      {S.RED}X. プログラムを終了する{END}
"""
    print(menu)

def main():
    pythonMainVer = sys.version_info[0]
    pythonSubVer = sys.version_info[1]
    if pythonMainVer < 3 or pythonSubVer < 8:
        print(f"{S.RED}Fatal Error: This program requires running Python 3.8 or higher!", f"You are running Python {pythonMainVer}.{pythonSubVer}{S.RESET}"),
        print("{S.RED}致命的なエラー： このプログラムにはPython 3.8以上が必要です。", f"あなたはPython {pythonMainVer}.{pythonSubVer}を実行しています。{S.RESET}")

    # declare global variables
    global jsonPath
    global directoryPath
    global decKey
    global driver
    global lang
    global loggedIn
    global lang

    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "config.json")
    directoryPath = pathlib.Path(__file__).resolve().parent.joinpath("downloads")

    # checks if config.json exists and the necessary configs are defined
    check_if_json_file_exists()

    loggedIn = {}
    lang = get_lang()
    print_in_both_en_jp(
        en=(f"{S.YELLOW}Running program...{END}"),
        jp=(f"{S.YELLOW}プログラムを実行する...{END}")
    )

    # generate a key for the encryption of passwords so that it won't be stored in plaintext
    try: decKey = Fernet(get_key())
    except: error_shutdown(
                en=("Fatal Error: Unable to retrieve key for decryption!", "Please report this error to the developer."),
                jp=("致命的なエラー： 復号化のためのキーを取得することができません!", "開発者にこのエラーを報告してください。")
            )

    # get the preferred browser
    loadBrowser = check_browser_config()
    if loadBrowser == None:
        selectedBrowser = get_user_browser_preference()

        driver = get_driver(selectedBrowser)

        if lang == "en": browserPrompt = "Would you like to automatically use this browser upon running this program again? (y/n): "
        else: browserPrompt = "本プログラムの再実行時に、自動的にこのブラウザを使用しますか？ (y/n)： "
        saveBrowser = get_input_from_user(prompt=browserPrompt, command=("y", "n"))
        
        if saveBrowser == "y":
            save_browser_config(selectedBrowser)
    else: driver = get_driver(loadBrowser)

    if lang == "en": loginPrompt = "Would you like to login to Fantia and Pixiv? (y/n) or (\"X\" to shutdown): "
    else: loginPrompt = "FantiaとPixivにログインしませんか？ (y/n)または(\"X\"でシャットダウン): "

    userLoginCmd = get_input_from_user(prompt=loginPrompt, command=("y", "n", "x"))
    if userLoginCmd == "x": shutdown()
    elif userLoginCmd == "y":
        # logging into Fantia and Pixiv
        print_in_both_en_jp(
            en=(
                f"\n{S.YELLOW}Logging in to Fantia and Pixiv...{END}", 
                f"{S.ORANGE}Note: This program will automatically log you in to Fantia and Pixiv.\nHowever, it might fail to login due to possible slow internet speed...\nHence, do not be surprised if there's a login error and your credentials are correct, you can re-attempt to login later.{END}\n"
            ),
            jp=(
                f"\n{S.YELLOW}FantiaとPixivにログイン中...{END}",
                f"{S.ORANGE}注意：このプログラムは、FantiaとPixivに自動的にログインします。\nしかし、インターネットの速度が遅い可能性があるため、ログインに失敗する可能性があります...\nしたがって、ログインエラーが発生しても驚かず、あなたの認証情報が正しい場合は、後でログインを再試行できます。{END}\n"
            )
        )

        # gets account details for Fantia and Pixiv for downloading images that requires a membership
        try: fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account()
        except: error_shutdown(
                en=("Fatal Error: Unable to retrieve user accounts for Fantia and Pixiv Fanbox.", "Please report this error to the developer."),
                jap=("致命的なエラー： FantiaとPixiv Fanboxのユーザーアカウントを取得できません。", "開発者にこのエラーを報告してください。")
            )

        if fantiaEmail != None != fantiaPassword != None and pixivUsername != None and pixivPassword != None: 
            loginOnce = False
            while True:
                if loginOnce != True:
                    fantiaSuccess = fantia_login(fantiaEmail, fantiaPassword)
                    pixivSuccess = pixiv_login(pixivUsername, pixivPassword)
                loginOnce = True
                if fantiaSuccess and pixivSuccess:
                    print_in_both_en_jp(
                        en=(f"{S.GREEN}Logins were successful!{END}"),
                        jp=(f"{S.GREEN}ログインに成功しました！{END}")
                    )
                    loggedIn["Fantia"] = {"email": fantiaEmail, "password": fantiaPassword}
                    loggedIn["Pixiv"] = {"username": pixivUsername, "password": pixivPassword}
                    break
                else:
                    if lang == "en":
                        continueLoggingIn = get_input_from_user(prints=("\nWould you like to retry or change all your account details and login again?", "Available commands:\n\"y\" to change account details\n\"n\" to abort logging in\n\"r\" to re-attempt to login."), prompt="Please enter \"y\" or \"n\" or \"r\" to continue: ", command=("y", "n", "r"))
                    else:
                        continueLoggingIn = get_input_from_user(prints=("\n再試行またはアカウント情報をすべて変更し、再度ログインしますか？", "使用できるコマンド：\n\"y\" アカウント情報を変更する。\n\"n\" ログインを中止します。\n\"r\" ログインを再試行する。"), prompt="続行するには、\"y\"または\"n\"または\"r\"を入力してください： ", command=("y", "n", "r"))

                    if continueLoggingIn == "y": change_account_details("all", cred=["username", "password"])
                    elif continueLoggingIn == "r":
                        if not fantiaSuccess: fantiaSuccess = fantia_login(fantiaEmail, fantiaPassword)
                        if not pixivSuccess: pixivSuccess = pixiv_login(pixivUsername, pixivPassword)
                    else:
                        print_in_both_en_jp(
                            en=(f"\n{S.YELLOW}Ignoring login errors...{END}", 
                                f"{S.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}"
                            ),
                            jp=(f"\n{S.YELLOW}ログインエラーを無視する...{END}", 
                                f"{S.RED}ご注意：ファンティアとピクシブの両方にログインしていない可能性があるので、会員登録が必要な画像はダウンロードできません。{END}"
                            )
                        )
                        break

        if fantiaSuccess: loggedIn["Fantia"] = {"email": fantiaEmail, "password": fantiaPassword}
        if pixivSuccess: loggedIn["Pixiv"] = {"username": pixivUsername, "password": fantiaPassword}
    else:
        print_in_both_en_jp(
            en=(f"{S.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}"), 
            jap=(f"{S.RED}ご注意：ファンティアとピクシブの両方にログインしていない可能性があるので、会員登録が必要な画像はダウンロードできません。{END}")
        )

    cmdInput = ""
    cmdCommands = ("1", "2", "3", "4", "5", "6", "7", "x")
    while cmdInput != "x":
        print_menu()
        if lang == "en":
            cmdInput = get_input_from_user(prompt="Enter command: ", command=cmdCommands, warning="Error: Invalid command input, please enter a valid command from the menu above.")
        else:
            cmdInput = get_input_from_user(prompt="コマンドを入力してください： ", command=cmdCommands, warning="エラー： 不正なコマンド入力です。上のメニューから正しいコマンドを入力してください。")
        if cmdInput == "1":
            imagePath = create_subfolder()
            if imagePath != "X":
                while True:
                    if lang == "en": urlInput = input("Enter the URL of the first image: ").strip()
                    else: urlInput = input("最初の画像のURLを入力してください： ").strip()

                    if urlInput == "": 
                        print_in_both_en_jp(
                            en=(f"{S.RED}Error: No URL entered.{END}", "Please enter a valid URL."),
                            jp=(f"{S.RED}エラー： URLが入力されていません。{END}", "URLを入力してください。")
                        )
                    else: break

                imageCounter = 1
                print_in_both_en_jp(
                    en=(f"{S.YELLOW}Downloading images...{END}"),
                    jp=(f"{S.GREEN}画像をダウンロードする...{END}")
                )

                urlArray = []
                while True:
                    driver.get(urlInput)
                    logs = driver.get_log("performance")
                    if get_status(logs) != 200: break

                    imageCounter += 1
                    urlArray.append(urlInput)

                    # increment the urlInput by one to retrieve the next image
                    splitURL = urlInput.split("/")
                    urlNum = str(int(splitURL[-1]) + 1)
                    urlPartsArray = splitURL[0:-1]
                    urlPartsArray.append(urlNum)
                    urlInput = "/".join(urlPartsArray)
                    del urlPartsArray

                if imageCounter != 1:
                    progress = 1
                    totalImages = len(urlArray)
                    for url in urlArray:
                        download(url, "FantiaImageURL", imagePath)
                        if lang == "en":
                            print_progress_bar(progress, totalImages, f"{S.YELLOW}Downloading image no.{progress} out of {totalImages}{END}")
                        else:
                            print_progress_bar(progress, totalImages, f"画像 {progress} / {totalImages} をダウンロード中")
                        
                        progress += 1

                print_download_completion_message(imageCounter-1)

        elif cmdInput == "2":
            imagePath = create_subfolder()
            if imagePath != "X":
                while True:
                    if lang == "en": urlInput = input("Enter the URL of the Fantia post: ").strip()
                    else: urlInput = input("Fantiaの投稿のURLを入力します： ").strip()

                    if urlInput == "": print_in_both_en_jp(
                                        en=(f"{S.RED}Error: No URL entered.{END}", "Please enter a valid URL."),
                                        jp=(f"{S.RED}エラー： URLが入力されていません。{END}", "URLを入力してください。")
                                    )
                    else: break

                imageCounter = 1
                print_in_both_en_jp(
                    en=(f"{S.YELLOW}Downloading images...{END}"),
                    jp=(f"{S.GREEN}画像をダウンロードする...{END}")
                )
                download(urlInput, "FantiaPost", imagePath)

        elif cmdInput == "3":
            imagePath = create_subfolder()
            if imagePath != "X":
                while True:
                    if lang == "en": urlInput = input("Enter the URL of the Pixiv Fanbox post: ").strip()
                    else: urlInput = input("Pixivファンボックスの投稿URLを入力してください： ").strip()
                    if urlInput == "": print_in_both_en_jp(
                                        en=(f"{S.RED}Error: No URL entered.{END}", "Please enter a valid URL."),
                                        jp=(f"{S.RED}エラー： URLが入力されていません。{END}", "URLを入力してください。")
                                    )
                    else: break

                imageCounter = 1
                print_in_both_en_jp(
                    en=(f"{S.YELLOW}Downloading images...{END}"),
                    jp=(f"{S.GREEN}画像をダウンロードする...{END}")
                )
                download(urlInput, "Pixiv", imagePath)

        elif cmdInput == "4":
            if lang == "en": webPrompt = "Which accounts would you like to update for? (Fantia/Pixiv/X to cancel): "
            else: webPrompt = "どのアカウントを更新しますか？（Fantia/Pixiv/All/Xでキャンセル）： "

            if lang == "en": credPrompt = "Enter the credentials to change (Username/Password/All/X to cancel): "
            else: credPrompt = "変更する資格情報を入力してください（Username/Password/All/Xでキャンセル）: "

            website = get_input_from_user(prompt=webPrompt, command=("fantia", "pixiv", "all", "x"))
            if website != "x":
                credentialsToChange = get_input_from_user(prompt=credPrompt, command=("username", "password", "all", "x"))

                if credentialsToChange != "x":
                    if credentialsToChange == "all": credentialsToChange = ["username", "password"]
                    else: credentialsToChange = [credentialsToChange] # convert to list
                    change_account_details(website, cred=credentialsToChange)
            
        elif cmdInput == "5":
            defaultBrowser = check_browser_config()
            if defaultBrowser != None:
                newDefaultBrowser = get_user_browser_preference()
                save_browser_config(newDefaultBrowser)
            else:
                print_in_both_en_jp(
                    en=(f"{S.RED}Error: No default browser found.{END}"),
                    jp=(f"{S.RED}エラー： デフォルトのブラウザが見つかりませんでした。{END}")
                )

                if lang == "en": browserPrompt = "Would you like to save a browser as your default browser for this program? (y/n): "
                else: browserPrompt = "このプログラムのデフォルトのブラウザを保存しますか？ (y/n): "
                saveBrowser = get_input_from_user(prompt=browserPrompt, command=("y", "n"))

                if saveBrowser == "y":
                    newDefaultBrowser = get_user_browser_preference()
                    save_browser_config(newDefaultBrowser)
                else: print_in_both_en_jp(
                        en=(f"{S.YELLOW}Note: Default Browser is unchanged.{END}"),
                        jp=(f"{S.YELLOW}注意： デフォルトブラウザは変更なし。{END}")
                    )

        elif cmdInput == "6":
            lang = update_lang()

        elif cmdInput == "7" and not check_if_user_is_logged_in():
            pass

if __name__ == "__main__":
    global END
    END = S.RESET

    introMenu = f"""
====================== {S.LIGHT_BLUE}CULTURED DOWNLOADER v{version}{END} ======================
=========== {S.LIGHT_BLUE}https://github.com/KJHJason/Cultured-Downloader{END} ===========
================ {S.LIGHT_BLUE}Author/開発者: KJHJason, aka Dratornic{END} ================
{S.YELLOW}
Purpose/目的: Allows you to download multiple images from Fantia or Pixiv Fanbox automatically.
              FantiaやPixivファンボックスから複数の画像を自動でダウンロードできるようにします。

Note/注意: Requires the user to provide his/her credentials for images that requires a membership.
           This program is not affiliated with Pixiv or Fantia.
           会員登録が必要な画像には、ユーザーの認証情報の提供が必要です。
           このプログラムはPixivやFantiaとは関係ありません。{END}
"""
    print(introMenu)
    main()
    shutdown()