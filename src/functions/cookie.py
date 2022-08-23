# Import Standard Libraries
import pathlib
import json

# import local files
from .crucial import install_dependency

# Import Third-party Libraries
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="cryptography>=37.0.4")
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    import jsonschema
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="jsonschema>=4.14.0")
    import jsonschema