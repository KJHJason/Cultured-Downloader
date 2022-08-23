# import Python's standard libraries
import sys
import subprocess
import platform
import pathlib
import shutil
from typing import Union, Optional

# import local files
from .crucial import install_dependency

try:
    import aiohttp
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="aiohttp>=3.8.1")
    import aiohttp

try:
    import requests
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="requests>=2.27.1")
    import requests

try:
    import gdown
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="gdown>=4.4.0")
    import gdown