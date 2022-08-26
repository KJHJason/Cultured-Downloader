# Import Standard Libraries
import pathlib
import json
from typing import Union, Optional, Callable

# import local files
if (__name__ == "__main__"):
    from crucial import install_dependency
    from constants import CONSTANTS as C
else:
    from .crucial import install_dependency
    from .constants import CONSTANTS as C

# Import Third-party Libraries
try:
    import cryptography
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="cryptography>=37.0.4")
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

try:
    import jsonschema
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="jsonschema>=4.14.0")
    import jsonschema

try:
    import requests
except (ModuleNotFoundError, ImportError):
    install_dependency(dep="requests>=2.27.1")
    import requests

def encrypt_cookie(plaintext: Union[str, bytes], digestMethod: Optional[Callable] = hashes.SHA512) -> bytes:
    """Encrypts a plaintext using the public key (RSA-OAEP-SHA) from Cultured Downloader website.

    Args:
        plaintext (str|bytes): 
            The plaintext to encrypt.
        digestMethod (cryptography.hazmat.primitives.hashes.HashAlgorithm):
            The hash algorithm to use for the encryption (defaults to SHA512).

    Returns:
        The encrypted ciphertext (bytes).

    Raises:
        TypeError:
            If the digest method is not a subclass of cryptography.hazmat.primitives.hashes.HashAlgorithm.
    """
    if (not issubclass(digestMethod, hashes.HashAlgorithm)):
        raise TypeError("digestMethod must be a subclass of cryptography.hazmat.primitives.hashes.HashAlgorithm")

    publicKey = requests.get(C.RSA_PUBLIC_KEY_URL).json()["public_key"]
    publicKey = serialization.load_pem_public_key(publicKey.encode("utf-8"), backend=default_backend())

    if (isinstance(plaintext, str)):
        plaintext = plaintext.encode("utf-8")

    # Construct the padding
    hashAlgo = digestMethod()
    mgf = padding.MGF1(algorithm=hashAlgo)
    pad = padding.OAEP(mgf=mgf, algorithm=hashAlgo, label=None)

    # Encrypt the plaintext using the public key
    return publicKey.encrypt(plaintext=plaintext, padding=pad)