# import Python's standard libraries
import json
import base64
import abc
from typing import Optional, Any, Union

# import local files
if (__name__ == "__main__"):
    from cryptography_operations import *
    from constants import CONSTANTS as C
    from functional import validate_schema
else:
    from .cryptography_operations import *
    from .constants import CONSTANTS as C
    from .functional import validate_schema

# Import Third-party Libraries
import requests

# Note: the cryptography library should have been
# installed upon import of cryptography_operations.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import types
from cryptography.hazmat.primitives import serialization

class UserData(abc.ABC):
    """Creates a way to securely deal with the user's data
    that is stored on the user's machine.

    Requires the following methods 
    to be overridden in the child class:
        - save_data
        - load_data
        - encrypt
        - decrypt

    The data stored on the user's machine is encrypted using AES-256-GCM 
    which is done server-side as only the server knows the symmetric key used.

    During transmission to Cultured Downloader API, the data is encrypted using asymmetric encryption
    on top of HTTPS as a form of layered security. Note that the RSA key pair is generated within 
    the current application execution and is not stored on the user's machine.
    """
    def __init__(self, data: Optional[Any] = None) -> None:
        """Constructor for the UserData class.

        Attributes:
            data (dict | bytes): 
                The data to be handled. If None, the data will be loaded 
                from the saved file in the application's directory via the
                load_data method that must be configured in the child class.
                Othewise, if the data is a type of bytes, it will be automatically be decrypted.
        """
        key_pair = generate_rsa_key_pair()
        self.__private_key = key_pair[0].decode("utf-8")
        self.__public_key = key_pair[1].decode("utf-8")
        self.__digest_method = "sha512" if (C.IS_64BITS) else "sha256"

        if (data is None):
            self.__data = self.load_data()
        elif (isinstance(data, bytes)):
            self.__data = self.decrypt(data)
        else:
            self.__data = data

    @abc.abstractmethod
    def save_data(self) -> None:
        """Saves the data to the user's machine."""
        pass

    @abc.abstractmethod
    def load_data(self) -> None:
        """Loads the data from the user's machine from the saved file."""
        pass

    @abc.abstractmethod
    def encrypt(self) -> bytes:
        """Encrypts the data which is done server-side on Cultured Downloader API."""
        pass

    @abc.abstractmethod
    def decrypt(self, data: bytes) -> Any:
        """Decrypts the data which is done server-side on Cultured Downloader API."""
        pass

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def private_key (self) -> str:
        return self.__private_key

    @property
    def public_key(self) -> str:
        return self.__public_key

    @property
    def digest_method(self) -> str:
        return self.__digest_method

    def prepare_data_for_transmission(self, data: Union[str, bytes]) -> str:
        """Prepares the data for transmission to the server by encrypting the payload
        using the public key obtained from Cultured Downloader API.

        Args:
            data (str | bytes): 
                The data to be transmitted for encryption.

        Returns:
            str: 
                The encrypted data to sent to Cultured Downloader API for symmetric encryption.
        """
        return base64.b64encode(rsa_encrypt(plaintext=data)).decode("utf-8")

    def read_api_response(self, received_data: str) -> bytes:
        """Reads the response from the server and decrypts the data.

        Args:
            received_data (str): 
                The data received from the server.
        """
        return rsa_decrypt(
                ciphertext=base64.b64decode(received_data), 
                private_key=self.format_private_key()
            )

    def format_private_key(self) -> types.PRIVATE_KEY_TYPES:
        """Formats the private key for use in the asymmetric encryption."""
        return serialization.load_pem_private_key(
            data=self.private_key.encode("utf-8"),
            password=None,
            backend=default_backend(),
        )
    def format_public_key(self) -> types.PUBLIC_KEY_TYPES:
        """Formats the public key for use in the asymmetric encryption."""
        return serialization.load_pem_public_key(
            data=self.publicKey.encode("utf-8"),
            backend=default_backend(),
        )

    def __str__(self) -> str:
        return str(self.__data)

    def __repr__(self) -> str:
        return f"Data<{self.__data}>"

class SecureCookie(UserData):
    """Creates a way to securely deal with the user's saved
    cookies that is stored on the user's machine."""
    def __init__(self, cookie_data: Optional[Union[bytes, dict]] = None):
        """Initializes the SecureCookie class.

        Args:
            cookie_data (dict | bytes): 
                The cookie data to be handled. If None, the cookie data will be loaded 
                from the saved file in the application's directory.
        """
        if (cookie_data is not None and not isinstance(cookie_data, Union[bytes, dict])):
            raise TypeError("cookie_data must be of type dict or bytes")

        super().__init__(data=cookie_data)

    def save_data(self) -> None:
        """Saves the cookie data to the user's machine in a file."""
        C.COOKIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(C.COOKIES_PATH, "wb") as f:
            f.write(self.encrypt())

    def load_data(self) -> None:
        """Loads the cookie data from the user's machine from the saved file."""
        with open(C.COOKIES_PATH, "rb") as f:
            self.data = self.decrypt(f.read())

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
                self.prepare_data_for_transmission(
                    data=json.dumps(self.data)
                ), 
            "public_key":
                self.public_key,
            "digest_method":
                self.digest_method
        }

        res = requests.post(f"{C.API_URL}/v1/encrypt-cookie", json=data, headers=C.REQ_HEADERS)
        if (res.status_code != 200):
            raise Exception(f"Server Response: {res.status_code} {res.reason}")

        res = res.json()
        if ("error" in res):
            raise Exception(res["error"])
        if (not validate_schema(schema=C.SERVER_RESPONSE_SCHEMA, data=res)):
            raise Exception("Invalid JSON format response from server...")

        encryptedCookie = base64.b64decode(res["cookie"])
        return rsa_decrypt(
            ciphertext=encryptedCookie,
            private_key=self.format_private_key(),
            digest_method=self.digest_method
        )

    def decrypt(self, encryptedCookie: bytes) -> dict:
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
                self.prepare_data_for_transmission(
                    data=encryptedCookie
                ),
            "public_key":
                self.public_key,
            "digest_method":
                self.digest_method
        }

        res = requests.post(f"{C.API_URL}/v1/decrypt-cookie", json=data, headers=C.REQ_HEADERS)
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
                private_key=self.format_private_key(),
                digest_method=self.digest_method
            )
        )

    def __str__(self) -> str:
        return json.dumps(self.data)

    def __repr__(self) -> str:
        return f"Cookie<{self.data}>"