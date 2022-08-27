# import Python's standard libraries
import json
import base64

# import local files
if (__name__ == "__main__"):
    from cryptography_operations import *
    from constants import CONSTANTS as C
    from functional import validate_schema, check_and_make_dir
else:
    from .cryptography_operations import *
    from .constants import CONSTANTS as C
    from .functional import validate_schema, check_and_make_dir

# Import Third-party Libraries
import requests

# Note: the cryptography library should have been
# installed upon import of cryptography_operations.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import types
from cryptography.hazmat.primitives import serialization

class SecureCookie:
    """Creates a way to securely deal with the cookie data 
    that is stored on the user's machine.

    The cookie stored on the user's machine is encrypted using AES-256-GCM 
    which is done server-side as only the server knows the symmetric key used.

    During transmission to Cultured Downloader API, the cookie is encrypted using asymmetric encryption
    on top of HTTPS as a form of layered security. Note that the RSA key pair is generated within 
    the current application execution and is not stored on the user's machine.
    """
    def __init__(self, cookieData: Optional[dict | bytes] = None) -> None:
        """Constructor for the SecureCookie class.

        Attributes:
            cookieData (dict | bytes): 
                The cookie data to be handled. If None, the cookie data will be loaded 
                from the saved file in the application's directory.
        """
        keyPair = generate_rsa_key_pair()
        self.__privateKey = keyPair[0].decode("utf-8")
        self.__publicKey = keyPair[1].decode("utf-8")

        if (isinstance(cookieData, dict)):
            self.__cookieData = cookieData
        elif (isinstance(cookieData, bytes)):
            self.__cookieData = self.__decrypt(cookieData)
        elif (cookieData is None):
            self.load_cookies()
        else:
            raise TypeError("Invalid cookie data type, must be a dict or bytes...")

    @property
    def cookieData(self) -> dict:
        return self.__cookieData

    @property
    def privateKey(self) -> str:
        return self.__privateKey

    @property
    def publicKey(self) -> str:
        return self.__publicKey

    def __format_private_key(self) -> types.PRIVATE_KEY_TYPES:
        return serialization.load_pem_private_key(
            data=self.privateKey.encode("utf-8"),
            password=None,
            backend=default_backend(),
        )
    def format_public_key(self) -> types.PUBLIC_KEY_TYPES:
        return serialization.load_pem_public_key(
            data=self.publicKey.encode("utf-8"),
            backend=default_backend(),
        )

    def save_cookies(self) -> None:
        """Saves the cookie data to the user's machine in a file."""
        check_and_make_dir(C.COOKIES_PATH.parent)
        with open(C.COOKIES_PATH, "wb") as f:
            f.write(self.encrypt())

    def load_cookies(self) -> None:
        """Loads the cookie data from the user's machine from the saved file."""
        with open(C.COOKIES_PATH, "rb") as f:
            self.__cookieData = self.__decrypt(f.read())

    def encrypt(self) -> bytes:
        """Encrypts the cookie data using AES-256-GCM (server-side).

        Will send the asymmetrically encrypted cookie during tranmission to Cultured Downloader API which
        does not provide much benefits but more for a layered security approach instead of just relying on HTTPS.

        The server will then decrypt the asymmetrically encrypted cookie ciphertext using its private key
        and encrypt using AES-256-GCM (server-side) and send back the encrypted cookie data which will also be asymmetrically encrypted using the user's public key from the user that was sent along with the payload.

        Returns:
            The symmetrically encrypted cookie data (bytes).

        Raises:
            Exception: 
                If the server response is not 200 or if the JSON response is invalid.
        """
        data = {
            "cookie": 
                base64.b64encode(
                    rsa_encrypt(json.dumps(self.__cookieData))
                ).decode("utf-8"), 
            "public_key":
                self.__publicKey
        }

        res = requests.post(f"{C.WEBSITE_URL}/api/v1/encrypt-cookie", json=data, headers=C.REQ_HEADERS)
        if (res.status_code != 200):
            raise Exception(f"Server Response: {res.status_code} {res.reason}")

        res = res.json()
        if ("error" in res):
            raise Exception(res["error"])
        if (not validate_schema(schema=C.SERVER_RESPONSE_SCHEMA, data=res)):
            raise Exception("Invalid JSON format response from server...")

        encryptedCookie = base64.b64decode(res["cookie"])
        return rsa_decrypt(ciphertext=encryptedCookie, privateKey=self.__format_private_key())

    def __decrypt(self, encryptedCookie: bytes) -> dict:
        """Decrypts the cookie data using AES-256-GCM (server-side).

        Will send the asymmetrically encrypted cookie during tranmission to Cultured Downloader API which
        does not provide much benefits but more for a layered security approach instead of just relying on HTTPS.

        The server will then decrypt the asymmetrically encrypted cookie ciphertext using its private key
        and decrypt using AES-256-GCM (server-side) and send back the decrypted cookie data which will also be asymmetrically encrypted using the user's public key from the user that was sent along with the payload.

        Returns:
            The symmetrically decrypted cookie data (dict).

        Raises:
            Exception: 
                If the server response is not 200 or if the JSON response is invalid.
        """
        data = {
            "cookie": 
                base64.b64encode(
                    rsa_encrypt(encryptedCookie)
                ).decode("utf-8"), 
            "public_key":
                self.__publicKey
        }

        res = requests.post(f"{C.WEBSITE_URL}/api/v1/decrypt-cookie", json=data, headers=C.REQ_HEADERS)
        if (res.status_code != 200):
            raise Exception(f"Server Response: {res.status_code} {res.reason}")

        res = res.json()
        if ("error" in res):
            raise Exception(res["error"])
        if (not validate_schema(schema=C.SERVER_RESPONSE_SCHEMA, data=res)):
            raise Exception("Invalid JSON format response from server...")

        return json.loads(
            rsa_decrypt(
                ciphertext=base64.b64decode(res["cookie"]), 
                privateKey=self.__format_private_key()
            )
        )

    def __str__(self) -> str:
        return json.dumps(self.__cookieData)

    def __repr__(self) -> str:
        return f"Cookie<{self.__cookieData}>"