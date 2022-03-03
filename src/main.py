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
from Colour_Settings import TerminalColours as S
from time import sleep
from cryptography.fernet import Fernet
import requests, pathlib, json, sys, shutil

"""Config Codes"""

def check_if_json_file_exists():
    jsonFolderPath = pathlib.Path(__file__).resolve().parent.joinpath("configs")
    if not jsonFolderPath.is_dir(): jsonFolderPath.mkdir(parents=True)
    if not jsonPath.is_file():
        print(f"{S.RED}Error: config.json does not exist.{END}")
        print(f"{S.YELLOW}Creating config.json file...{END}")
        with open(jsonPath, "w") as f:
            json.dump({}, f)
    else: print(f"{S.GREEN}Loading configurations from config.json...{END}")

def encrypt_string(inputString):
    return decKey.encrypt(inputString.encode()).decode()

def decrypt_string(inputString):
    try:
        return decKey.decrypt(inputString.encode()).decode()
    except:
        print(f"{S.RED}Fatal Error: Could not decrypt string.{END}")
        print(f"{S.RED}Resetting Key and encrypted values in config.json...{END}")
        with open(jsonPath, "r") as f:
            config = json.load(f)
        config["Key"] = ""
        config["Accounts"]["Fantia"]["Password"] = ""
        config["Accounts"]["Pixiv"]["Password"] = ""
        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)
        print(f"{S.RED}Please restart the program.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)

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
        print(f"{S.RED}Error: config.json does not have all the necessary account details.{END}")

        accountsKeyExists = False
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
        else: 
            data = config["Accounts"]
            accountsKeyExists = True

        while True:
            configInput = input("Would you like to save your account details now? (y/n): ").lower()
            if configInput == "y" or configInput == "n": break
            else: print(f"{S.RED}Error: Invalid Input.{END}")
        
        if configInput == "n": 
            print(f"{S.RED}Warning: Since you have not added your account details yet,\nyou will not be able to download any images that requires a membership.\nFret not, you can add your account details later.{END}")

            if not accountsKeyExists:
                config.update(data)
                with open(jsonPath, "w") as f:
                    json.dump(config, f, indent=4)
            return None, None, None, None
        else:
            print(f"\n{S.YELLOW}Adding account details for Fantia...{END}")

            fantiaEmail = input("Enter your email address for Fantia: ").lower().strip()
            if accountsKeyExists: data["Fantia"]["User"] = fantiaEmail
            else: data["Accounts"]["Fantia"]["User"] = fantiaEmail
            fantiaPassword = input("Enter your password for Fantia: ")
            if accountsKeyExists: data["Fantia"]["Password"] = encrypt_string(fantiaPassword)
            else: data["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)

            print(f"{S.GREEN}Fantia Account successfully added!{END}")

            print(f"\n{S.YELLOW}Adding account details for Pixiv fanbox...{END}")

            pixivUsername = input("Enter your username for Pixiv: ").strip()
            if accountsKeyExists: data["Pixiv"]["User"] = pixivUsername
            else: data["Accounts"]["Pixiv"]["User"] = pixivUsername
            pixivPassword = input("Enter your password for Pixiv: ")
            if accountsKeyExists: data["Pixiv"]["Password"] = encrypt_string(pixivPassword)
            else: data["Accounts"]["Pixiv"]["Password"] = encrypt_string(pixivPassword)

            with open(jsonPath, "w") as f:
                if not accountsKeyExists: config.update(data)
                json.dump(config, f, indent=4)

            print(f"{S.GREEN}Pixiv Account successfully added!{END}")
            
            return fantiaEmail, fantiaPassword, pixivUsername, pixivPassword

def change_account_details(typeToChange):
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        if typeToChange == "Fantia":
            print(f"\n{S.YELLOW}Changing Fantia Account Details...{END}")
            fantiaEmail = input("Enter your new email (X to cancel): ").lower().strip()
            if fantiaEmail.upper() != "X": config["Accounts"]["Fantia"]["User"] = fantiaEmail

            fantiaPassword = input("Enter your new password (X to cancel): ")
            if fantiaPassword.upper() != "X": config["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)
        elif typeToChange == "Pixiv":
            print(f"\n{S.YELLOW}Changing Pixiv Account Details...{END}")
            pixivUsername = input("Enter your new username (X to cancel): ").strip()
            if pixivUsername.upper() != "X": config["Accounts"]["Pixiv"]["User"] = pixivUsername

            pixivPassword = input("Enter your new password (X to cancel): ")
            if pixivPassword.upper() != "X": config["Accounts"]["Pixiv"]["Password"] = encrypt_string(pixivPassword)
        elif typeToChange == "All":
            print(f"\n{S.YELLOW}Changing Fantia Account Details...{END}")

            fantiaEmail = input("Enter your new email (X to cancel): ").lower().strip()
            if fantiaEmail.upper() != "X": config["Accounts"]["Fantia"]["User"] = fantiaEmail
            
            fantiaPassword = input("Enter your new password (X to cancel): ")
            if pixivPassword.upper() != "X": config["Accounts"]["Fantia"]["Password"] = encrypt_string(fantiaPassword)

            print(f"\n{S.YELLOW}Changing Pixiv Account Details...{END}")

            pixivUsername = input("Enter your new username (X to cancel): ").strip()
            if pixivUsername.upper() != "X": config["Accounts"]["Pixiv"]["User"] = pixivUsername

            pixivPassword = input("Enter your new password (X to cancel): ")
            if pixivPassword.upper() != "X": config["Accounts"]["Pixiv"]["Password"] = encrypt_string(pixivPassword)
        else:
            print(f"{S.RED}Unexpected Error: Error when trying to change account details.{END}")
            print(f"{S.RED}Please report this error to the developer.{END}")
            input("Please enter any key to exit...")
            sys.exit(1)

        with open(jsonPath, "w") as f:
            json.dump(config, f, indent=4)

    except KeyError:
        print(f"{S.RED}Error: Encountered a KeyError when trying to change account details.{END}")
        print(f"{S.RED}Please report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)
    except:
        print(f"{S.RED}Unexpected Error: Error when trying to change account details.{END}")
        print(f"{S.RED}Please report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)

def get_driver(browserType):
    if browserType == "chrome":
        #minimise the browser window and hides unnecessary text output
        cOptions = chromeOptions()
        cOptions.headless = True
        cOptions.add_argument('--log-level=3')

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
        eOptions.headless = True
        eOptions.add_argument('--log-level=3')

        # for checking response code
        capabilities = DesiredCapabilities.EDGE.copy()
        capabilities["loggingPrefs"] = {"performance": "ALL"}

        # auto downloads msedgedriver.exe
        eService = edgeService(EdgeChromiumDriverManager(log_level=0, print_first_line=False).install())

        # start webdriver
        driver = webdriver.Edge(service=eService, options=eOptions, capabilities=capabilities)
    else:
        print(f"{S.RED}Error: Unknown browser type.{END}")
        print(f"{S.RED}Please report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)
    
    return driver

def get_user_browser_preference():
    browserSet = {"chrome", "firefox", "edge"}
    while True:
        print(f"{S.YELLOW}What browser would you like to use?{END}")
        print(f"{S.YELLOW}Available browsers: Chrome, Firefox, Edge.{END}")
        selectedBrowser = input("\nEnter a browser to use from above: ").lower()
        if selectedBrowser in browserSet: break
        else: print(f"{S.RED}Invalid browser. Please enter a browser from the available browsers.{END}")
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
        print(f"{S.RED}Unexpected Error: Error when trying to check browser config.{END}")
        print(f"{S.RED}Please report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)

def save_browser_config(selectedBrowser):
    with open(jsonPath, "r") as f:
        config = json.load(f)
    config["Browser"] = selectedBrowser
    with open(jsonPath, "w") as f:
        json.dump(config, f, indent=4)
    print(f"{S.GREEN}{selectedBrowser.title()} will be automatically loaded next time!{END}")

def get_key():
    with open(jsonPath, "r") as f:
        config = json.load(f)
    try:
        key = config["Key"]
        if key == "":
            raise Exception("Key is empty.")
        return key
    except:
        print(f"{S.RED}Error: Key is not defined in the config.json file.{END}")

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
    sys.stdout.write(f"{S.YELLOW}[{'=' * int(barLength * currentProg):{barLength}s}] {int(100 * currentProg)}% {caption}{END}")
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
        print(f"{S.GREEN}Successfully logged in to Fantia!{END}")
    except TimeoutException:
        # if there is no element with a class name of "avatar", it will raise a TimeoutException
        print(f"{S.RED}Error: Fantia login failed.{END}")
        return False
    except:
        print(f"{S.RED}Unexpected Error: Error when trying to login to Fantia.\nPlease report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)

    driver.get("https://www.fanbox.cc/login")
    driver.find_element(by=By.XPATH, value="//input[@placeholder='E-mail address / pixiv ID']").send_keys(pixivUsername)
    driver.find_element(by=By.XPATH, value="//input[@placeholder='password']").send_keys(pixivPassword)
    driver.find_element(by=By.XPATH, value="//button[@class='signup-form__submit']").click()

    # checks if the user is authenticated and wait for a max of 10 seconds for the page to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/creators/supporting' and @class='sc-1mdohqc-0 ilARNI']"))
        )
        print(f"{S.GREEN}Successfully logged in to Pixiv!{END}")
    except TimeoutException:
        # if there is no element with a class name of "avatar", it will raise a TimeoutException
        print(f"{S.RED}Error: Pixiv login failed.{END}")
        return False
    except:
        print(f"{S.RED}Unexpected Error: Error when trying to login to Pixiv.\nPlease report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)
    
    return True

def get_image_name(imageURL, website):
    if website == "Fantia":
        try: return imageURL.split("/")[-1].split("?")[0]
        except:
            print(f"{S.RED}Error: Unable to retrieve image name from the image URL.{END}")
            print(f"{S.RED}Please report this error to the developer.{END}")
            input("Please enter any key to exit...")
            sys.exit(1)
    elif website == "Pixiv":
        try: return imageURL.split("/")[-1]
        except:
            print(f"{S.RED}Error: Unable to retrieve image name from the image URL.{END}")
            print(f"{S.RED}Please report this error to the developer.{END}")
            input("Please enter any key to exit...")
            sys.exit(1)
    else:
        print(f"{S.RED}Error: Unknown website.{END}")
        print(f"{S.RED}Please report this error to the developer.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)

def get_pixiv_image_full_res_url(imageURL):
    urlArray = []
    for urlParts in imageURL.split("/"):
        if urlParts == "w" or urlParts == "1200": pass
        else: urlArray.append(urlParts)
    return "/".join(urlArray)

def save_image(imageURL, pathToSave):
    with requests.get(imageURL, stream=True) as r:
        with open(pathToSave, "wb") as f:
            shutil.copyfileobj(r.raw, f)

def download(urlInput, website, subFolderPath):
    driver.get(urlInput)
    if website == "FantiaImageURL":
        image = driver.find_element(by=By.TAG_NAME, value="img")
        imageSrc = image.get_attribute("src")
        imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Fantia"))
        save_image(imageSrc, imagePath)
    elif website == "FantiaPost":
        imagePosts = driver.find_elements(by=By.CLASS_NAME, value="fantiaImage")
        for imagePost in imagePosts:
            imageHREFLink = imagePost.get_attribute("href")
            driver.get(imageHREFLink)
            image = driver.find_element(by=By.TAG_NAME, value="img")
            imageSrc = image.get_attribute("src")
            imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Fantia"))
            save_image(imageSrc, imagePath)
    elif website == "Pixiv":
        images = driver.find_elements(by=By.XPATH, value="//img[@class='sc-14k46gk-1']")
        for image in images:
            imageSrc = get_pixiv_image_full_res_url(image.get_attribute("src"))
            imagePath = subFolderPath.joinpath(get_image_name(imageSrc, "Pixiv"))
            save_image(imageSrc, imagePath)

def create_subfolder():
    while True:
        foldername = input("Enter the name of the folder you want to save the images (X to cancel): ")
        if foldername.upper() == "X": return "X"
        
        # main download folder
        if not directoryPath.is_dir():
            directoryPath.mkdir(parents=True)

        # subfolder
        imagePath = directoryPath.joinpath(foldername)
        if not imagePath.is_dir():
            imagePath.mkdir(parents=True)

        if check_if_directory_has_files(imagePath): print(f"{S.RED}Error: Folder already exists with images inside.\nPlease enter a different NEW name for a new folder.{END}")
        else: return imagePath

def main():
    menuEn = f"""
---------------------- {S.YELLOW}Download Options{END} ----------------------
      {S.GREEN}1. Download images from Fantia using an image URL{END}
      {S.GREEN}2. Download images from a Fantia post URL{END}
      {S.CYAN}3. Download images from a Pixiv Fanbox post URL{END}

---------------------- {S.YELLOW}Config Options{END} ----------------------
      {S.LIGHT_BLUE}4. Update Account Details{END}
      {S.LIGHT_BLUE}5. Change Default Browser{END}
      {S.RED}X. Shutdown the program{END}
 """
    menuJp = f"""
---------------------- {S.YELLOW}ダウンロードのオプション{END} ----------------------
      {S.GREEN}1. 画像URLでFantiaから画像をダウンロードする{END}
      {S.GREEN}2. Fantia投稿URLから画像をダウンロードする{END}
      {S.CYAN}3. Pixivファンボックスの投稿URLから画像をダウンロードする{END}

---------------------- {S.YELLOW}コンフィグのオプション{END} ----------------------
      {S.LIGHT_BLUE}4. アカウント情報を更新する{END}
      {S.LIGHT_BLUE}5. ブラウザを変更する{END}
      {S.RED}X. プログラムを終了する{END}
"""
    menu = menuEn if lang == "en" else menuJp
    while True:
        print(menu)
        cmdInput = input("Enter command: ").upper()
        if cmdInput == "1":
            imagePath = create_subfolder()
            if imagePath != "X":
                # imagesNum = int(input("Enter number of images to download: "))
                urlInput = input("Enter the URL of the first image: ")
                imageCounter = 1
                print(f"{S.YELLOW}Downloading images...{END}")

                urlArray = []
                # for i in range(imagesNum):
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
                        print_progress_bar(progress, totalImages, f"{S.YELLOW}Downloading image no.{progress} out of {totalImages}{END}")
                        sleep(0.1)
                        progress += 1

                    print(f"\n{S.GREEN}All {imageCounter - 1} images downloaded successfully!{END}")
                else: print(f"{S.RED}Error: No images to download.{END}")
        elif cmdInput == "2":
            imagePath = create_subfolder()
            if imagePath != "X":
                urlInput = input("Enter the URL of the first image: ")
                imageCounter = 1
                print(f"{S.YELLOW}Downloading images...{END}")

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
                        download(url, "FantiaImageURL", imagePath)
                        print_progress_bar(progress, totalImages, f"{S.YELLOW}Downloading image no.{progress} out of {totalImages}{END}")
                        sleep(0.1)
                        progress += 1

                    print(f"{S.GREEN}All {imageCounter - 1} images downloaded successfully!{END}")
                else: print(f"{S.RED}Error: No images to download.{END}")
        elif cmdInput == "3":
            imagePath = create_subfolder()
        elif cmdInput == "4":
            imagePath = create_subfolder()
        elif cmdInput == "5":
            defaultBrowser = check_browser_config()
            if defaultBrowser != None:
                newDefaultBrowser = get_user_browser_preference()
                save_browser_config(newDefaultBrowser)
            else:
                print(f"{S.RED}Error: No default browser found.{END}")
                while True:
                    saveBrowser = input("Would you like to save a browser as your default browser for this program? (y/n): ").lower()
                    if saveBrowser == "y" or saveBrowser == "n": break
                    else: print(f"{S.RED}Invalid input. Please enter y or n.{END}")
                
                if saveBrowser == "y":
                    newDefaultBrowser = get_user_browser_preference()
                    save_browser_config(newDefaultBrowser)

        elif cmdInput == "X": break
        else: print(f"{S.RED}Invalid input. Please try again.{END}")

if __name__ == "__main__":
    # declare global variables
    global END
    global jsonPath
    global directoryPath
    global decKey
    global driver
    global lang

    END = S.RESET
    print(f"{S.YELLOW}Running program...{END}")
    
    jsonPath = pathlib.Path(__file__).resolve().parent.joinpath("configs", "config.json")
    
    directoryPath = pathlib.Path(__file__).resolve().parent.joinpath("downloads")

    pythonMainVer = sys.version_info[0]
    pythonSubVer = sys.version_info[1]
    if pythonMainVer < 3 or pythonSubVer < 8:
        print(f"{S.RED}Fatal Error: This program requires running Python 3.8 or higher!\nYou are running Python " + str(pythonMainVer) + "." + str(pythonSubVer) + f"{END}")
        input("Please enter any key to exit...")
        sys.exit(1)
    
    # checks if config.json exists and the necessary configs are defined
    check_if_json_file_exists()

    # generate a key for the encryption of passwords so that it won't be stored in plaintext
    try: decKey = Fernet(get_key())
    except:
        print(f"{S.RED}Fatal Error: Unable to retrieve key for decryption.{END}")
        input("Please enter any key to exit...")
        sys.exit(1)

    # get the preferred browser
    loadBrowser = check_browser_config()
    if loadBrowser == None:
        selectedBrowser = get_user_browser_preference()

        driver = get_driver(selectedBrowser)

        while True:
            saveBrowser = input("Would you like to automatically use this browser upon running this program again? (y/n): ").lower()
            if saveBrowser == "y" or saveBrowser == "n": break
            else: print(f"{S.RED}Invalid input. Please enter y or n.{END}")
        
        if saveBrowser == "y":
            save_browser_config(selectedBrowser)
    else: driver = get_driver(loadBrowser)
            
    while True:
        lang = input("Select a language/言語を選択してください (en/jp): ").lower()
        if lang == "en" or lang == "jp": break
        else: print(f"{S.RED}Error: Invalid language prefix entered.{END}")
    
    # logging into Fantia and Pixiv
    print(f"{S.YELLOW}Logging in to Fantia and Pixiv...{END}")
    while True:
        # gets account details for Fantia and Pixiv for downloading images that requires a membership
        try: fantiaEmail, fantiaPassword, pixivUsername, pixivPassword = get_user_account()
        except:
            print(f"{S.RED}Fatal Error: Unable to retrieve user accounts for Fantia and Pixiv Fanbox.{END}")
            input("Please enter any key to exit...")
            sys.exit(1)

        if fantiaEmail == None and fantiaPassword == None and pixivUsername == None and pixivPassword == None: break

        loginSuccess = login(fantiaEmail, fantiaPassword, pixivUsername, pixivPassword)
        if loginSuccess:
            print(f"{S.GREEN}Logins were successful!{END}")
            break
        else:
            while True:
                continueLoggingIn = input("Would you like to retry or change your account details and login again? (y/n/retry): ").lower()
                if continueLoggingIn == "y" or continueLoggingIn == "n" or continueLoggingIn == "retry": break
                else: print(f"{S.RED}Error: Invalid input. Please enter y or n.{END}")

            if continueLoggingIn == "y": change_account_details("All")
            elif continueLoggingIn == "retry": continue
            else:
                print(f"{S.YELLOW}Ignoring login errors...{END}")
                print(f"{S.RED}Warning: Since you might have not logged in to both Fantia and Pixiv,\nyou will not be able to download any images that requires a membership.{END}")
                break

    main()
    print(f"{S.YELLOW}Thank you for using Cultured Downloader.{END}")
    input("Please enter any key to exit...")
    driver.close()
    sys.exit(0)