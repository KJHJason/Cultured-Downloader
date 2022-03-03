import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pathlib, json, sys, shutil
from colorama import Fore, Style
from time import sleep
from cryptography.fernet import Fernet

# function below from https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code
def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass

def print_progress_bar(prog, totalEl, caption):
    barLength =20 #size of progress bar
    currentProg = prog / totalEl
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}")
    sys.stdout.flush()

def check_if_directory_has_files(dirPath):
    hasFiles = any(dirPath.iterdir())
    return hasFiles

def login(website, user, password):
    if website == "Fantia":
        driver.get("https://fantia.jp/sessions/signin")
        driver.find_element(by=By.ID, value="user_email").send_keys(user)
        driver.find_element(by=By.ID, value="user_password").send_keys(password)
        driver.find_element(by=By.XPATH, value="//button[@class='btn btn-primary btn-block mb-10 p-15']").click()
    elif website == "pixiv":
        driver.get("https://www.fanbox.cc/login")
        driver.find_element(by=By.XPATH, value="//input[@placeholder='E-mail address / pixiv ID']").send_keys(user)
        driver.find_element(by=By.XPATH, value="//input[@placeholder='password']").send_keys(password)
        driver.find_element(by=By.XPATH, value="//button[@class='signup-form__submit']").click()

def get_image_name(imageURL, website):
    if website == "Fantia":
        try:
            return imageURL.split("/")[-1].split("?")[0]
        except:
            print(f"{Fore.RED}Error: Unable to retrieve image extension from the image URL.{RESET}")
            sys.exit(1)
    elif website == "pixiv":
        pass

def download(directoryPath, urlInput, website):
    if website == "Fantia":
        driver.get(urlInput)
        image = driver.find_element(by=By.TAG_NAME, value="img")
        imageSrc = image.get_attribute('src')
        imagePath = directoryPath.joinpath(get_image_name(imageSrc, "Fantia"))
        with requests.get(imageSrc, stream=True) as r:
            with open(imagePath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    elif website == "pixiv":
        pass

def check_if_json_file_exists():
    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs")
    if not jsonPath.is_dir(): jsonPath.mkdir(parents=True)
    jsonPath = jsonPath.joinpath("config.json")
    if not jsonPath.is_file():
        print(f"{Fore.RED}Error: config.json does not exist.{Fore.RESET}")
        print(f"{Fore.YELLOW}Creating config.json file...{Fore.RESET}")
        with open(jsonPath, "w") as f:
            json.dump({}, f)
    else: print(f"{Fore.GREEN}Loading configurations from config.json...{RESET}")

def encrypt_string(inputString):
    return decKey.encrypt(inputString.encode()).decode()

def decrypt_string(inputString):
    return decKey.decrypt(inputString.encode()).decode()

def get_user_account():
    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "config.json")
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
            print("\nAdding account details for Fantia...")

            fantiaEmail = input("Enter your email address for Fantia: ").strip()
            if accountsKeyExists: data["Fantia"]["User"] = fantiaEmail
            else: data["Accounts"]["Fantia"]["User"] = fantiaEmail
            fantiaPassword = input("Enter your password for Fantia: ")
            if accountsKeyExists: data["Fantia"]["Password"] = encrypt_string(fantiaPassword)
            else: data["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)

            print(f"{Fore.GREEN}Fantia Account successfully added!{RESET}")

            print("\nAdding account details for pixiv fanbox...")

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

def get_chrome_driver_path():
    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "config.json")
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        chromeDriverPath = config["ChromeDriverPath"].strip()
        if chromeDriverPath == "":
            raise Exception("ChromeDriverPath is empty.")
        return chromeDriverPath
    except:
        print(f"{Fore.RED}Error: ChromeDriverPath is not defined in the config.json file.{Fore.RESET}")
        if "ChromeDriverPath" not in config:
            dataPath = {"ChromeDriverPath": ""}
        else: dataPath = config["ChromeDriverPath"]

        while True:
            userInputPath = input(f"Enter the {Fore.RED}FULL path{RESET} to your ChromeDriver.exe: ")

            correctEXE = False
            if "\\" in userInputPath:
                if userInputPath.split("\\")[-1] == "chromedriver.exe":
                    correctEXE = True
            elif "/" in userInputPath:
                if userInputPath.split("/")[-1] == "chromedriver.exe":
                    correctEXE = True

            if correctEXE:
                if pathlib.Path(userInputPath).is_file():
                    dataPath["ChromeDriverPath"] = userInputPath
                    config.update(dataPath)
                    with open(jsonPath, "w") as f:
                        json.dump(config, f, indent=4)
                    return userInputPath
                else: print(f"{Fore.RED}Error: ChromeDriver.exe does not exist in the path.{Fore.RESET}")
            else: print(f"{Fore.RED}Error: ChromeDriver.exe does not exist in the path.{Fore.RESET}")

def get_key():
    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "config.json")
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
                foldername = input("Enter the name of the folder you want to save the images: ")
                
                # main folder
                directoryPath = pathlib.Path(__file__).resolve().parent.joinpath("downloads")
                if not directoryPath.is_dir():
                    directoryPath.mkdir(parents=True)

                # subfolder
                directoryPath = directoryPath.joinpath(foldername)
                if not directoryPath.is_dir():
                    directoryPath.mkdir(parents=True)

                if check_if_directory_has_files(directoryPath): print(f"{Fore.RED}Error: Folder already exists with images inside.{RESET}\n{Fore.GREEN}Please enter a different NEW name for a new folder.{RESET}")
                else: break

            if fantiaEmail != None and fantiaPassword != None:
                login("Fantia", fantiaEmail, fantiaPassword)

            urlInput = input("Enter the URL of the first image: ")
            imageCounter = 1
            print("Downloading images...")

            urlArray = []
            while True:
                driver.get(urlInput)
                logs = driver.get_log('performance')
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
                    download(directoryPath, url, "Fantia")
                    print_progress_bar(progress, totalImages, f"{Fore.GREEN}Downloading image no.{progress} out of {totalImages}{RESET}")
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
            
            if pixivUsername != None and pixivPassword != None:
                login("pixiv", pixivUsername, pixivPassword)

        elif cmdInput == "X": break
        else: print("Invalid input. Please try again.")

if __name__ == "__main__":
    print("Running program...")
    # to hide logs
    """
    log-level: 
    Sets the minimum log level.
    Valid values are from 0 to 3: 

        INFO = 0, 
        WARNING = 1, 
        LOG_ERROR = 2, 
        LOG_FATAL = 3.

    default is 0.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    
    # for checking response code
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    # additional configs
    global RESET
    RESET = Style.RESET_ALL

    # checks if config.json exists and the necessary configs are defined
    check_if_json_file_exists()

    # generate a key for the encryption of passwords so that it won't be stored in plaintext
    global decKey
    try: decKey = Fernet(get_key())
    except:
        print(f"{Fore.RED}Fatal Error: Unable to retrieve key for decryption.{RESET}")
        sys.exit(1)

    # run Install_Chrome_Driver.py if you do not have chromedriver.exe downloaded
    gService = Service(get_chrome_driver_path())

    global fantiaEmail
    global fantiaPassword
    global pixivUsername
    global pixivPassword
    try: fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account()
    except:
        print(f"{Fore.RED}Fatal Error: Unable to retrieve user accounts for Fantia and pixiv Fanbox.{RESET}")
        sys.exit(1)

    # start webdriver
    global driver
    driver = webdriver.Chrome(service=gService, options=chrome_options, desired_capabilities=capabilities)

    global lang
    while True:
        lang = input("Select a language/言語を選択してください (en/jp): ").lower()
        if lang == "en" or lang == "jp": break
        else: print(f"{Fore.RED}Error: Invalid language prefix entered.{RESET}")

    main()
    print(f"{Fore.RED}Program terminated.{RESET}")
    print(f"{Fore.YELLOW}Thank you for using Cultured Downloader.{RESET}")
    driver.close()