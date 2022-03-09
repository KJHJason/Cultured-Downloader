__author__ = "KJHJason"
__copyright__ = "Copyright 2022 KJHJason"
__credits__ = ["KJHJason"]
__license__ = "MIT License"
__version__ = "1.11"

# Import Third-party Libraries
import requests, dill
from colorama import init as coloramaInit
from colorama import Style
from colorama import Fore as F
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
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.edge.options import Options as edgeOptions

# Import Standard Libraries
import pathlib, json, sys, logging, webbrowser
from urllib.parse import urlparse
from json.decoder import JSONDecodeError
from random import uniform
from time import sleep
from datetime import datetime
from shutil import rmtree, copyfileobj

# Importing Custom Python Files as Modules
from Key import Key

"""--------------------------- Config Codes ---------------------------"""

def shutdown():
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
    logFolderPath = get_saved_config_data_folder().joinpath("logs")
    print(f"\n{F.RED}Unknown Error Occurred/不明なエラーが発生した{END}")
    print(f"{F.RED}Please provide the developer with a error text file generated in {logFolderPath}\n{logFolderPath}に生成されたエラーテキストファイルを開発者に提供してください。\n{END}")
    try: driver.close()
    except: pass

def log_error():
    filePath = get_saved_config_data_folder().joinpath("logs")
    if not filePath.is_dir(): filePath.mkdir(parents=True)

    fileName = "".join([f"cultured-downloader-v{__version__ }-error-", datetime.now().strftime("%d-%m-%Y"), ".txt"])
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
    prints = kwargs.get("prints")
    prompt = kwargs.get("prompt")
    commands = kwargs.get("command")
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
    dataDirectory = pathlib.Path.home().joinpath("AppData", "LocalLow", "Cultured Downloader")
    if not dataDirectory.is_dir(): dataDirectory.mkdir(parents=True)
    return dataDirectory

def encrypt_string(inputString):
    return decKey.encrypt(inputString.encode()).decode()

def decrypt_string(inputString):
    try:
        return decKey.decrypt(inputString.encode()).decode()
    except:
        print_in_both_en_jp(
            en=(f"{F.RED}Fatal Error: Could not decrypt string.{END}", f"{F.RED}Resetting Key and encrypted values in config.json...{END}"),
            jp=(f"{F.RED}致命的なエラー: 文字列を復号化できませんでした。{END}", f"{F.RED}config.jsonのキーと暗号化された値をリセットしています...{END}")
        )
        keyPath = appPath.joinpath("configs", "key")
        if keyPath.is_file():
            keyPath.unlink()
        
        with open(jsonPath, "r") as f:
            config = json.load(f)
        
        config["Accounts"]["Fantia"]["Password"] = ""
        config["Accounts"]["Pixiv"]["Password"] = ""
        
        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)
            
        error_shutdown(en=("Please restart the program."), jp=("このプログラムを再起動してください。"))

def get_user_account(website):
    with open(jsonPath, "r") as f:
        config = json.load(f)
    if website == "all":
        try:
            fantiaEmail = config["Accounts"]["Fantia"]["User"]
            fantiaPassword = config["Accounts"]["Fantia"]["Password"]
            pixivUsername = config["Accounts"]["Pixiv"]["User"]
            pixivPassword = config["Accounts"]["Pixiv"]["Password"]
            if fantiaEmail == "" or fantiaPassword == "" or pixivUsername == "" or pixivPassword == "":
                raise Exception("Account details had empty values.")
            
            try: fantiaPassword = decrypt_string(fantiaPassword)
            except: raise SystemExit

            try: pixivPassword = decrypt_string(pixivPassword)
            except: raise SystemExit

            return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword
        except SystemExit:
            config["Accounts"]["Fantia"]["Password"] = ""
            config["Accounts"]["Pixiv"]["Password"] = ""
            with open(jsonPath, "w") as f:
                json.dump(config, f, indent=4)
            raise SystemExit
        except Exception or KeyError:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: config.json does not have all the necessary account details.{END}"),
                jp=(f"{F.RED}エラー: config.jsonに必要なアカウントの詳細がありません。{END}")
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
                        en=(f"{F.RED}Warning: Since you have not added your account details yet,\nyou will not be able to download any images that requires a membership.\nFret not, you can add your account details later.{END}"),
                        jp=(f"{F.RED}ご注意： まだアカウント情報を追加していないため、\n会員登録が必要な画像をダウンロードすることはできません。\n後でアカウント情報を追加することができますので、ご安心ください。{END}")
                    )

                    config.update(data)
                    with open(jsonPath, "w") as f:
                        json.dump(config, f, indent=4)
                    return None, None, None, None
                else:
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Fantia...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaのアカウント情報を追加しています...{END}")
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
                        en=(f"{F.GREEN}Fantia Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Fantiaのアカウント情報を追加しました！{END}")
                    )

                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Pixiv...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を追加しています...{END}")
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
                        en=(f"{F.GREEN}Pixiv Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Pixivのアカウント情報を追加しました！{END}")
                    )
                    
                    return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword
            else: 
                fantiaData = config["Accounts"]["Fantia"]
                pixivData = config["Accounts"]["Pixiv"]

                if fantiaData["User"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Fantia...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaのアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": fantiaEmail = input("Enter your email address for Fantia: ").lower().strip()
                        else: fantiaEmail = input("FantiaアカウントのEメールを入力してください： ").lower().strip()
                        if fantiaEmail != "":
                            fantiaData["User"] = fantiaEmail
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Email for Fantia Account successfully added!{END}"),
                        jp=(f"{F.GREEN}FantiaアカウントのEメール追加に成功しました！{END}")
                    )
                if fantiaData["Password"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Fantia...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaのアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": fantiaPassword = input("Enter your password for Fantia: ")
                        else: fantiaPassword = input("Fantiaアカウントのパスワードを入力してください： ")
                        if fantiaPassword != "":
                            fantiaData["Password"] = encrypt_string(fantiaPassword)
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Password for Fantia Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Fantiaアカウントのパスワード追加に成功しました！{END}")
                    )
                if pixivData["User"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Pixiv...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": pixivUsername = input("Enter your Pixiv ID: ").strip()
                        else: pixivUsername = input("PixivアカウントのIDを入力してください： ").strip()
                        if pixivUsername != "":
                            pixivData["User"] = pixivUsername
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Pixiv ID successfully added!{END}"),
                        jp=(f"{F.GREEN}PixivアカウントのID追加に成功しました！{END}")
                    )
                if pixivData["Password"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Pixiv fanbox...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": pixivPassword = input("Enter your password for Pixiv: ")
                        else: pixivPassword = input("Pixivアカウントのパスワードを入力してください： ")
                        if pixivPassword != "":
                            pixivData["Password"] = encrypt_string(pixivPassword)
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Password for Pixiv Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Pixivアカウントのパスワード追加に成功しました！{END}")
                    )
                
                with open(jsonPath, "w") as f:
                    json.dump(config, f, indent=4)

                return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword
    elif website == "fantia":
        try:
            fantiaEmail = config["Accounts"]["Fantia"]["User"]
            fantiaPassword = config["Accounts"]["Fantia"]["Password"]
            if fantiaEmail == "" or fantiaPassword == "":
                raise Exception("Fantia account details had empty values.")
            
            try: fantiaPassword = decrypt_string(fantiaPassword)
            except: raise SystemExit

            return fantiaEmail, fantiaPassword
        except SystemExit:
            config["Accounts"]["Fantia"]["Password"] = ""
            with open(jsonPath, "w") as f:
                json.dump(config, f, indent=4)
            raise SystemExit
        except Exception or KeyError:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: config.json does not have all the necessary account details.{END}"),
                jp=(f"{F.RED}エラー: config.jsonに必要なアカウントの詳細がありません。{END}")
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
                        en=(f"{F.RED}Warning: Since you have not added your account details yet,\nyou will not be able to download any images that requires a membership.\nFret not, you can add your account details later.{END}"),
                        jp=(f"{F.RED}ご注意： まだアカウント情報を追加していないため、\n会員登録が必要な画像をダウンロードすることはできません。\n後でアカウント情報を追加することができますので、ご安心ください。{END}")
                    )

                    config.update(data)
                    with open(jsonPath, "w") as f:
                        json.dump(config, f, indent=4)
                    return None, None
                else:
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Fantia...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaのアカウント情報を追加しています...{END}")
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
                        en=(f"{F.GREEN}Fantia Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Fantiaのアカウント情報を追加しました！{END}")
                    )

                    with open(jsonPath, "w") as f:
                        config.update(data)
                        json.dump(config, f, indent=4)

                    return fantiaEmail, fantiaPassword
            else: 
                fantiaData = config["Accounts"]["Fantia"]

                if fantiaData["User"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Fantia...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaのアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": fantiaEmail = input("Enter your email address for Fantia: ").lower().strip()
                        else: fantiaEmail = input("FantiaアカウントのEメールを入力してください： ").lower().strip()
                        if fantiaEmail != "":
                            fantiaData["User"] = fantiaEmail
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Email for Fantia Account successfully added!{END}"),
                        jp=(f"{F.GREEN}FantiaアカウントのEメール追加に成功しました！{END}")
                    )
                if fantiaData["Password"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Fantia...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaのアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": fantiaPassword = input("Enter your password for Fantia: ")
                        else: fantiaPassword = input("Fantiaアカウントのパスワードを入力してください： ")
                        if fantiaPassword != "":
                            fantiaData["Password"] = encrypt_string(fantiaPassword)
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Password for Fantia Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Fantiaアカウントのパスワード追加に成功しました！{END}")
                    )
                
                with open(jsonPath, "w") as f:
                    json.dump(config, f, indent=4)

                return fantiaEmail, fantiaPassword
    elif website == "pixiv":
        try:
            pixivEmail = config["Accounts"]["Pixiv"]["User"]
            pixivPassword = config["Accounts"]["Pixiv"]["Password"]
            if pixivEmail == "" or pixivPassword == "":
                raise Exception("Fantia account details had empty values.")
            
            try: pixivPassword = decrypt_string(pixivPassword)
            except: raise SystemExit

            return pixivEmail, pixivPassword
        except SystemExit:
            config["Accounts"]["Pixiv"]["Password"] = ""
            with open(jsonPath, "w") as f:
                json.dump(config, f, indent=4)
            raise SystemExit
        except Exception or KeyError:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: config.json does not have all the necessary account details.{END}"),
                jp=(f"{F.RED}エラー: config.jsonに必要なアカウントの詳細がありません。{END}")
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
                        en=(f"{F.RED}Warning: Since you have not added your account details yet,\nyou will not be able to download any images that requires a membership.\nFret not, you can add your account details later.{END}"),
                        jp=(f"{F.RED}ご注意： まだアカウント情報を追加していないため、\n会員登録が必要な画像をダウンロードすることはできません。\n後でアカウント情報を追加することができますので、ご安心ください。{END}")
                    )

                    config.update(data)
                    with open(jsonPath, "w") as f:
                        json.dump(config, f, indent=4)
                    return None, None
                else:
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Pixiv...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を追加しています...{END}")
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
                        en=(f"{F.GREEN}Pixiv Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Pixivのアカウント情報を追加しました！{END}")
                    )
                    
                    return pixivUsername, pixivPassword
            else: 
                pixivData = config["Accounts"]["Pixiv"]
                if pixivData["User"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Pixiv...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": pixivUsername = input("Enter your Pixiv ID: ").strip()
                        else: pixivUsername = input("PixivアカウントのIDを入力してください： ").strip()
                        if pixivUsername != "":
                            pixivData["User"] = pixivUsername
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Pixiv ID successfully added!{END}"),
                        jp=(f"{F.GREEN}PixivアカウントのID追加に成功しました！{END}")
                    )
                if pixivData["Password"] == "":
                    print_in_both_en_jp(
                        en=(f"\n{F.LIGHTYELLOW_EX}Adding account details for Pixiv fanbox...{END}"),
                        jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を追加しています...{END}")
                    )

                    while True:
                        if lang == "en": pixivPassword = input("Enter your password for Pixiv: ")
                        else: pixivPassword = input("Pixivアカウントのパスワードを入力してください： ")
                        if pixivPassword != "":
                            pixivData["Password"] = encrypt_string(pixivPassword)
                            break

                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Password for Pixiv Account successfully added!{END}"),
                        jp=(f"{F.GREEN}Pixivアカウントのパスワード追加に成功しました！{END}")
                    )
                
                with open(jsonPath, "w") as f:
                    json.dump(config, f, indent=4)

                return pixivUsername, pixivPassword

def change_account_details(typeToChange, **credToUpdate):
    credentialsToChangeList = credToUpdate.get("cred")
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        if typeToChange == "fantia":
            print_in_both_en_jp(
                en=(f"\n{F.LIGHTYELLOW_EX}Changing account details for Fantia...{END}"),
                jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaアカウント情報を変更する...{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
                        )
                        break

        elif typeToChange == "pixiv":
            print_in_both_en_jp(
                en=(f"\n{F.LIGHTYELLOW_EX}Changing Pixiv Account Details...{END}"),
                jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を変更する...{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
                        )
                        break
                
        elif typeToChange == "all":
            print_in_both_en_jp(
                en=(f"\n{F.LIGHTYELLOW_EX}Changing account details for Fantia...{END}"),
                jp=(f"\n{F.LIGHTYELLOW_EX}Fantiaアカウント情報を変更する...{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
                        )
                        break

            print_in_both_en_jp(
                en=(f"\n{F.LIGHTYELLOW_EX}Changing Pixiv Account Details...{END}"),
                jp=(f"\n{F.LIGHTYELLOW_EX}Pixivアカウント情報を変更する...{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
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
                            en=(f"{F.GREEN}No changes made!{END}"),
                            jp=(f"{F.GREEN}変更は行われませんでした！{END}")
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
        cOptions.add_argument("--disable-dev-shm-usage") # from https://stackoverflow.com/questions/62898801/selenium-headless-chrome-runs-much-slower

        # for checking response code
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        # change default download location
        cOptions.add_experimental_option("prefs", {
            "download.default_directory": str(pixivDownloadLocation),
            "profile.managed_default_content_settings.images": 2
        })

        # auto downloads chromedriver.exe
        gService = chromeService(ChromeDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Chrome(service=gService, options=cOptions, desired_capabilities=capabilities)
    elif browserType == "edge":
        # minimise the browser window and hides unnecessary text output
        eOptions = edgeOptions()
        eOptions.headless = True
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
            "profile.managed_default_content_settings.images": 2
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

def get_user_browser_preference():
    if lang == "en":
        selectedBrowser = get_input_from_user(prompt="Select a browser from the available options: ", command=("chrome", "edge"), prints=("What browser would you like to use?", "Available browsers: Chrome, Edge."), warning="Invalid browser, please enter a browser from the available browsers.")
    else:
        selectedBrowser = get_input_from_user(prompt="利用可能なオプションからブラウザを選択します： ", command=("chrome", "edge"), prints=("どのブラウザを使用しますか？", "使用可能なブラウザ： Chrome, Edge。"), warning="不正なブラウザです。使用可能なブラウザから選んでください。")
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
        en=(f"{F.GREEN}{selectedBrowser.title()} will be automatically loaded next time!{END}"),
        jp=(f"{F.GREEN}{selectedBrowser.title()}は次回起動時に自動的にロードされます！{END}")
    )

def get_key():
    keyPath = appPath.joinpath("configs", "key")
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
    fantiaLoggedIn = pixivLoggedIn = False

    if "Fantia" in loggedIn: fantiaLoggedIn = True
    if "Pixiv" in loggedIn: pixivLoggedIn = True

    if fantiaLoggedIn and pixivLoggedIn: return True
    else: return False

def set_default_download_directory_to_desktop(jsonConfig):
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


"""--------------------------- End of Config Codes ---------------------------"""

"""--------------------------- Start of Functions Codes ---------------------------"""

def check_if_input_is_url(inputString):
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
    userInput = userInput.replace(" ", "")
    userInput = userInput.replace("　", "")
    if "," in userInput: userInput = userInput.split(",")
    elif "、" in userInput: userInput = userInput.split("、")
    return userInput

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

def randomise_delay():
    sleep(round(uniform(0.2, 0.6), 2))

def save_pixiv_cookie():
    driver.get("https://www.fanbox.cc/")
    sleep(5)
    pixivCookieDirPath = appPath.joinpath("configs")
    pixivCookieDirPath.mkdir(parents=True, exist_ok=True)
    pixivCookiePath = pixivCookieDirPath.joinpath("pixiv_cookies")
    with open(pixivCookiePath, 'wb') as f:
        dill.dump(driver.get_cookies(), f)
    print_in_both_en_jp(
        en=(
            f"{F.GREEN}The cookie saved to {pixivCookiePath}\nThe cookie will be automatically loaded in next time in Cultured Downloader for a faster login process!{END}", f"{F.RED}Warning: Please do not share the cookie with anyone as they will be able to gain access to your pixiv account!{END}"
        ),
        jp=(
            f"{F.GREEN}{pixivCookiePath} に保存されたクッキーは、次回からCultured Downloaderで自動的に読み込まれ、ログイン処理が速くなります!{END}", 
            f"{F.RED}警告： このクッキーを誰かと共有すると、あなたのpixivアカウントにアクセスできてしまうので、共有しないでください！"
        )
    )

def save_fantia_cookie():
    driver.get("https://fantia.jp/")
    sleep(5)
    fantiaCookieDirPath = appPath.joinpath("configs")
    fantiaCookieDirPath.mkdir(parents=True, exist_ok=True)
    fantiaCookiePath = fantiaCookieDirPath.joinpath("fantia_cookies")
    with open(fantiaCookiePath, 'wb') as f:
        Fantiacookies = driver.get_cookies()
        for cookie in reversed(Fantiacookies): # reversed since most of the time the _session_id cookie is at the bottom of the list of cookies
            if cookie["name"] == "_session_id":
                dill.dump(cookie, f)
                break

    print_in_both_en_jp(
        en=(
            f"{F.GREEN}The cookie saved to {fantiaCookiePath}\nThe cookie will be automatically loaded in next time in Cultured Downloader for a faster login process!{END}", f"{F.RED}Warning: Please do not share the cookie with anyone as they will be able to gain access to your pixiv account!{END}"
        ),
        jp=(
            f"{F.GREEN}{fantiaCookiePath} に保存されたクッキーは、次回からCultured Downloaderで自動的に読み込まれ、ログイン処理が速くなります!{END}", 
            f"{F.RED}警告： このクッキーを誰かと共有すると、あなたのpixivアカウントにアクセスできてしまうので、共有しないでください！"
        )
    )

def load_pixiv_cookie():
    cookiePath = appPath.joinpath("configs", "pixiv_cookies")

    if cookiePath.is_file():
        driver.get("https://www.fanbox.cc/")
        sleep(5)
        with open(cookiePath, 'rb') as f:
            pixivCookies = dill.load(f)
        for cookie in pixivCookies:
            driver.add_cookie(cookie)

        driver.get("https://www.fanbox.cc/messages")
        sleep(5)
        if driver.current_url == "https://www.fanbox.cc/messages": 
            print_in_both_en_jp(
                en=(f"{F.GREEN}Pixiv Fanbox cookied loaded successfully!{END}"),
                jp=(f"{F.GREEN}Pixivファンボックスのクッキーが正常に読み込まれました！{END}")
            )
            return True
        else: return False
    else: return False

def get_pixiv_cookie():
    cookiePath = appPath.joinpath("configs", "pixiv_cookies")

    if cookiePath.is_file():
        pixivSessionID = ""
        with open(cookiePath, 'rb') as f:
            pixivCookies = dill.load(f)
            for cookie in pixivCookies:
                if cookie["name"] == "FANBOXSESSID":
                    pixivSessionID = cookie["value"]
                    break
        
        if pixivSessionID != "":
            pixivSessionObject = requests.session()
            pixivSessionIDCookie = requests.cookies.create_cookie(domain="fanbox.cc", name="FANBOXSESSID", value=pixivSessionID)
            pixivSessionObject.cookies.set_cookie(pixivSessionIDCookie)
            return pixivSessionObject
        else: return ""
    else: return ""

def load_fantia_cookie():
    cookiePath = appPath.joinpath("configs", "fantia_cookies")

    if cookiePath.is_file():
        driver.get("https://fantia.jp/")
        sleep(5)
        with open(cookiePath, 'rb') as f:
            cookie = dill.load(f)
            driver.delete_all_cookies()
            driver.add_cookie(cookie)

        driver.get("https://fantia.jp/mypage/users/plans")
        sleep(5)
        if driver.current_url == "https://fantia.jp/mypage/users/plans": 
            print_in_both_en_jp(
                en=(f"{F.GREEN}Fantia cookied loaded successfully!{END}"),
                jp=(f"{F.GREEN}Fantiaのクッキーが正常に読み込まれました！{END}")
            )
            return True
        else: return False
    else: return False

def fantia_login(fantiaEmail, fantiaPassword):
    # a bunch of sleep delays to prevent being detected for being a bot
    driver.get("https://fantia.jp/sessions/signin")
    sleep(4)
    driver.find_element(by=By.ID, value="user_email").send_keys(fantiaEmail)
    sleep(3)
    driver.find_element(by=By.ID, value="user_password").send_keys(fantiaPassword)
    sleep(3)
    driver.find_element(by=By.XPATH, value="//button[@class='btn btn-primary btn-block mb-10 p-15']").click()

    # checks if the user is authenticated
    try:
        sleep(15)
        driver.get("https://fantia.jp/mypage/cart")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
        if driver.current_url != "https://fantia.jp/mypage/cart": raise Exception("Fantia login failed.")
        print_in_both_en_jp(
            en=(f"{F.GREEN}Successfully logged in to Fantia!{END}"),
            jp=(f"{F.GREEN}Fantiaへのログインに成功しました!{END}")
        )
        if lang == "en": pixivCookiePrompt = "Would you like to save your Fantia session cookie for a faster login next time? (y/n): "
        else: pixivCookiePrompt = "Fantiaのセッションクッキーを保存して、次回のログインを早くしたいですか？ (y/n): "
        savePixivCookieCondition = get_input_from_user(prompt=pixivCookiePrompt, command=("y", "n"))
        if savePixivCookieCondition == "y": 
            save_fantia_cookie()
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Saving of Fantia cookie will be aborted as per user's request.{END}"),
                jp=(f"{F.RED}FantiaのセッションCookieの保存は、ユーザーの要求に応じて中止されます。{END}")
            )
        return True
    except Exception or TimeoutException:
        print_in_both_en_jp(
            en=(f"{F.RED}Error: Fantia login failed.{END}"),
            jp=(f"{F.RED}エラー： Fantiaのログインに失敗しました。{END}")
        )
        return False
    except:
        error_shutdown(
            en=("Unexpected Error: Error when trying to login to Fantia.", "Please report this error to the developer."),
            jap=("予期せぬエラー： Fantiaにログインしようとするとエラーが発生します。", "このエラーを開発者に報告してください。")
        )

def pixiv_login(pixivUsername, pixivPassword):
    # a bunch of sleep delays to prevent being detected for being a bot
    driver.get("https://www.fanbox.cc/login")
    if driver.current_url == "https://www.fanbox.cc/": return True
    driver.execute_script("window.scroll({top: 250, left: 0, behavior: 'smooth'});")
    sleep(5)
    for char in pixivUsername:
        driver.find_element(by=By.XPATH, value="//input[@placeholder='E-mail address / pixiv ID']").send_keys(char)
        randomise_delay()

    sleep(2)
    for char in pixivPassword:
        driver.find_element(by=By.XPATH, value="//input[@placeholder='password']").send_keys(char)
        randomise_delay()

    sleep(2)
    driver.find_element(by=By.XPATH, value="//button[@class='signup-form__submit']").click()
    sleep(3)

    # checks if the user is authenticated
    try:
        sleep(15)
        driver.get("https://www.fanbox.cc/creators/supporting")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
        if driver.current_url != "https://www.fanbox.cc/creators/supporting": raise Exception("Pixiv login failed.")

        print_in_both_en_jp(
            en=(f"{F.GREEN}Successfully logged in to Pixiv!{END}"),
            jp=(f"{F.GREEN}Pixivへのログインに成功しました!{END}")
        )

        if lang == "en": pixivCookiePrompt = "Would you like to save your pixiv session cookie for a faster login next time? (y/n): "
        else: pixivCookiePrompt = "pixivのセッションクッキーを保存して、次回のログインを早くしたいですか？ (y/n): "
        savePixivCookieCondition = get_input_from_user(prompt=pixivCookiePrompt, command=("y", "n"))
        if savePixivCookieCondition == "y": 
            save_pixiv_cookie()
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Saving of pixiv cookie will be aborted as per user's request.{END}"),
                jp=(f"{F.RED}pixivのセッションCookieの保存は、ユーザーの要求に応じて中止されます。{END}")
            )
        return True
    except Exception or TimeoutException:
        print_in_both_en_jp(
            en=(f"{F.RED}Error: Pixiv login failed.{END}"),
            jp=(f"{F.RED}エラー： Pixivのログインに失敗しました。{END}")
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
    try:
        if imageURL.split(".")[-1] == "gif": return imageURL
        else:
            urlArray = []
            for urlParts in imageURL.split("/"):
                if urlParts == "w" or urlParts == "1200": pass
                else: urlArray.append(urlParts)
            return "/".join(urlArray)
    except AttributeError:
        raise AttributeError

def save_image(imageURL, pathToSave, **requestSession):
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
    barLength = 20 #size of progress bar
    currentProg = prog / totalEl
    sys.stdout.write("\r")
    sys.stdout.write(f"{F.LIGHTYELLOW_EX}[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}{END}")
    sys.stdout.flush()

def print_download_completion_message(totalImage, subFolderPath):
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
    driver.execute_script("window.open('_blank');")
    driver.switch_to.window(driver.window_handles[-1])

def close_new_tab():
    driver.execute_script("window.close();")
    driver.switch_to.window(driver.window_handles[0])

def get_latest_post_num_from_file_name():
    postNumList = []
    try:
        for filePath in pixivDownloadLocation.iterdir():
            if filePath.is_file():
                filePath = str(filePath.name).split("_")
                postNumList.append(int(filePath[1]))
        return max(postNumList) + 1
    except:
        return 0

def download_image_javascript(imageSrcURL, imageName):
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
                en=(f"{F.LIGHTYELLOW_EX}Skipping stage 1...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}ステージ1をスキップします...{END}")
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
                en=(f"{F.LIGHTYELLOW_EX}Skipping stage 2...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}ステージ2をスキップします...{END}")
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
                en=(f"{F.LIGHTYELLOW_EX}Skipping stage 3...{END}"),
                jp=(f"{F.LIGHTYELLOW_EX}ステージ3をスキップします...{END}")
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

def check_if_path_contains_illegal_char(userPathInput):
    # checks if the user's input path is valid
    illegalChars = '<>:"/\\|?*' # based on https://docs.microsoft.com/en-gb/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN
    if any(char in illegalChars for char in userPathInput): return True
    else: return False

def create_subfolder(website):
    while True:
        if lang == "en": folderName = input("Enter the name of the folder you want to save the images (X to cancel): ").strip()
        else: folderName = input("画像を保存するフォルダーの名前を入力してください (\"X\"でキャンセル): ").strip()

        if not check_if_path_contains_illegal_char(folderName):
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

def print_menu():
    if "Fantia" in loggedIn: emailFantia = loggedIn["Fantia"]["user"]
    else: emailFantia = "Guest (Not logged in)"
    if "Pixiv" in loggedIn: usernamePixiv = loggedIn["Pixiv"]["user"]
    else: usernamePixiv = "Guest (Not logged in)"

    if lang == "jp": 
        emailFantia = "ゲスト（ログインしていない）"
        usernamePixiv = "ゲスト（ログインしていない）"

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
      {F.LIGHTBLUE_EX}5. アカウント情報を更新する{END}
      {F.LIGHTBLUE_EX}6. ブラウザを変更する{END}
      {F.LIGHTBLUE_EX}7. 言語を変更する{END}
"""
        if emailFantia == "ゲスト（ログインしていない）" or usernamePixiv == "ゲスト（ログインしていない）":
            menuAdditionalOptions = f"""      {F.LIGHTBLUE_EX}8. ログインする{END}\n"""
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
      {F.LIGHTBLUE_EX}5. Update Account Details{END}
      {F.LIGHTBLUE_EX}6. Change Default Browser{END}
      {F.LIGHTBLUE_EX}7. Change Language{END}
"""
        if emailFantia == "Guest (Not logged in)" or usernamePixiv == "Guest (Not logged in)":
            menuAdditionalOptions = f"""      {F.LIGHTBLUE_EX}8. Login{END}\n"""
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
    global loggedIn
    global fantiaDownloadLocation
    global pixivDownloadLocation
    global pixivCookieLoaded
    global fantiaCookieLoaded
    global pixivSession

    appPath = get_saved_config_data_folder()
    jsonPath = appPath.joinpath("configs", "config.json")

    # checks if config.json exists and the necessary configs are defined
    check_if_json_file_exists()

    loggedIn = {}
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

    # retrieve cookie if exists
    pixivCookieLoaded = fantiaCookieLoaded = False

    fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
    pixivCookiePath = appPath.joinpath("configs", "pixiv_cookies")

    if fantiaCookiePath.is_file() or fantiaCookiePath.is_file():    
        if lang == "en": cookiePrompt = "Would you like to load your cookies? (y/n): "
        else: cookiePrompt = "クッキーをロードしますか？ (y/n)： "
        userCookieInput = get_input_from_user(prompt=cookiePrompt, command=("y", "n"))
        if userCookieInput == "y":
            pixivCookieLoaded = load_pixiv_cookie()
            fantiaCookieLoaded = load_fantia_cookie()
        else:
            print_in_both_en_jp(
                en=(f"{F.YELLOW}Cookies will not be loaded into the webdriver...{END}"),
                jp=(f"{F.YELLOW}その場合、クッキーは読み込まれません...{END}")
            )

    if pixivCookieLoaded: pixivSession = get_pixiv_cookie()

    # gets account details for Fantia and Pixiv for downloading images that requires a membership
    if not pixivCookieLoaded and not fantiaCookieLoaded: fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account("all")
    else: 
        if not pixivCookieLoaded: pixivUsername, pixivPassword = get_user_account("pixiv")
        if not fantiaCookieLoaded: fantiaEmail, fantiaPassword = get_user_account("fantia")

    if pixivCookieLoaded:
        if lang == "en": pixivUsername = pixivPassword = "User account loaded from cookie"
        else: pixivUsername = pixivPassword = "クッキーから読み込まれるユーザーアカウント"
        loggedIn["Pixiv"] = {"user": pixivUsername, "password": pixivPassword}
    if fantiaCookieLoaded:
        if lang == "en": fantiaEmail = fantiaPassword = "User account loaded from cookie"
        else: fantiaEmail = fantiaPassword = "クッキーから読み込まれるユーザーアカウント"
        loggedIn["Fantia"] = {"user": fantiaEmail, "password": fantiaPassword}

    while True:
        if not pixivCookieLoaded and not fantiaCookieLoaded:

            if lang == "en": loginPrompt = "Would you like to login to Fantia and Pixiv? (y/n) or (\"X\" to shutdown): "
            else: loginPrompt = "FantiaとPixivにログインしませんか？ (y/n)または(\"X\"でシャットダウン): "

            userLoginCmd = get_input_from_user(prompt=loginPrompt, command=("y", "n", "x"))
            if userLoginCmd == "x": shutdown()
            elif userLoginCmd == "y":
                print_in_both_en_jp(
                    en=(
                        f"\n{F.LIGHTYELLOW_EX}Logging in to Fantia and Pixiv (may take quite a while)...{END}", 
                        f"{F.LIGHTRED_EX}Note: This program will automatically log you in to Fantia and Pixiv.\nHowever, it might fail to login due to possible slow internet speed...\nHence, do not be surprised if there's a login error and your credentials are correct, you can re-attempt to login later.{END}\n"
                    ),
                    jp=(
                        f"\n{F.LIGHTYELLOW_EX}FantiaとPixivにログイン中（ログインにかなり時間がかか）...{END}",
                        f"{F.LIGHTRED_EX}注意：このプログラムは、FantiaとPixivに自動的にログインします。\nしかし、インターネットの速度が遅い可能性があるため、ログインに失敗する可能性があります...\nしたがって、ログインエラーが発生しても驚かず、あなたの認証情報が正しい場合は、後でログインを再試行できます。{END}\n"
                    )
                )

                if fantiaEmail != None and fantiaPassword != None and pixivUsername != None and pixivPassword != None: 
                    fantiaSuccess = fantia_login(fantiaEmail, fantiaPassword)
                    pixivSuccess = pixiv_login(pixivUsername, pixivPassword)

                if fantiaSuccess and pixivSuccess:
                    print_in_both_en_jp(
                        en=(f"{F.GREEN}Logins were successful!{END}"),
                        jp=(f"{F.GREEN}ログインに成功しました！{END}")
                    )
                else:
                    print_in_both_en_jp(
                    en=(f"{F.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}"), 
                    jap=(f"{F.RED}ご注意：ファンティアとピクシブの両方にログインしていない可能性があるので、会員登録が必要な画像はダウンロードできません。{END}")
                )

                if fantiaSuccess: loggedIn["Fantia"] = {"user": fantiaEmail, "password": fantiaPassword}
                if pixivSuccess: loggedIn["Pixiv"] = {"user": pixivUsername, "password": pixivPassword}
                break
            else:
                print_in_both_en_jp(
                    en=(f"{F.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}"), 
                    jap=(f"{F.RED}ご注意：ファンティアとピクシブの両方にログインしていない可能性があるので、会員登録が必要な画像はダウンロードできません。{END}")
                )
                break
        else:
            if not pixivCookieLoaded or not fantiaCookieLoaded:
                if pixivCookieLoaded and not fantiaCookieLoaded:
                    if lang == "en": loginPrompt = "Would you like to login to Fantia (y/n) or (\"X\" to shutdown): "
                    else: loginPrompt = "Fantiaにログインしませんか？ (y/n)または(\"X\"でシャットダウン): "
                elif not pixivCookieLoaded and fantiaCookieLoaded:
                    if lang == "en": loginPrompt = "Would you like to login to Pixiv (y/n) or (\"X\" to shutdown): "
                    else: loginPrompt = "Pixivにログインしませんか？ (y/n)または(\"X\"でシャットダウン): "

                userLoginCmd = get_input_from_user(prompt=loginPrompt, command=("y", "n", "x"))
                if userLoginCmd == "x": shutdown()
                elif userLoginCmd == "y":
                    if pixivCookieLoaded and not fantiaCookieLoaded:
                        print_in_both_en_jp(
                            en=(
                                f"\n{F.LIGHTYELLOW_EX}Logging in to Fantia...{END}", 
                                f"{F.LIGHTRED_EX}Note: This program will automatically log you in to Fantia.\nHowever, it might fail to login due to possible slow internet speed...\nHence, do not be surprised if there's a login error and your credentials are correct, you can re-attempt to login later.{END}\n"
                            ),
                            jp=(
                                f"\n{F.LIGHTYELLOW_EX}Fantiaにログイン中...{END}",
                                f"{F.LIGHTRED_EX}注意：このプログラムは、Fantiaに自動的にログインします。\nしかし、インターネットの速度が遅い可能性があるため、ログインに失敗する可能性があります...\nしたがって、ログインエラーが発生しても驚かず、あなたの認証情報が正しい場合は、後でログインを再試行できます。{END}\n"
                            )
                        )
                    elif not pixivCookieLoaded and fantiaCookieLoaded:
                        print_in_both_en_jp(
                            en=(
                                f"\n{F.LIGHTYELLOW_EX}Logging in to pixiv...{END}", 
                                f"{F.LIGHTRED_EX}Note: This program will automatically log you in to pixiv.\nHowever, it might fail to login due to possible slow internet speed...\nHence, do not be surprised if there's a login error and your credentials are correct, you can re-attempt to login later.{END}\n"
                            ),
                            jp=(
                                f"\n{F.LIGHTYELLOW_EX}pixivにログイン中...{END}",
                                f"{F.LIGHTRED_EX}注意：このプログラムは、pixivに自動的にログインします。\nしかし、インターネットの速度が遅い可能性があるため、ログインに失敗する可能性があります...\nしたがって、ログインエラーが発生しても驚かず、あなたの認証情報が正しい場合は、後でログインを再試行できます。{END}\n"
                            )
                        )

                    if fantiaEmail != None and fantiaPassword != None and pixivUsername != None and pixivPassword != None: 
                        if not fantiaCookieLoaded: fantiaSuccess = fantia_login(fantiaEmail, fantiaPassword)
                        if not pixivCookieLoaded: pixivSuccess = pixiv_login(pixivUsername, pixivPassword)

                    if fantiaSuccess or pixivSuccess:
                        print_in_both_en_jp(
                            en=(f"{F.GREEN}Logins were successful!{END}"),
                            jp=(f"{F.GREEN}ログインに成功しました！{END}")
                        )
                    else:
                        print_in_both_en_jp(
                        en=(f"{F.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}"), 
                        jap=(f"{F.RED}ご注意：ファンティアとピクシブの両方にログインしていない可能性があるので、会員登録が必要な画像はダウンロードできません。{END}")
                    )

                    if fantiaSuccess: loggedIn["Fantia"] = {"user": fantiaEmail, "password": fantiaPassword}
                    if pixivSuccess: loggedIn["Pixiv"] = {"user": pixivUsername, "password": pixivPassword}
                    break
                else:
                    print_in_both_en_jp(
                        en=(f"{F.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}"), 
                        jap=(f"{F.RED}ご注意：ファンティアとピクシブの両方にログインしていない可能性があるので、会員登録が必要な画像はダウンロードできません。{END}")
                    )
                    break
            else: break

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
                            en=(f"{F.RED}Error: No URL entered.{END}", "Please enter a valid URL."),
                            jp=(f"{F.RED}エラー： URLが入力されていません。{END}", "URLを入力してください。")
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
                            en=(f"{F.RED}Error: No URL entered.{END}", "Please enter a valid URL."),
                            jp=(f"{F.RED}エラー： URLが入力されていません。{END}", "URLを入力してください。")
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
                        en=(f"{F.LIGHTYELLOW_EX}Note: Default Browser is unchanged.{END}"),
                        jp=(f"{F.LIGHTYELLOW_EX}注意： デフォルトブラウザは変更なし。{END}")
                    )

        elif cmdInput == "7":
            lang = update_lang()

        elif cmdInput == "8" and not check_if_user_is_logged_in():
            if (fantiaEmail != None or fantiaPassword != None) and (pixivUsername != None or pixivPassword != None) and (pixivCookieLoaded != True and fantiaCookieLoaded != True): 
                fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account("all")
            elif not fantiaCookieLoaded: 
                fantiaEmail, fantiaPassword = get_user_account("fantia")
            elif not pixivCookieLoaded: 
                pixivUsername, pixivPassword = get_user_account("pixiv")
            else: 
                fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account("all")

            if fantiaEmail != None and fantiaPassword != None and pixivUsername != None and pixivPassword != None:
                print_in_both_en_jp(
                    en=(
                        f"\n{F.LIGHTYELLOW_EX}Logging in to Fantia and Pixiv (may take quite a while)...{END}", 
                        f"{F.LIGHTRED_EX}Note: This program will automatically log you in to Fantia and Pixiv.\nHowever, it might fail to login due to possible slow internet speed...\nHence, do not be surprised if there's a login error and your credentials are correct, you can re-attempt to login later.{END}\n"
                    ),
                    jp=(
                        f"\n{F.LIGHTYELLOW_EX}FantiaとPixivにログイン中（ログインにかなり時間がかか）...{END}",
                        f"{F.LIGHTRED_EX}注意：このプログラムは、FantiaとPixivに自動的にログインします。\nしかし、インターネットの速度が遅い可能性があるため、ログインに失敗する可能性があります...\nしたがって、ログインエラーが発生しても驚かず、あなたの認証情報が正しい場合は、後でログインを再試行できます。{END}\n"
                    )
                )
                fantiaSuccessful = False
                pixivSuccessful = False
                while True:
                    if "Fantia" not in loggedIn: fantiaSuccessful = fantia_login(fantiaEmail, fantiaPassword)
                    else: fantiaSuccessful = True
                    if "Pixiv" not in loggedIn: pixivSuccessful = pixiv_login(pixivUsername, pixivPassword)
                    else: pixivSuccessful = True
                    
                    if fantiaSuccessful and "Fantia" not in loggedIn: loggedIn["Fantia"] = {"user": fantiaEmail, "password": fantiaPassword}
                    if pixivSuccessful and "Pixiv" not in loggedIn: loggedIn["Pixiv"] = {"user": pixivUsername, "password": fantiaPassword}
                    
                    if pixivSuccessful != True or fantiaSuccessful != True:
                        if lang == "en": 
                            loginPrints = ("\nWould you like to retry or change all your account details and login again?", "Available commands:\n\"y\" to change account details\n\"n\" to abort logging in\n\"r\" to re-attempt to login.")
                            loginPrompts = "Please enter \"y\" or \"n\" or \"r\" to continue: "
                        else: 
                            loginPrints = ("\n再試行またはアカウント情報をすべて変更し、再度ログインしますか？", "使用できるコマンド：\n\"y\" アカウント情報を変更する。\n\"n\" ログインを中止します。\n\"r\" ログインを再試行する。") 
                            loginPrompts = "続行するには、\"y\"または\"n\"または\"r\"を入力してください： "

                        continueLoggingIn = get_input_from_user(prints=loginPrints, prompt=loginPrompts, command=("y", "n", "r"))
                        if continueLoggingIn == "y": 
                            change_account_details("all", cred=["username", "password"])
                            fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account("all")
                        elif continueLoggingIn == "r": continue
                        else: break
                    else: break

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
                
        elif cmdInput == "dc" and (pixivCookieLoaded or fantiaCookieLoaded):
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
================ {F.LIGHTBLUE_EX}Author/開発者: KJHJason, aka Dratornic{END} ================
{F.LIGHTYELLOW_EX}
Purpose/目的: Allows you to download multiple images from Fantia or Pixiv Fanbox automatically.
              FantiaやPixivファンボックスから複数の画像を自動でダウンロードできるようにします。

Note/注意: Requires the user to provide his/her credentials for images that requires a membership.
           This program is not affiliated with Pixiv or Fantia.
           会員登録が必要な画像には、ユーザーの認証情報の提供が必要です。
           このプログラムはPixivやFantiaとは関係ありません。{END}

{F.RED}Disclaimer/免責条項: 
1. This program, Cultured Downloader, is not liable for any damages caused. 
   This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually.
   本プログラム「Cultured Downloader」は、発生した損害について一切の責任を負いかねます。
   このプログラムは、個人的な使用と、pixiv FanboxとFantiaから画像を手動でダウンロードする時間を節約するためのものです。

2. As a user of this program, you must never share any data such as config.json to other people.
   If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable but the user(s) involved will be.
   本プログラムのユーザーとして、config.jsonなどのデータは絶対に他人と共有しないでください。
   もし、あなたのデータを共有したり、他人のデータを使用していることが判明した場合、このプログラムおよび開発者は責任を負いませんが、関係するユーザーは責任を負うことになります。

   (In an event of mistranslation, the English version will take priority and will be used/誤訳があった場合は、英語版を優先して使用します。)
{END}{F.LIGHTRED_EX}
Known Issues/既知のバグについて: 
1. Frequent logins to Pixiv per day will show a captcha which will render the program useless...
   To resolve this, please go to pixiv manually and try to login again and clear the captcha.
   Pixivに1日に何度もログインすると、キャプチャが表示され、プログラムが使えなくなる...
   解決するには、手動でpixivにアクセスし、再度ログインしてキャプチャをクリアしてみてください。

2. Logins are slow or the logins always fails.
   To resolve this, please run pixiv_manual_login.exe and fantia_manual_login.exe to save the cookies needed for your login sessions.
   However, please do not share your cookies as it is the same as sharing your accounts with others.
   ログインに時間がかかる、または常にログインに失敗する。
   これを解決するには、pixiv_manual_login.exe と fantia_manual_login.exe を実行し、ログインセッションに必要なクッキーを保存してください。
   ただし、Cookieを共有することは、他の人とアカウントを共有することと同じですので、絶対にやめてください。

3. Sometimes the program does not shutdown automatically. In this case, please close the program manually or press CTRL + C to terminate the program.
   プログラムが自動的にシャットダウンしないことがあります。この場合、手動でプログラムを終了させるか、CTRL + Cキーを押してプログラムを終了させてください{END}
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
    except:
        print_error_log_notification()
        log_error()
        sys.exit()

    shutdown()