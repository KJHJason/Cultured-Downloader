# import Python's standard libraries
import re
import json
from typing import Union, Optional, Any

# import local files
if (__package__ is None or __package__ == ""):
    from schemas.config import ConfigSchema
    from constants import CONSTANTS as C
else:
    from .schemas.config import ConfigSchema
    from .constants import CONSTANTS as C

# import third-party libraries
from colorama import Fore as F
from pydantic import BaseModel
import pydantic.error_wrappers as pydantic_error_wrappers 

def validate_schema(schema: BaseModel, data: Union[dict, list], 
                    return_bool: Optional[bool] = True) -> Union[bool, BaseModel]:
    """Validates the data against the schema

    Args:
        schema (BaseModel): 
            The pydantic base model object to validate against
        data (dict | list):
            The data to validate
        return_bool (bool, optional):
            Whether to return a boolean or the pydantic base model object.

    Returns:
        Union[bool, BaseModel]:
            False if the data is invalid, otherwise the pydantic base model object with the data or a boolean.
    """
    if (not isinstance(data, Union[dict, list])):
        return False

    try:
        pydantic_obj = schema(**data)
        return pydantic_obj if (not return_bool) else True
    except (pydantic_error_wrappers.ValidationError):
        return False

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

def load_configs() -> Union[bool, BaseModel]:
    """Load the configs from the config file.

    Returns:
        Any: The configs loaded from the config file.
    """
    configs = {}
    if (C.CONFIG_JSON_FILE_PATH.exists() and C.CONFIG_JSON_FILE_PATH.is_file()):
        with open(C.CONFIG_JSON_FILE_PATH, "r") as f:
            configs = json.load(f)

    return validate_schema(schema=ConfigSchema, data=configs, return_bool=False)

def edit_configs(new_configs: dict) -> None:
    """Edit the configs in the config file.
    Args:
        new_configs (dict):
            The new configuration to save to the config file.

    Returns:
        None
    """
    with open(C.CONFIG_JSON_FILE_PATH, "w") as f:
        json.dump(new_configs, f, indent=4)

def print_menu(login_status: dict[str, bool]) -> None:
    """Print the menu for the user to read and enter their desired action

    Args:
        login_status (dict[str, bool]):
            The login status of the user,
            E.g. {"pixiv": False, "fantia": True}

    Returns:
        None
    """
    fantia_status, pixiv_status = login_status.get("fantia"), login_status.get("pixiv")
    print(f"""{F.LIGHTYELLOW_EX}
> Login Status...
> Fantia: {'Logged In' if (fantia_status) else 'Guest (Not logged in)'}
> Pixiv: {'Logged In' if (pixiv_status) else 'Guest (Not logged in)'}
{C.END}
--------------------- {F.LIGHTYELLOW_EX}Download Options{C.END} --------------------
      {F.GREEN}1. Download images from Fantia post(s){C.END}
      {F.GREEN}2. Download all Fantia posts from creator(s){C.END}
      {F.LIGHTCYAN_EX}3. Download images from pixiv Fanbox post(s){C.END}
      {F.LIGHTCYAN_EX}4. Download all pixiv Fanbox posts from a creator(s){C.END}

---------------------- {F.LIGHTYELLOW_EX}Config Options{C.END} ----------------------
      {F.LIGHTBLUE_EX}5. Change Default Download Folder{C.END}""")

    if (not fantia_status or not pixiv_status):
        print(f"      {F.LIGHTBLUE_EX}6. Login{C.END}")

    print(f"\n---------------------- {F.LIGHTYELLOW_EX}Other Options{C.END} ----------------------")
    print(f"      {F.LIGHTRED_EX}Y. Report a bug{C.END}")
    print(f"      {F.RED}X. Shutdown the program{C.END}")
    print()

def get_input(input_msg: str, inputs: Optional[Union[tuple[str], list[str]]] = None, 
              regex: re.Pattern[str] = None, default: Optional[str] = None,
              warning: str = None, extra_information: Optional[str] = None) -> Any:
    """Get the expected input from the user.

    Args:
        input_msg (str):
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
        extra_information (str, optional):
            The extra information to print to the user before the input message.

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
        # fail-safe if the list or tuple passed in does not contain all lowercase strings
        inputs = tuple(str(inp).lower() for inp in inputs)

    while (1):
        if (extra_information is not None):
            print_warning(extra_information)

        user_input = input(input_msg).strip().lower()
        if (inputs is not None and user_input in inputs):
            return user_input
        elif (regex is not None and regex.match(user_input)):
            return user_input
        elif (default is not None and user_input == ""):
            return default
        else:
            print_danger(f"Sorry, please enter a valid input." if (warning is None) else warning)