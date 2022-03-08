version = "1.00"

# Import Third-party Libraries
import dill
from colorama import init as coloramaInit
from colorama import Style
from colorama import Fore as F
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.chrome.options import Options as chromeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.edge.options import Options as edgeOptions

# Import Standard Libraries
import pathlib, sys, logging
from datetime import datetime
from time import sleep

def get_saved_config_data_folder():
    dataDirectory = pathlib.Path.home().joinpath("AppData", "LocalLow", "Cultured Downloader")
    if not dataDirectory.is_dir(): dataDirectory.mkdir(parents=True)
    return dataDirectory

def print_error_log_notification():
    logFolderPath = get_saved_config_data_folder().joinpath("logs")
    print(f"\n{F.RED}Unknown Error Occurred/不明なエラーが発生した{END}")
    print(f"{F.RED}Please provide the developer with a error text file generated in {logFolderPath}\n{logFolderPath}に生成されたエラーテキストファイルを開発者に提供してください。\n{END}")
    try: driver.close()
    except: pass

def log_error():
    filePath = get_saved_config_data_folder().joinpath("logs")
    if not filePath.is_dir(): filePath.mkdir(parents=True)

    fileName = "".join([f"pixiv-manual-login-error-v{version}-", datetime.now().strftime("%d-%m-%Y"), ".txt"])
    fullFilePath = filePath.joinpath(fileName)
    
    if not fullFilePath.is_file():
        with open(fullFilePath, "w") as f:
            f.write(f"Cultured Downloader Pixiv Manual Login v{version} Error Logs\n\n")
    else:
        with open(fullFilePath, "a") as f:
            f.write(f"\n")

    logging.basicConfig(filename=fullFilePath, filemode="a", format="%(asctime)s - %(message)s")
    logging.error("Error Details: ", exc_info=True)

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

def get_user_browser_preference():
    if lang == "en":
        selectedBrowser = get_input_from_user(prompt="Select a browser from the available options: ", command=("chrome", "edge"), prints=("What browser would you like to use?", "Available browsers: Chrome, Edge."), warning="Invalid browser, please enter a browser from the available browsers.")
    else:
        selectedBrowser = get_input_from_user(prompt="利用可能なオプションからブラウザを選択します： ", command=("chrome", "edge"), prints=("どのブラウザを使用しますか？", "使用可能なブラウザ： Chrome, Edge。"), warning="不正なブラウザです。使用可能なブラウザから選んでください。")
    return selectedBrowser

def get_driver(browserType):
    if browserType == "chrome":
        #minimise the browser window and hides unnecessary text output
        cOptions = chromeOptions()
        cOptions.headless = False
        cOptions.add_argument("--log-level=3")
        cOptions.add_argument("--disable-gpu")
        cOptions.add_argument('--disable-dev-shm-usage') # from https://stackoverflow.com/questions/62898801/selenium-headless-chrome-runs-much-slower

        # auto downloads chromedriver.exe
        gService = chromeService(ChromeDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Chrome(service=gService, options=cOptions)
    elif browserType == "edge":
        # minimise the browser window and hides unnecessary text output
        eOptions = edgeOptions()
        eOptions.headless = False
        eOptions.use_chromium = True
        eOptions.add_argument("--log-level=3")
        eOptions.add_argument("--disable-gpu")

        # auto downloads msedgedriver.exe
        eService = edgeService(EdgeChromiumDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Edge(service=eService, options=eOptions)

    return driver

def fantia_login():
    driver.get("https://fantia.jp/sessions/signin")

    print_in_both_en_jp(
        en=(f"{F.LIGHTYELLOW_EX}A new browser should have opened.{END}", f"{F.LIGHTYELLOW_EX}Please enter your username and password and login to Fantia manually.{END}"),
        jp=(f"{F.LIGHTYELLOW_EX}新しいブラウザが起動したはずです。{END}", f"{F.LIGHTYELLOW_EX}ユーザー名とパスワードを入力し、手動でFantiaにログインしてください。{END}")
    )

    if lang == "en": input("Press any key to continue after logging in...")
    else: input("ログイン後に何かキーを押してください...")

    try:
        driver.get("https://fantia.jp/mypage/users/plans")
        sleep(3)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
    except TimeoutException:
        print_in_both_en_jp(
            en=(f"{F.RED}Error: TimeoutException. Please try again.{END}"),
            jp=(f"{F.RED}エラー: タイムアウトエラー。再度実行してください。{END}")
        )
        return False

    if driver.current_url != "https://fantia.jp/mypage/users/plans": return False
    else: return True

def main():
    global lang
    global driver
    global appPath

    appPath = get_saved_config_data_folder()
    fantiaCookiePath = appPath.joinpath("configs", "fantia_cookies")
    
    print(f"{F.YELLOW}Select a language/言語を選択してください{END}")
    lang = get_input_from_user(prompt="(en/jp) or/または (\"X\" to shutdown/\"X\"でキャンセル） : ", command=("en", "jp", "x"))
    
    if lang == "x": raise SystemExit

    browserType = get_user_browser_preference()
    driver = get_driver(browserType)

    fantiaLoggedIn = False
    while True:
        fantiaLoggedIn = fantia_login()
        if fantiaLoggedIn: break
        else:
            print_in_both_en_jp(
                en=(f"{F.RED}Error: Fantia login failed.{END}"),
                jp=(f"{F.RED}エラー： Fantiaのログインに失敗しました。{END}")
            )
            if lang == "en": retryInput = get_input_from_user(prompt="Would you like to retry logging in manually? (y/n): ", command=("y", "n"))
            else: retryInput = get_input_from_user(prompt="もう一度手動でログインし直しますか？(y/n)： ", command=("y", "n"))
            if retryInput == "n": break

    if fantiaLoggedIn:
        if driver.current_url != "https://fantia.jp/": driver.get("https://fantia.jp/")
        configFolder = appPath.joinpath("configs")
        if not configFolder.is_dir(): configFolder.mkdir(parents=True)
        with open(fantiaCookiePath, 'wb') as f:
            Fantiacookies = driver.get_cookies()
            for cookie in reversed(Fantiacookies): # reversed since most of the time the _session_id cookie is at the bottom of the list of cookies
                if cookie["name"] == "_session_id":
                    dill.dump(cookie, f)
                    break

        print_in_both_en_jp(
            en=(f"{F.GREEN}The cookie saved to {fantiaCookiePath}\nThe cookie will be automatically loaded in next time in Cultured Downloader for a faster login process!{END}"),
            jp=(f"{F.GREEN}{fantiaCookiePath} に保存されたクッキーは、次回からCultured Downloaderで自動的に読み込まれ、ログイン処理が速くなります!{END}")
        )
    
    driver.close()
    raise SystemExit
            
if __name__ == "__main__":
    coloramaInit(autoreset=False, convert=True)
    global END
    END = Style.RESET_ALL

    introMenu = f"""
====================== {F.LIGHTBLUE_EX}CULTURED DOWNLOADER's FANTIA MANUAL LOGIN v{version}{END} ======================
========================== {F.LIGHTBLUE_EX}https://github.com/KJHJason/Cultured-Downloader{END} =========================
============================== {F.LIGHTBLUE_EX}Author/開発者: KJHJason, aka Dratornic{END} ==============================
{F.LIGHTYELLOW_EX}
Purpose/目的: Allows you to login to Fantia manually and save the cookie for faster login in the main program, Cultured Downloader.
              Fantiaに手動でログインし、メインプログラムのCultured Downloaderでより速くログインするためのクッキーを保存できるようにします。

Note/注意: This program is not affiliated with Pixiv or Fantia.
           このプログラムはPixivやFantiaとは関係ありません。{END}

{F.RED}Disclaimer/免責条項: 
1. This program, Cultured Downloader's Fantia Manual Login, is not liable for any damages caused. 
   This program is meant for personal use and to save time from logging into Fantia on the main program, Cultured Downloader.
   本プログラム「Cultured Downloader's Fantia Manual Login」は、発生した損害について一切の責任を負いません。
   このプログラムは、個人的な使用を目的とし、メインプログラムであるCultured DownloaderでFantiaにログインする時間を短縮するためのものです。

2. As a user of this program, you must never share any data such as config.json to other people.
   If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable but the user(s) involved will be.
   本プログラムのユーザーとして、config.jsonなどのデータは絶対に他人と共有しないでください。
   もし、あなたのデータを共有したり、他人のデータを使用していることが判明した場合、このプログラムおよび開発者は責任を負いませんが、関係するユーザーは責任を負うことになります。

   (In an event of mistranslation, the English version will take priority and will be used/誤訳があった場合は、英語版を優先して使用します。)
{END}{F.LIGHTRED_EX}
Known Issues/既知のバグについて: 
1. Sometimes the program does not shutdown automatically. In this case, please close the program manually or press CTRL + C to terminate the program.
   プログラムが自動的にシャットダウンしないことがあります。この場合、手動でプログラムを終了させるか、CTRL + Cキーを押してプログラムを終了させてください{END}
"""
    print(introMenu)

    try:
        main()
    except SystemExit:
        print_in_both_en_jp(
            en=(f"{F.LIGHTYELLOW_EX}Thank you, this program will now exit...{END}"),
            jp=(f"{F.LIGHTYELLOW_EX}ありがとうございました、このプログラムは終了します...{END}")
        )
        if lang == "en": input("Please enter any key to exit...")
        elif lang == "jp": input("何か入力すると終了します。。。")
        else: input("Please enter any key to exit/何か入力すると終了します。。。")
        sys.exit()
    except KeyboardInterrupt:
        print(f"\n{F.RED}Program Terminated/プログラムが終了しました{END}")
        sleep(1)
        sys.exit()
    except:
        print_error_log_notification()
        log_error()
        sys.exit(1)