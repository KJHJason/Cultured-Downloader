version = "0.10"

# Import Third-party Libraries
import dill
from colorama import init as coloramaInit
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

# Importing Custom Python Files as Modules
from Colour_Settings import TerminalColours as S

def print_error_log_notification():
    print(f"\n{S.RED}Unknown Error Occurred/不明なエラーが発生した{END}")
    print(f"{S.RED}Please provide the developer with a error text file generated in the logs folder/\nlogsフォルダに生成されたエラーテキストファイルを開発者に提供してください。\n{END}")
    try: driver.close()
    except: pass

def log_error():
    filePath = pathlib.Path(__file__).resolve().parent.joinpath("logs")
    if not filePath.is_dir(): filePath.mkdir(parents=True)

    fileName = "".join(["pixiv-login-error-", datetime.now().strftime("%d-%m-%Y"), ".txt"])
    fullFilePath = filePath.joinpath(fileName)
    
    if not fullFilePath.is_file():
        with open(fullFilePath, "w") as f:
            f.write(f"Cultured Downloader's Pixiv Manual Login Program v{version} Error Logs\n\n")
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

def pixiv_login():
    driver.get("https://www.fanbox.cc/login")
    if driver.current_url == "https://www.fanbox.cc/": return True

    print_in_both_en_jp(
        en=(f"{S.YELLOW}A new browser should have opened.{END}", f"{S.YELLOW}Please enter your username and password and login to Pixiv manually.{END}"),
        jp=(f"{S.YELLOW}新しいブラウザが起動したはずです。{END}", f"{S.YELLOW}ユーザー名とパスワードを入力し、手動でPixivにログインしてください。{END}")
    )

    if lang == "en": input("Press any key to continue after logging in...")
    else: input("ログイン後に何かキーを押してください...")

    try:
        driver.get("https://www.fanbox.cc/creators/supporting")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/head/title"))
        )
    except TimeoutException:
        print_in_both_en_jp(
            en=(f"{S.RED}Error: TimeoutException. Please try again.{END}"),
            jp=(f"{S.RED}エラー: タイムアウトエラー。再度実行してください。{END}")
        )
        return False

    if driver.current_url != "https://www.fanbox.cc/creators/supporting":
        print_in_both_en_jp(
            en=(f"{S.RED}Error: Pixiv login failed.{END}"),
            jp=(f"{S.RED}エラー： Pixivのログインに失敗しました。{END}")
        )
        return False

def main():
    global lang
    global driver
    
    lang = get_input_from_user(prompt="Select a language/言語を選択してください (en/jp): ", command=("en", "jp"))

    browserType = get_user_browser_preference()
    driver = get_driver(browserType)

    pixivLoggedIn = False
    while True:
        pixivLoggedIn = pixiv_login()
        if pixivLoggedIn: break
        else:
            if lang == "en": retryInput = get_input_from_user(prompt="Would you like to retry logging in manually? (y/n): ", command=("y", "n"))
            else: retryInput = get_input_from_user(prompt="もう一度手動でログインし直しますか？(y/n)： ", command=("y", "n"))
            if retryInput == "n": break

    if pixivLoggedIn:
        if driver.current_url != "https://www.fanbox.cc/": driver.get("https://www.fanbox.cc/")
        configFolder = pathlib.Path(__file__).resolve().parent.joinpath("configs")
        if not configFolder.is_dir(): configFolder.mkdir(parents=True)
        with open(configFolder.joinpath("pixiv_cookies"), 'wb') as f:
            dill.dump(driver.get_cookies(), f)
        print_in_both_en_jp(
            en=(f"{S.GREEN}The cookie saved will be automatically loaded in!{END}"),
            jp=(f"{S.GREEN}保存されたクッキーは自動的に読み込まれます！{END}")
        )
    
    driver.close()
    raise SystemExit
            
if __name__ == "__main__":
    coloramaInit(autoreset=False, wrap=False)
    global END
    END = S.RESET
    introMenu = f"""
====================== {S.LIGHT_BLUE}CULTURED DOWNLOADER's PIXIV MANUAL LOGIN PROGRAM v{version}{END} ======================
========================== {S.LIGHT_BLUE}https://github.com/KJHJason/Cultured-Downloader{END} =========================
============================== {S.LIGHT_BLUE}Author/開発者: KJHJason, aka Dratornic{END} ==============================
{S.YELLOW}
Purpose/目的: Allows you to login to Pixiv manually and save the cookie for faster login in the main program, Cultured Downloader.
              Pixivに手動でログインし、メインプログラムのCultured Downloaderでより速くログインするためのクッキーを保存できるようにします。

Note/注意: This program is not affiliated with Pixiv or Fantia.
           このプログラムはPixivやFantiaとは関係ありません。{END}
"""
    print(introMenu)

    try:
        main()
    except SystemExit:
        print_in_both_en_jp(
            en=(f"{S.YELLOW}Thank you, this program will now exit...{END}"),
            jp=(f"{S.YELLOW}ありがとうございました、このプログラムは終了します...{END}")
        )
        if lang == "en": input("Please enter any key to exit...")
        else: input("何か入力すると終了します。。。")
        sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n{S.RED}Program Terminated/プログラムが終了しました{END}")
        sleep(1)
        sys.exit(0)
    except:
        print_error_log_notification()
        log_error()
        sys.exit(1)