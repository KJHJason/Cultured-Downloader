from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.chrome.options import Options as chromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.firefox.options import Options as firefoxOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.edge.options import Options as edgeOptions
from warnings import filterwarnings, catch_warnings
from colorama import Fore, Style
from time import sleep
from cryptography.fernet import Fernet
import requests, pathlib, json, sys, shutil

"""Config Codes"""

def check_if_json_file_exists():
    jsonFolderPath = pathlib.Path(__file__).resolve().parent.joinpath("configs")
    if not jsonFolderPath.is_dir(): jsonFolderPath.mkdir(parents=True)
    if not jsonPath.is_file():
        print(f"{Fore.RED}Error: config.json does not exist.{Fore.RESET}")
        print(f"{Fore.YELLOW}Creating config.json file...{Fore.RESET}")
        with open(jsonPath, "w") as f:
            json.dump({}, f)
    else: print(f"{Fore.GREEN}Loading configurations from config.json...{RESET}")

def encrypt_string(inputString):
    return decKey.encrypt(inputString.encode()).decode()

def decrypt_string(inputString):
    try:
        return decKey.decrypt(inputString.encode()).decode()
    except:
        print(f"{Fore.RED}Fatal Error: Could not decrypt string.{RESET}")
        print(f"{Fore.RED}Resetting Key and encrypted values in config.json...{RESET}")
        with open(jsonPath, "r") as f:
            config = json.load(f)
        config["Key"] = ""
        config["Accounts"]["Fantia"]["Password"] = ""
        config["Accounts"]["pixiv"]["Password"] = ""
        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)
        print(f"{Fore.RED}Please restart the program.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)

def get_user_account():
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        fantiaEmail = config["Accounts"]["Fantia"]["User"]
        fantiaPassword = config["Accounts"]["Fantia"]["Password"]
        pixivUsername = config["Accounts"]["pixiv"]["User"]
        pixivPassword = config["Accounts"]["pixiv"]["Password"]
        if fantiaEmail == "" or fantiaPassword == "" or pixivUsername == "" or pixivPassword == "":
            raise Exception("Account details had empty values.")
        return fantiaEmail, decrypt_string(fantiaPassword), pixivUsername, decrypt_string(pixivPassword)
    except:
        print(f"{Fore.RED}Error: config.json does not have all the necessary account details.{Fore.RESET}")

        accountsKeyExists = False
        if "Accounts" not in config:
            data = {"Accounts": {
                        "Fantia": {
                            "User": "",
                            "Password": ""
                            },
                        "pixiv": {
                            "User": "",
                            "Password": ""
                            }
                        }
                    }
        else: 
            data = config["Accounts"]
            accountsKeyExists = True

        while True:
            configInput = input("Would you like to enter your account details now? (y/n): ").lower()
            if configInput == "y" or configInput == "n": break
            else: print(f"{Fore.RED}Error: Invalid Input.{Fore.RESET}")
        
        if configInput == "n": 
            print(f"{Fore.RED}Warning: Since you have not added your account details yet, you will not be able to download any images that requires a membership.\nHence, you can add your account details later.{Fore.RESET}")

            if not accountsKeyExists:
                config.update(data)
                with open(jsonPath, "w") as f:
                    json.dump(config, f, indent=4)
            return None, None, None, None
        else:
            print(f"\n{Fore.YELLOW}Adding account details for Fantia...{RESET}")

            fantiaEmail = input("Enter your email address for Fantia: ").lower().strip()
            if accountsKeyExists: data["Fantia"]["User"] = fantiaEmail
            else: data["Accounts"]["Fantia"]["User"] = fantiaEmail
            fantiaPassword = input("Enter your password for Fantia: ")
            if accountsKeyExists: data["Fantia"]["Password"] = encrypt_string(fantiaPassword)
            else: data["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)

            print(f"{Fore.GREEN}Fantia Account successfully added!{RESET}")

            print(f"\n{Fore.YELLOW}Adding account details for pixiv fanbox...{RESET}")

            pixivUsername = input("Enter your username for pixiv: ").strip()
            if accountsKeyExists: data["pixiv"]["User"] = pixivUsername
            else: data["Accounts"]["pixiv"]["User"] = pixivUsername
            pixivPassword = input("Enter your password for pixiv: ")
            if accountsKeyExists: data["pixiv"]["Password"] = encrypt_string(pixivPassword)
            else: data["Accounts"]["pixiv"]["Password"] = encrypt_string(pixivPassword)

            with open(jsonPath, "w") as f:
                if not accountsKeyExists: config.update(data)
                json.dump(config, f, indent=4)

            print(f"{Fore.GREEN}pixiv Account successfully added!{RESET}")
            
            return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword

def change_account_details(typeToChange):
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        if typeToChange == "Fantia":
            print(f"\n{Fore.YELLOW}Changing Fantia Account Details...{RESET}")
            fantiaEmail = input("Enter your new email: ").lower().strip()
            config["Accounts"]["Fantia"]["User"] = fantiaEmail
            fantiaPassword = input("Enter your new password: ")
            config["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)
        elif typeToChange == "pixiv":
            print(f"\n{Fore.YELLOW}Changing pixiv Account Details...{RESET}")
            pixivUsername = input("Enter your new username: ").strip()
            config["Accounts"]["pixiv"]["User"] = pixivUsername
            pixivPassword = input("Enter your new password: ")
            config["Accounts"]["pixiv"]["Password"] = encrypt_string(pixivPassword)
        elif typeToChange == "All":
            print(f"\n{Fore.YELLOW}Changing Fantia Account Details...{RESET}")
            fantiaEmail = input("Enter your new email: ").lower().strip()
            config["Accounts"]["Fantia"]["User"] = fantiaEmail
            fantiaPassword = input("Enter your new password: ")
            config["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)

            print(f"\n{Fore.YELLOW}Changing pixiv Account Details...{RESET}")
            pixivUsername = input("Enter your new username: ").strip()
            config["Accounts"]["pixiv"]["User"] = pixivUsername
            pixivPassword = input("Enter your new password: ")
            config["Accounts"]["pixiv"]["Password"] = encrypt_string(pixivPassword)
        else:
            print(f"{Fore.RED}Unexpected Error: Error when trying to change account details.{Fore.RESET}")
            print(f"{Fore.RED}Please report this error to the developer.{RESET}")
            input("Please enter any key to exit...")
            sys.exit(1)

        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)
    except KeyError:
        print(f"{Fore.RED}Error: Encountered a KeyError when trying to change account details.{Fore.RESET}")
        print(f"{Fore.RED}Please report this error to the developer.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)
    except:
        print(f"{Fore.RED}Unexpected Error: Error when trying to change account details.{Fore.RESET}")
        print(f"{Fore.RED}Please report this error to the developer.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)

def get_driver(browserType):
    if browserType == "chrome":
        #minimise the browser window and hides unnecessary text output
        cOptions = chromeOptions()
        cOptions.add_argument('--headless')
        cOptions.add_argument('--log-level=3')

        # for checking response code
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["loggingPrefs"] = {"performance": "ALL"}

        # auto downloads chromedriver.exe
        gService = chromeService(ChromeDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Chrome(service=gService, options=cOptions, desired_capabilities=capabilities)
    elif browserType == "firefox":
        #minimise the browser window and hides unnecessary text output
        fOptions = firefoxOptions()
        fOptions.add_argument('--headless')
        fOptions.add_argument('--log-level=3')

        # for checking response code
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities["loggingPrefs"] = {"performance": "ALL"}

        # auto downloads geckodriver.exe
        with catch_warnings():
            filterwarnings("ignore", category=DeprecationWarning)
            fService = firefoxService(GeckoDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Firefox(service=fService, options=fOptions, desired_capabilities=capabilities)
    elif browserType == "edge":
        #minimise the browser window and hides unnecessary text output
        eOptions = edgeOptions()
        eOptions.add_argument('--headless')
        eOptions.add_argument('--log-level=3')

        # for checking response code
        capabilities = DesiredCapabilities.EDGE.copy()
        capabilities["loggingPrefs"] = {"performance": "ALL"}

        # auto downloads msedgedriver.exe
        eService = edgeService(EdgeChromiumDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Edge(service=eService, options=eOptions, capabilities=capabilities)
    else:
        print(f"{Fore.RED}Error: Unknown browser type.{Fore.RESET}")
        print(f"{Fore.RED}Please report this error to the developer.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)
    
    return driver

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
        print(f"{Fore.RED}Unexpected Error: Error when trying to check browser config.{Fore.RESET}")
        print(f"{Fore.RED}Please report this error to the developer.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)

def save_browser_config(selectedBrowser):
    with open(jsonPath, "r") as f:
        config = json.load(f)
    config["Browser"] = selectedBrowser
    with open(jsonPath, "w") as f:
        json.dump(config, f, indent=4)
    print(f"{Fore.GREEN}{selectedBrowser.title()} will be automatically loaded next time!{RESET}")

def get_key():
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        key = config["Key"]
        if key == "":
            raise Exception("Key is empty.")
        return key
    except:
        print(f"{Fore.RED}Error: Key is not defined in the config.json file.{Fore.RESET}")

        keyExists = False
        if "Key" in config:
            dataKey = config["Key"]
            keyExists = True
        else: 
            dataKey = {"Key": ""}
            
        key = Fernet.generate_key().decode()

        if keyExists: dataKey = key
        else: dataKey["Key"] = key

        with open(jsonPath, "w") as f:
            if not keyExists: config.update(dataKey)
            json.dump(config, f, indent=4)

        return key

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

def print_progress_bar(prog, totalEl, caption):
    barLength = 20 #size of progress bar
    currentProg = prog / totalEl
    sys.stdout.write("\r")
    sys.stdout.write(f"[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}")
    sys.stdout.flush()

def check_if_directory_has_files(dirPath):
    hasFiles = any(dirPath.iterdir())
    return hasFiles

def login(fantiaEmail, fantiaPassword, pixivUsername, pixivPassword):
    driver.get("https://fantia.jp/sessions/signin")
    driver.find_element(by=By.ID, value="user_email").send_keys(fantiaEmail)
    driver.find_element(by=By.ID, value="user_password").send_keys(fantiaPassword)
    driver.find_element(by=By.XPATH, value="//button[@class='btn btn-primary btn-block mb-10 p-15']").click()

    # checks if the user is authenticated and wait for a max of 10 seconds for the page to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "loggedin"))
        )
    except TimeoutException:
        # if there is no element with a class name of "avatar", it will raise a TimeoutException
        print(f"{Fore.RED}Error: Fantia login failed.{RESET}")
        return False
    except:
        print(f"{Fore.RED}Unexpected Error: Error when trying to login to Fantia.\nPlease report this error to the developer.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)

    driver.get("https://www.fanbox.cc/login")
    driver.find_element(by=By.XPATH, value="//input[@placeholder='E-mail address / pixiv ID']").send_keys(pixivUsername)
    driver.find_element(by=By.XPATH, value="//input[@placeholder='password']").send_keys(pixivPassword)
    driver.find_element(by=By.XPATH, value="//button[@class='signup-fporm__submit']").click()

    # checks if the user is authenticated and wait for a max of 10 seconds for the page to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "csMGsu"))
        )
    except TimeoutException:
        # if there is no element with a class name of "avatar", it will raise a TimeoutException
        print(f"{Fore.RED}Error: pixiv login failed.{RESET}")
        return False
    except:
        print(f"{Fore.RED}Unexpected Error: Error when trying to login to pixiv.\nPlease report this error to the developer.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)
    
    return True

def get_image_name(imageURL, website):
    if website == "Fantia":
        try:
            return imageURL.split("/")[-1].split("?")[0]
        except:
            print(f"{Fore.RED}Error: Unable to retrieve image extension from the image URL.{RESET}")
            input("Please enter any key to exit...")
            sys.exit(1)
    elif website == "pixiv":
        pass

def download(directoryPath, urlInput, website):
    driver.get(urlInput)
    if website == "FantiaImageURL":
        image = driver.find_element(by=By.TAG_NAME, value="img")
        imageSrc = image.get_attribute("src")
        imagePath = directoryPath.joinpath(get_image_name(imageSrc, "Fantia"))
        with requests.get(imageSrc, stream=True) as r:
            with open(imagePath, "wb") as f:
                shutil.copyfileobj(r.raw, f)
    elif website == "FantiaPost":
        images = driver.find_element(by=By.CLASS_NAME, value="fantiaImage")
        for image in images:
            imageSrc = image.get_attribute("href")
            imagePath = directoryPath.joinpath(get_image_name(imageSrc, "Fantia"))
            with requests.get(imageSrc, stream=True) as r:
                with open(imagePath, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
    elif website == "pixiv":
        pass

def main():
    # menu
    menuEn = f"""
---------------------- {Fore.YELLOW}Download Options{RESET} ----------------------
      {Fore.GREEN}1. Download images from Fantia using an image URL{RESET}
      {Fore.GREEN}2. Download images from a Fantia post URL{RESET}
      {Fore.CYAN}3. Download images from a pixiv fanbox post URL{RESET}
      {Fore.RED}X. Shutdown the program{RESET}
 """
    menuJp = f"""
---------------------- {Fore.YELLOW}ダウンロードのオプション{RESET} ----------------------
      {Fore.GREEN}1. 画像URLでFantiaから画像をダウンロード{RESET}
      {Fore.GREEN}2. Fantia投稿URLから画像をダウンロードする{RESET}
      {Fore.CYAN}3. pixivファンボックスの投稿URLから画像をダウンロードする{RESET}
      {Fore.RED}X. プログラムを終了する{RESET}
"""
    menu = menuEn if lang == "en" else menuJp
    while True:
        print(menu)
        cmdInput = input("Enter command: ").upper()
        if cmdInput == "1":
            while True:
                foldername = input("Enter the name of the folder you want to save the images (X to cancel): ")
                if foldername.upper() == "X": break
                
                # main folder
                directoryPath = pathlib.Path(__file__).resolve().parent.joinpath("downloads")
                if not directoryPath.is_dir():
                    directoryPath.mkdir(parents=True)

                # subfolder
                directoryPath = directoryPath.joinpath(foldername)
                if not directoryPath.is_dir():
                    directoryPath.mkdir(parents=True)

                if check_if_directory_has_files(directoryPath): print(f"{Fore.RED}Error: Folder already exists with images inside.\nPlease enter a different NEW name for a new folder.{RESET}")
                else: break

            urlInput = input("Enter the URL of the first image: ")
            imageCounter = 1
            print(f"{Fore.YELLOW}Downloading images...{RESET}")

            urlArray = []
            while True:
                driver.get(urlInput)
                logs = driver.get_log("performance")
                if get_status(logs) != 200: break

                imageCounter += 1
                urlArray.append(urlInput)

                # increment the urlInput by one to retrieve the next image
                spiltURL = url.split("/")
                urlNumString = spiltURL[-1]
                urlNum = str(int(urlNumString) + 1)
                urlInput = "/".join(spiltURL[0:-1]) + urlNum

            if imageCounter != 1:
                progress = 1
                totalImages = len(urlArray)
                for url in urlArray:
                    download(directoryPath, url, "FantiaImageURL")
                    print_progress_bar(progress, totalImages, f"{Fore.YELLOW}Downloading image no.{progress} out of {totalImages}{RESET}")
                    sleep(0.1)
                    progress += 1

                print(f"{Fore.GREEN}All {imageCounter} images downloaded successfully!{RESET}")
            else: print(f"{Fore.RED}Error: No images to download.{RESET}")
        elif cmdInput == "2":
            pass
        elif cmdInput == "3":
            while True:
                foldername = input("Enter the name of the folder you want to save the images: ")
                pathtodownload = str(pathlib.Path(__file__).resolve().parent)
                
                directoryPath = pathlib.Path(pathtodownload).joinpath("downloaded_images", foldername)
                directoryPath.mkdir(parents=True, exist_ok=True)

                if check_if_directory_has_files(directoryPath): print(f"{Fore.RED}Error: Folder already exists with images inside.{RESET}\n{Fore.GREEN}Please enter a different NEW name for a new folder.{RESET}")
                else: break

        elif cmdInput == "X": break
        else: print(f"{Fore.RED}Invalid input. Please try again.{RESET}")

if __name__ == "__main__":
    global RESET
    RESET = Style.RESET_ALL

    print(f"{Fore.YELLOW}Running program...{RESET}")

    global jsonPath
    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "config.json")

    pythonMainVer = sys.version_info[0]
    pythonSubVer = sys.version_info[1]
    if pythonMainVer < 3 or pythonSubVer < 8:
        print(f"{Fore.RED}Fatal Error: This program requires running Python 3.8 or higher!\nYou are running Python " + str(pythonMainVer) + "." + str(pythonSubVer) + f"{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)
    
    # checks if config.json exists and the necessary configs are defined
    check_if_json_file_exists()

    # generate a key for the encryption of passwords so that it won't be stored in plaintext
    global decKey
    try: decKey = Fernet(get_key())
    except:
        print(f"{Fore.RED}Fatal Error: Unable to retrieve key for decryption.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)

    # get the preferred browser
    loadBrowser = check_browser_config()
    if loadBrowser == None:
        browserSet = {"chrome", "firefox", "edge"}
        while True:
            print(f"{Fore.YELLOW}What browser would you like to use?{RESET}")
            print(f"{Fore.YELLOW}Available browsers: Chrome, Firefox, Edge.{RESET}")
            selectedBrowser = input("\nEnter a browser to use from above: ").lower()
            if selectedBrowser in browserSet: break
            else: print(f"{Fore.RED}Invalid browser. Please enter a browser from the available browsers.{RESET}")

        global driver
        driver = get_driver(selectedBrowser)

        while True:
            saveBrowser = input("Would you like to automatically use this browser upon running this program again? (y/n): ").lower()
            if saveBrowser == "y" or saveBrowser == "n": break
            else: print(f"{Fore.RED}Invalid input. Please enter y or n.{RESET}")
        
        if saveBrowser == "y":
            save_browser_config(selectedBrowser)
            
    # gets account details for Fantia and pixiv for downloading images that requires a membership
    try: fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account()
    except:
        print(f"{Fore.RED}Fatal Error: Unable to retrieve user accounts for Fantia and pixiv Fanbox.{RESET}")
        input("Please enter any key to exit...")
        sys.exit(1)

    global lang
    while True:
        lang = input("Select a language/言語を選択してください (en/jp): ").lower()
        if lang == "en" or lang == "jp": break
        else: print(f"{Fore.RED}Error: Invalid language prefix entered.{RESET}")

    print(f"{Fore.YELLOW}Logging in to Fantia and Pixiv...{RESET}")
    # logging into fantia and pixiv
    if fantiaEmail != None and fantiaPassword != None and pixivUsername != None and pixivPassword != None:
        loginSuccess = login(fantiaEmail, fantiaPassword, pixivUsername, pixivPassword)
        if loginSuccess:
            print(f"{Fore.GREEN}Logins successful!{RESET}")
        else:
            change_account_details("All")

    main()
    print(f"{Fore.RED}Program terminated.{RESET}")
    print(f"{Fore.YELLOW}Thank you for using Cultured Downloader.{RESET}")
    input("Please enter any key to exit...")
    driver.close()
    sys.exit(0)