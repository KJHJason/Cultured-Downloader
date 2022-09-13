# import Python's standard libraries
import time
import json
import itertools
import threading
import functools
from typing import Any, Callable, Union, Optional

# import third-party libraries
from colorama import Fore as F, Style as S

# import local files
if (__package__ is None or __package__ == ""):
    from constants import CONSTANTS as C
else:
    from .constants import CONSTANTS as C

def convert_str_to_ansii(colour: Union[str, None]) -> str:
    """Convert a string to ANSI escape code using colorama.

    Args:
        colour (str | None): 
            The colour string to convert. (None is converted to empty string)

    Returns:
        str: The ANSI escape code.
    """
    colour_table = {
        None: "",
        "black": F.BLACK,
        "red": F.RED,
        "green": F.GREEN,
        "yellow": F.YELLOW,
        "blue": F.BLUE,
        "magenta": F.MAGENTA,
        "cyan": F.CYAN,
        "white": F.WHITE,
        "light_black": F.LIGHTBLACK_EX,
        "light_red": F.LIGHTRED_EX,
        "light_green": F.LIGHTGREEN_EX,
        "light_yellow": F.LIGHTYELLOW_EX,
        "light_blue": F.LIGHTBLUE_EX,
        "light_magenta": F.LIGHTMAGENTA_EX,
        "light_cyan": F.LIGHTCYAN_EX,
        "light_white": F.LIGHTWHITE_EX,
    }
    if (isinstance(colour, str)):
        colour = colour.lower()

    if (colour not in colour_table):
        raise ValueError("Invalid colour option.")

    return colour_table[colour]

class Spinner:
    """Spinner class for displaying a spinner animation
    with a text message in the terminal on a separate thread.

    Inspired by 
        - https://github.com/manrajgrover/halo
        - https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor
    """
    CLEAR_LINE = "\033[K"
    def __init__(self, 
        message: str,
        colour: Optional[str] = None,
        spinner_type: str = "dots",
        spinner_position: Optional[str] = "left") -> None:
        """Constructs the spinner object.

        Attributes:
            message (str):
                The message to display along with the spinner.
            colour (str | None):
                The colour of the spinner. (default: None for default terminal colour)
            spinner_type (str):
                The type of spinner to display. (default: "dots")
            spinner_position (str | None):
                The position of the spinner. (default: "left")
        """
        # Spinner configurations below
        spinner_info = self.load_spinner(spinner_type=spinner_type)
        self.__spinner = itertools.cycle(spinner_info["frames"])
        self.__interval = 0.001 * spinner_info["interval"]
        self.__message = message
        self.__colour = convert_str_to_ansii(colour)
        self.__position = spinner_position.lower()
        if (self.__position not in ("left", "right")):
            raise ValueError("Invalid spinner position.")

        # Spinner thread and event below
        self.__spinner_thread = None
        self.__stop_event = None

    def load_spinner(self, spinner_type: str) -> list[str]:
        """Load the spinner type from the JSON file in the json folder
        which was obtained from https://github.com/sindresorhus/cli-spinners/blob/main/spinners.json"""
        with open(C.SPINNERS_JSON_PATH, "r", encoding="utf-8") as f:
            spinners = json.load(f)

        if (spinner_type not in spinners):
            raise ValueError("Invalid spinner type.")
        return spinners[spinner_type]

    def get_spin(self) -> itertools.cycle:
        """returns the spinner cycle."""
        return self.__spinner

    def __run_spinner(self):
        """Run and display the spinner animation with the text message."""
        while (not self.__stop_event.is_set()):
            print(
                f"\r{self.__colour}",
                "{} {}".format(
                    *(
                        (self.__message, next(self.__spinner)) 
                        if (self.__position == "right") 
                        else (next(self.__spinner), self.__message)
                    ,)[0]
                ),
                S.RESET_ALL,
                sep="",
                end=""
            )
            time.sleep(self.__interval)

    def start(self):
        """Start the spinner and returns self."""
        self.__stop_event = threading.Event()
        self.__spinner_thread = threading.Thread(target=self.__run_spinner, daemon=True)
        self.__spinner_thread.start()
        return self

    def stop(self) -> None:
        """Stop the spinner."""
        if (self.__spinner_thread is not None and self.__spinner_thread.is_alive()):
            self.__stop_event.set()
            self.__spinner_thread.join()

        print("\r", self.CLEAR_LINE, end="", sep="")

    def __enter__(self):
        """Start the spinner object and to be used in a context manager and returns self."""
        return self.start()

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        """Stops the spinner when used in a context manager."""
        self.stop()

    def __call__(self, func: Callable):
        """Allow the spinner object to be used as a regular function decorator."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

# Test codes below
if (__name__ == "__main__"):
    import time

    @Spinner("loading", colour="yellow", spinner_position="left", spinner_type="aesthetic")
    def test():
        time.sleep(15)

    test()