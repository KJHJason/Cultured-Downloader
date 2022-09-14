# import Python's standard libraries
import sys
import types
import logging
from typing import Optional, NoReturn, Type

# import local files
if (__package__ is None or __package__ == ""):
    from functional import print_danger
    from constants import CONSTANTS as C
else:
    from .functional import print_danger
    from .constants import CONSTANTS as C

def get_logger() -> logging.Logger:
    """Get the logger."""
    logger = logging.getLogger(C.LOGGER_NAME)

    logger.setLevel(logging.ERROR)
    separator = "-" * 100
    formatter = logging.Formatter(
        f"{separator}\n%(asctime)s [{C.LOGGER_NAME}] [%(levelname)s]: %(message)s\n{separator}"
    )

    C.LOG_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(filename=C.TODAYS_LOG_FILE_PATH, mode="a")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def exception_handler(
    exc_type: Optional[Type[BaseException]],
    exc: Optional[BaseException],
    traceback: Optional[types.TracebackType]) -> NoReturn:
    """Use a custom logger to log exceptions to a file."""
    logger.exception(f"Uncaught {exc_type.__name__}", exc_info=(exc_type, exc, traceback))
    print_danger(f"\nUncaught {exc_type.__name__}")
    print_danger(f"Please provide the developer with the error log generated at\n{logger.handlers[0].baseFilename}")

    input("Please press ENTER to exit...")
    return sys.exit(1)

logger = get_logger()

__all__ = [
    "logger",
    "exception_handler"
]