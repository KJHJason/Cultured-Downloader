# import Python's standard libraries
import json
import base64
import abc
import binascii
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
import httpx

# Note: the cryptography library should have been
# installed upon import of cryptography_operations.py
from cryptography.exceptions import InvalidTag
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
            data (Any | bytes): 
                The data to be handled. If None, the data will be loaded 
                from the saved file in the application's directory via the
                load_data method that must be configured in the child class.
                Othewise, if the data is a type of bytes, it will be automatically be decrypted.
        """
        key_pair = generate_rsa_key_pair()
        self.__private_key = key_pair[0].decode("utf-8")
        self.__public_key = key_pair[1].decode("utf-8")
        self.__client_digest_method = "sha512"  if (C.IS_64BITS) \
                                                else "sha256"
        self.__server_digest_method = "sha512"  if (self.__client_digest_method == "sha512") \
                                                else "sha256"

        self.__secret_key = self.__load_key()
        if (data is None):
            self.data = self.load_data()
        elif (isinstance(data, bytes)):
            self.data = self.decrypt(data)
        else:
            self.data = data

    @abc.abstractmethod
    def save_data(self) -> None:
        """Saves the data to the user's machine."""
        pass

    @abc.abstractmethod
    def load_data(self) -> None:
        """Loads the data from the user's machine from the saved file."""
        pass

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
        return base64.b64encode(
            rsa_encrypt(plaintext=data, digest_method=self.server_digest_method)
        ).decode("utf-8")

    def read_api_response(self, received_data: str) -> bytes:
        """Reads the response from the server and decrypts the data.

        Args:
            received_data (str): 
                The data received from the server.
        """
        return rsa_decrypt(
            ciphertext=base64.b64decode(received_data), 
            private_key=self.format_private_key(), 
            digest_method=self.server_digest_method
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

    def get_csrf_token(self) -> tuple:
        """Gets the CSRF token from the server.

        Returns:
            The CSRF token (str) and the session cookie with the CSRF token.
        """
        with httpx.Client(http2=True, headers=C.REQ_HEADERS) as client:
            res = client.get(f"{C.API_URL}/csrf-token")

        if (res.status_code not in (200, 404)):
            raise Exception(f"Server Response: {res.status_code} {res.reason}")

        cookies = res.cookies
        json_data = res.json()
        if ("error" in json_data):
            raise Exception(json_data["error"])
        if (not validate_schema(schema=C.SERVER_CSRF_RESPONSE, data=json_data)):
            raise Exception("Invalid JSON format response from server...")

        return json_data["csrf_token"], cookies

    def __load_key(self) -> bytes:
        """Loads the secret symmetric key from the API or locally"""
        secret_key_path = C.SECRET_KEY_PATH
        if (secret_key_path.exists() and secret_key_path.is_file()):
            with open(secret_key_path, "rb") as f:
                return f.read()

        key_id_token_path = C.KEY_ID_TOKEN_JSON_PATH
        key_id_token = None
        if (key_id_token_path.exists() and key_id_token_path.is_file()):
            with open(key_id_token_path, "r") as f:
                try:
                    key_id_token = json.load(f).get("key_id_token")
                except (json.JSONDecodeError, TypeError):
                    pass

        if (key_id_token is None):
            return generate_chacha20_key()

        csrf_token, cookies = self.get_csrf_token()
        json_data = {
            "csrf_token":
                csrf_token,
            "server_digest_method": 
                self.__server_digest_method,
            "client_public_key":
                self.__public_key,
            "client_digest_method":
                self.__client_digest_method,
            "key_id_token":
                self.prepare_data_for_transmission(
                    data=key_id_token
                )
        }
        with httpx.Client(http2=True, headers=C.REQ_HEADERS, cookies=cookies) as client:
            res = client.post(f"{C.API_URL}/get-key", json=json_data)

        if (res.status_code not in (200, 404, 400)):
            raise Exception(f"Server Response: {res.status_code}")

        if (res.status_code == 404):
            # happens when the key_id_token 
            # has expired or is invalid
            key_id_token_path.unlink()
            return generate_chacha20_key()

        json_data = res.json()
        if ("error" in json_data):
            raise Exception(json_data["error"])
        if (not validate_schema(schema=C.SECRET_KEY_RESPONSE_SCHEMA, data=json_data)):
            raise Exception("Invalid JSON format response from server...")

        secret_key = self.read_api_response(json_data["secret_key"])
        return secret_key

    def save_key(self, save_locally: Optional[bool] = False) -> None:
        """Saves the secret symmetric key to the API or locally.

        Args:
            save_locally (bool, optional):
                Whether to save the key locally or not. Defaults to False.

        Returns:
            None
        """
        if (save_locally):
            with open(C.SECRET_KEY_PATH, "wb") as f:
                f.write(self.__secret_key)

        csrf_token, cookies = self.get_csrf_token()
        json_data = {
            "csrf_token":
                csrf_token,
            "server_digest_method": 
                self.__server_digest_method,
            "client_public_key":
                self.__public_key,
            "client_digest_method":
                self.__client_digest_method,
            "secret_key":
                self.prepare_data_for_transmission(
                    data=self.__secret_key
                )
        }

        with httpx.Client(http2=True, headers=C.REQ_HEADERS, cookies=cookies) as client:
            res = client.post(f"{C.API_URL}/save-key", json=json_data)

        if (res.status_code not in (200, 400)):
            raise Exception(f"Server Response: {res.status_code}")

        res = res.json()
        if ("error" in res):
            raise Exception(res["error"])
        if (not validate_schema(schema=C.KEY_ID_TOKEN_RESPONSE_SCHEMA, data=res)):
            raise Exception("Invalid JSON format response from server...")

        key_id_token = rsa_decrypt(
            ciphertext=base64.b64decode(res["key_id_token"]),
            private_key=self.format_private_key(),
            digest_method=self.client_digest_method,
            decode=True
        )
        with open(C.KEY_ID_TOKEN_JSON_PATH, "w") as f:
            json.dump({"key_id_token": key_id_token}, f, indent=4)

    @property
    def secret_key(self) -> bytes:
        return self.__secret_key

    @property
    def private_key (self) -> str:
        return self.__private_key

    @property
    def public_key(self) -> str:
        return self.__public_key

    @property
    def client_digest_method(self) -> str:
        return self.__client_digest_method

    @property
    def server_digest_method(self) -> str:
        return self.__server_digest_method

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"Data<{self.data}>"

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
        encrypted_cookies, nonce = chacha_encrypt(plaintext=self.data, key=self.secret_key)
        encoded_cookies = base64.b64encode(encrypted_cookies)
        nonce = base64.b64encode(nonce)
        with open(C.COOKIES_PATH, "w") as f:
            f.write(".".join((encoded_cookies.decode("utf-8"), nonce.decode("utf-8"))))

    def load_data(self) -> None:
        """Loads the cookie data from the user's machine from the saved file."""
        if (not C.COOKIES_PATH.exists() and not C.COOKIES_PATH.is_file()):
            self.data = {}
            return

        with open(C.COOKIES_PATH, "r") as f:
            try:
                encrypted_data, nonce = f.read().split(".")
            except (ValueError):
                raise Exception("Invalid cookie data...")

        try:
            encrypted_data = base64.b64decode(encrypted_data)
            nonce = base64.b64decode(nonce)
        except (binascii.Error, TypeError, ValueError):
            raise Exception("Invalid cookie data...")

        try:
            self.data = chacha_decrypt(ciphertext=encrypted_data, key=self.secret_key, nonce=nonce)
        except (InvalidTag):
            self.data = {}
            C.COOKIES_PATH.unlink()

    def __str__(self) -> str:
        return json.dumps(self.data)

    def __repr__(self) -> str:
        return f"Cookie<{self.data}>"

# test codes
if (__name__ == "__main__"):
    SecureCookie({"test": "test"}).save_key()