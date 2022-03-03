import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pathlib, json, sys, shutil
from colorama import Fore, Style
from time import sleep

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

def check_user_account():
    jsonPath = pathlib.Path.cwd().joinpath("configs", "config.json")
    if jsonPath.is_file():
        with open(jsonPath, "r") as f:
            config = json.load(f)
        return config["Accounts"]
    else:
        print(f"{Fore.RED}Error: config.json not found{Fore.RESET}")
        print(f"Creating config.json file...")
        data = {
            "Accounts": {
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
        with open(jsonPath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"{Fore.GREEN}config.json created{Fore.RESET}")

        while True:
            configInput = input("Would you like to enter your account details now? (y/n): ").lower()
            if configInput != "y" or configInput != "n": print(f"{Fore.RED}Error: Invalid Input.{Fore.RESET}")
            else: break
        
        if configInput == "n": print(f"{Fore.RED}Warning: Since you have not added your account details yet, you will not be able to download any paid images.\nHence, {Fore.RESET}")
        else: pass
            
            
def main():
    while True:
        if lang == "en": print(menuEn)
        elif lang == "jp": print(menuJp)
        cmdInput = input("Enter command: ")
        if cmdInput == "1":
            while True:
                foldername = input("Enter the name of the folder you want to save the images: ")
                
                # main folder
                directoryPath = pathlib.Path.cwd().joinpath("downloads")
                if not directoryPath.isdir():
                    directoryPath.mkdir(parents=True)

                # subfolder
                directoryPath = directoryPath.joinpath(foldername)
                if not directoryPath.isdir():
                    directoryPath.mkdir(parents=True)

                if check_if_directory_has_files(directoryPath): print(f"{Fore.RED}Error: Folder already exists with images inside.{RESET}\n{Fore.GREEN}Please enter a different NEW name for a new folder.{RESET}")
                else: break

            login("Fantia", email, password)

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

            progress = 1
            totalImages = len(urlArray)
            for url in urlArray:
                download(directoryPath, url, "Fantia")
                print_progress_bar(progress, totalImages, f"{Fore.GREEN}Downloading image no.{progress} out of {totalImages}{RESET}")
                sleep(0.1)
                progress += 1

            print(f"{Fore.GREEN}All {imageCounter} images downloaded successfully!{RESET}")
        elif cmdInput == "2":
            pass
        elif cmdInput == "3":
            while True:
                foldername = input("Enter the name of the folder you want to save the images: ")
                pathtodownload = str(pathlib.Path.cwd())
                
                directoryPath = pathlib.Path(pathtodownload).joinpath("downloaded_images", foldername)
                directoryPath.mkdir(parents=True, exist_ok=True)

                if check_if_directory_has_files(directoryPath): print(f"{Fore.RED}Error: Folder already exists with images inside.{RESET}\n{Fore.GREEN}Please enter a different NEW name for a new folder.{RESET}")
                else: break
            
            login("pixiv", username, password)
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

    # change location of chromedriver, if not downloaded, run Install_Chrome_Driver.py and paste the url here
    gService = Service(r"C:\Users\Admin\.wdm\drivers\chromedriver\win32\98.0.4758.102\chromedriver.exe")

    # start webdriver
    driver = webdriver.Chrome(service=gService, options=chrome_options, desired_capabilities=capabilities)

    # additional configs
    RESET = Style.RESET_ALL
    menuEn = f"""
---------------------- {Fore.YELLOW}Download Options{RESET} ----------------------
      {Fore.GREEN}1. Download images from Fantia using an image URL{RESET}
      {Fore.GREEN}2. Download images from a Fantia post URL{RESET}
      {Fore.CYAN}3. Download images from a pixiv fanbox post URL{RESET}
 """
    menuJp = f"""
---------------------- {Fore.YELLOW}ダウンロードのオプション{RESET} ----------------------
      {Fore.GREEN}1. 画像URLでFantiaから画像をダウンロード{RESET}
      {Fore.GREEN}2. Fantia投稿URLから画像をダウンロードする{RESET}
      {Fore.CYAN}3. pixivファンボックスの投稿URLから画像をダウンロードする{RESET}
"""
    while True:
        lang = input("Select a language/言語を選択してください (en/jp): ").lower()
        if lang != "en" or lang != "jp": print(f"{Fore.RED}Error: Invalid language prefix entered.{RESET}")
        else: break

    main()
    print(f"{Fore.RED}Program terminated.{RESET}")
    # driver.close()