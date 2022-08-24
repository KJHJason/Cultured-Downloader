# import Python's standard libraries
import pathlib
import re
import sys
from typing import NoReturn, Union, Optional, Any

# import local files
if (__name__ != "__main__"):
    from .crucial import install_dependency
    from .constants import CONSTANTS as C
else:
    from crucial import install_dependency
    from constants import CONSTANTS as C

# import third-party libraries
from colorama import Fore as F

def print_danger(message: Any, **kwargs) -> None:
    """Print a message in red.

    Args:
        message (Any):
            The message to print.
        kwargs:
            Any keyword arguments to pass to the print function.

    Returns:
        None
    """
    print(f"{F.LIGHTRED_EX}{message}{F.RESET}", **kwargs)

def print_warning(message: Any, **kwargs) -> None:
    """Print a message in yellow.

    Args:
        message (Any):
            The message to print.
        kwargs:
            Any keyword arguments to pass to the print function.

    Returns:
        None
    """
    print(f"{F.LIGHTYELLOW_EX}{message}{F.RESET}", **kwargs)

def print_success(message: Any, **kwargs) -> None:
    """Print a message in green.

    Args:
        message (Any):
            The message to print.
        kwargs:
            Any keyword arguments to pass to the print function.

    Returns:
        None
    """
    print(f"{F.LIGHTGREEN_EX}{message}{F.RESET}", **kwargs)

def check_and_make_dir(dirPath: pathlib.Path) -> None:
    """Check if a directory exists and if not, create it.

    Args:
        dirPath (pathlib.Path):
            The path of the directory to check and create if it doesn't exist.

    Returns:
        None
    """
    if (not dirPath.exists() and not dirPath.is_dir()):
        dirPath.mkdir(parents=True)

def get_saved_folder_path() -> Union[pathlib.Path, NoReturn]:
    """Returns a pathlib Path object of Cultured Downloader folder where files are saved depending on the platform.
    Supported OS: Windows, Linux, macOS
    """
    if (C.USER_PLATFORM == "Windows"):
        dataDirectory = pathlib.Path.home().joinpath("AppData/Roaming/Cultured-Downloader")
    elif (C.USER_PLATFORM == "Linux"):
        dataDirectory = pathlib.Path.home().joinpath(".config/Cultured-Downloader")
    elif (C.USER_PLATFORM == "Darwin"): # macOS
        dataDirectory = pathlib.Path.home().joinpath("Library/Preferences/Cultured-Downloader")
    else:
        print_danger(f"Your OS is not supported")
        print_danger(f"Supported OS: Windows, Linux, macOS...")
        print("Please enter any key to exit")
        return sys.exit(1)

    check_and_make_dir(dirPath=dataDirectory)
    return dataDirectory

def print_menu(loginStatus: dict[str, bool]) -> None:
    """Print the menu for the user to read and enter their desired action

    Args:
        loginStatus (dict[str, bool]):
            The login status of the user,
            E.g. {"pixiv": False, "fantia": True}

    Returns:
        None
    """
    fantiaStatus, pixivStatus = loginStatus.get("fantia"), loginStatus.get("pixiv")
    print(f"""{F.LIGHTYELLOW_EX}
> Login Status...
> Fantia: {'Logged In' if (fantiaStatus) else 'Guest (Not logged in)'}
> Pixiv: {'Logged In' if (pixivStatus) else 'Guest (Not logged in)'}
{C.END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{C.END} --------------------
      {F.GREEN}1. Download images from Fantia post(s){C.END}
      {F.GREEN}2. Download all Fantia posts from creator(s){C.END}
      {F.LIGHTCYAN_EX}3. Download images from pixiv Fanbox post(s){C.END}
      {F.LIGHTCYAN_EX}4. Download all pixiv Fanbox posts from a creator(s){C.END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{C.END} ----------------------
      {F.LIGHTBLUE_EX}5. Change Default Download Folder{C.END}""")

    if (not fantiaStatus or not pixivStatus):
        print(f"      {F.LIGHTBLUE_EX}6. Login{C.END}")

    print(f"\n---------------------- {F.LIGHTYELLOW_EX}Other Options{C.END} ----------------------")
    print(f"      {F.LIGHTRED_EX}Y. Report a bug{C.END}")
    print(f"      {F.RED}X. Shutdown the program{C.END}")
    print()

def get_input(inputMsg: str, inputs: Optional[Union[tuple[str], list[str]]] = None, 
              regex: re.Pattern[str] = None, default: Optional[str] = None,
              warning: str = None) -> Any:
    """Get the expected input from the user.

    Args:
        inputMsg (str):
            The message to print to the user.
        inputs (tuple[str] | list[str], optional):
            The inputs that the user can enter.
            Note: inputs must be lowercase but will be converted to lowercase string as a failsafe.
            If this is passed in, regex parameter cannot be passed in!
        regex (re.Pattern[str], optional):
            The regex pattern to match the input against.
            If this is passed in, inputs parameter cannot be passed in!
        default (str, optional):
            The default input to be returned if the user doesn't enter anything.
        warning (str, optional):
            The warning message to print to the user if the input is invalid.

    Returns:
        The input the user entered.

    Raises:
        ValueError:
            If the inputs and regex are both passed in.
    """
    if (inputs and regex):
        raise ValueError("inputs and regex cannot be passed in together")

    if (inputs is not None and (not isinstance(inputs, tuple) and not isinstance(inputs, list))):
        raise TypeError("inputs must be a tuple or a list")
    if (regex is not None and not isinstance(regex, re.Pattern)):
        raise TypeError("regex must be a re.Pattern")
    if (warning is not None and not isinstance(warning, str)):
        raise TypeError("warning must be a str")

    if (inputs is not None):
        # failsafe if the list or tuple passed in does not contain all lowercase strings
        inputs = tuple(str(inp).lower() for inp in inputs)

    while (1):
        userInput = input(inputMsg).strip().lower()
        if (inputs is not None and userInput in inputs):
            return userInput
        elif (regex is not None and regex.match(userInput)):
            return userInput
        elif (default is not None and userInput == ""):
            return default
        else:
            print_danger(f"Sorry, please enter a valid input." if (warning is None) else warning)