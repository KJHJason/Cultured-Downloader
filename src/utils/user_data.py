# import Python's standard libraries
import re
import abc
import json
import time
import base64
import pathlib
import warnings
import binascii
import threading
from typing import Optional, Any, Union, Literal

# import local files
if (__package__ is None or __package__ == ""):
    from errors import APIServerError
    from cryptography_operations import *
    from constants import CONSTANTS as C
    from logger import logger
    from spinner import Spinner
    from schemas import CookieSchema, APIKeyResponse, APIKeyIDResponse, APICsrfResponse, KeyIdToken, ClientSecret, ClientToken
    from functional import  validate_schema, save_key_prompt, print_success, \
                            print_danger, load_configs, edit_configs, log_api_error, website_to_readable_format
else:
    from .errors import APIServerError
    from .cryptography_operations import *
    from .constants import CONSTANTS as C
    from .logger import logger
    from .spinner import Spinner
    from .schemas import CookieSchema, APIKeyResponse, APIKeyIDResponse, APICsrfResponse, KeyIdToken, ClientSecret, ClientToken
    from .functional import validate_schema, save_key_prompt, print_success, \
                            print_danger, load_configs, edit_configs, log_api_error, website_to_readable_format

# Import Third-party Libraries
import httpx
from pydantic import BaseModel

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
        - __str__
        - __repr__

    The data stored on the user's machine is encrypted client-side using ChaCha20-Poly1305.
    However, the user can opt to store their generated secret key on Cultured Downloader API
    or on their own machine if they wish for a faster loading time.

    During transmission to Cultured Downloader API, the user's secret key or key ID token
    is encrypted using asymmetric encryption on top of HTTPS as a form of layered security.
    Note that the RSA key pair is generated within the 
    current application execution and is not stored on the user's machine.
    """
    def __init__(self, data_path: pathlib.Path, data: Optional[Any] = None) -> None:
        """Constructor for the UserData class.

        Args:
            data_path (pathlib.Path):
                The path to the file where the data is stored.
            data (Any, Optional): 
                The data to be handled. If None, the data will be loaded 
                from the saved file in the application's directory via the
                load_data method that must be configured in the child class.
        """
        key_pair = generate_rsa_key_pair()
        self.__private_key = key_pair[0].decode("utf-8")
        self.__public_key = key_pair[1].decode("utf-8")
        self.__client_digest_method = self.__load_client_digest_method()
        self.__server_digest_method = "sha512"  if (self.__client_digest_method == "sha512") \
                                                else "sha256"

        if (not isinstance(data_path, pathlib.Path)):
            raise TypeError(f"Expected pathlib.Path object, got {type(data_path)} for data_path argument.")
        self.__data_path = data_path

        self.__secret_key = self.__load_key()
        if (data is None):
            self.data = self.load_data()
        else:
            self.data = data

    def __load_client_digest_method(self) -> str:
        """Loads the client's digest method from the configs file."""
        configs = load_configs()
        if (configs.client_digest_method is None):
            configs.client_digest_method = "sha512" if (C.IS_64BITS) \
                                                    else "sha256"
            edit_configs(configs.dict())

        return configs.client_digest_method

    def encrypt_data(self, data: Optional[Any] = None) -> None:
        """Encrypts the cookie data to the user's machine in a file."""
        self.__data_path.parent.mkdir(parents=True, exist_ok=True)

        if (data is None):
            data = self.data
        encrypted_data, nonce = chacha_encrypt(plaintext=data, key=self.__secret_key)

        encoded_data = base64.b64encode(encrypted_data)
        nonce = base64.b64encode(nonce)
        with open(self.__data_path, "w") as f:
            f.write(".".join((encoded_data.decode("utf-8"), nonce.decode("utf-8"))))

    def decrypt_data(self, decode: Optional[bool] = True, schema: Optional[BaseModel] = None, 
                     regex: Optional[re.Pattern] = None) -> Union[bytes, str, dict, None]:
        """Decrypt the cookie data from the user's machine from the saved file.

        Args:
            decode (bool):
                Whether to decode the plaintext from bytes to a string. 
                (Must be True if validating against a schema or a regex.)
            schema (BaseModel):
                The schema to validate the data against.
                (Will parse the decrypted data into a dictionary if not None.)
            regex (re.Pattern):
                The regex pattern to validate the data against.

        Returns:
            bytes | str | dict | None: 
                The data or None if the file does not exist or is invalid.
        """
        if (schema is not None and regex is not None):
            raise ValueError("Cannot validate against both schema and regex at the same time")

        if (not decode and (schema is not None or regex is not None)):
            warnings.warn("Cannot validate schema/regex if decode is False. Hence, decode will be set to True.")
            decode = True

        if (not self.__data_path.exists() or not self.__data_path.is_file()):
            return

        with open(self.__data_path, "r") as f:
            encrypted_data_with_nonce = f.read()

        try:
            encrypted_data, nonce = encrypted_data_with_nonce.split(sep=".")
        except (ValueError):
            self.__data_path.unlink()
            return

        try:
            encrypted_data = base64.b64decode(encrypted_data)
            nonce = base64.b64decode(nonce)
        except (binascii.Error, TypeError, ValueError):
            self.__data_path.unlink()
            return

        try:
            decrypted_data = chacha_decrypt(
                ciphertext=encrypted_data, 
                key=self.__secret_key, 
                nonce=nonce
            )
        except (InvalidTag, ValueError):
            self.__data_path.unlink()
            return

        if (decode):
            decrypted_data = decrypted_data.decode("utf-8")

        if (regex is not None):
            if (regex.match(decrypted_data) is None):
                self.__data_path.unlink()
                return

        if (schema is not None):
            try:
                decrypted_data = json.loads(decrypted_data)
            except (json.JSONDecodeError):  
                self.__data_path.unlink()
                return

            if (not validate_schema(schema, decrypted_data)):
                self.__data_path.unlink()
                return

        return decrypted_data

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
            rsa_encrypt(plaintext=data, digest_method=self.__server_digest_method)
        ).decode("utf-8")

    def read_api_response(self, received_data: str) -> bytes:
        """Reads the response from the server and decrypts the data.

        Args:
            received_data (str): 
                The data received from the server.
        """
        return rsa_decrypt(
            ciphertext=base64.b64decode(received_data), 
            private_key=self.__format_private_key(), 
            digest_method=self.__client_digest_method
        )

    def __format_private_key(self) -> types.PRIVATE_KEY_TYPES:
        """Formats the private key for use in the asymmetric encryption."""
        return serialization.load_pem_private_key(
            data=self.__private_key.encode("utf-8"),
            password=None,
            backend=default_backend(),
        )

    def format_public_key(self) -> types.PUBLIC_KEY_TYPES:
        """Formats the public key for use in the asymmetric encryption."""
        return serialization.load_pem_public_key(
            data=self.__public_key.encode("utf-8"),
            backend=default_backend(),
        )

    def get_csrf_token(self) -> tuple:
        """Gets the CSRF token from the server.

        Returns:
            The CSRF token (str) and the session cookie with the CSRF token.
        """
        with httpx.Client(http2=True, headers=C.BASE_REQ_HEADERS, timeout=30) as client:
            try:
                res = client.get(f"{C.API_URL}/csrf-token")
            except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.error(f"httpx error while retrieving CSRF token from the API:\n{e}")
                raise

        if (res.status_code not in (200, 404)):
            log_api_error(f"Received {res.status_code} response\n{res.text}")

        cookies = res.cookies
        json_data = res.json()
        if ("error" in json_data):
            log_api_error(json_data["error"])
        if (not validate_schema(schema=APICsrfResponse, data=json_data)):
            log_api_error("Invalid JSON format response from server...")

        return json_data["csrf_token"], cookies

    def __load_key(self) -> bytes:
        """Loads the secret symmetric key from the API or locally"""
        secret_key_path = C.SECRET_KEY_PATH
        if (secret_key_path.exists() and secret_key_path.is_file()):
            with open(secret_key_path, "rb") as f:
                secret_key = f.read()

            if (len(secret_key) == 32):
                return secret_key

        key_id_token = None
        key_id_token_path = C.KEY_ID_TOKEN_JSON_PATH
        if (key_id_token_path.exists() and key_id_token_path.is_file()):
            with open(key_id_token_path, "r") as f:
                try:
                    key_id_token_json = json.load(f)
                except (json.JSONDecodeError, TypeError):
                    key_id_token_json = None

            if (key_id_token_json is not None):
                key_id_token_obj: KeyIdToken = validate_schema(
                    schema=KeyIdToken,
                    data=key_id_token_json,
                    return_bool=False
                )
                if (key_id_token_obj is not False):
                    key_id_token = key_id_token_obj.key_id_token

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
        with httpx.Client(http2=True, headers=C.JSON_REQ_HEADERS, cookies=cookies, timeout=30) as client:
            try:
                res = client.post(f"{C.API_URL}/get-key", json=json_data)
            except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.error(f"httpx error while loading key from API:\n{e}")
                raise

        if (res.status_code not in (200, 404, 400)):
            log_api_error(f"Received {res.status_code} response\n{res.text}")

        if (res.status_code == 404):
            # happens when the key_id_token 
            # has expired or is invalid
            key_id_token_path.unlink()
            return generate_chacha20_key()

        json_data = res.json()
        if ("error" in json_data):
            log_api_error(json_data["error"])
        if (not validate_schema(schema=APIKeyResponse, data=json_data)):
            log_api_error("Invalid JSON format response from server...")

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
        # Check if the key was already saved locally
        if (C.SECRET_KEY_PATH.exists() and C.SECRET_KEY_PATH.is_file()):
            with open(C.SECRET_KEY_PATH, "rb") as f:
                if (f.read() == self.__secret_key):
                    return

        # Check if the key was already saved on the API
        if (C.KEY_ID_TOKEN_JSON_PATH.exists() and C.KEY_ID_TOKEN_JSON_PATH.is_file()):
            return

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

        with httpx.Client(http2=True, headers=C.JSON_REQ_HEADERS, cookies=cookies, timeout=30) as client:
            try:
                res = client.post(f"{C.API_URL}/save-key", json=json_data)
            except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.error(f"httpx error while saving key from API:\n{e}")
                raise

        if (res.status_code not in (200, 400)):
            log_api_error(f"Received {res.status_code} response\n{res.text}")

        res = res.json()
        if ("error" in res):
            log_api_error(res["error"])
        if (not validate_schema(schema=APIKeyIDResponse, data=res)):
            log_api_error("Invalid JSON format response from server...")

        key_id_token = rsa_decrypt(
            ciphertext=base64.b64decode(res["key_id_token"]),
            private_key=self.__format_private_key(),
            digest_method=self.__client_digest_method,
            decode=True
        )
        with open(C.KEY_ID_TOKEN_JSON_PATH, "w") as f:
            json.dump({"key_id_token": key_id_token}, f, indent=4)

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass

def convert_website_to_path(website: str) -> pathlib.Path:
    """Converts a website to a path.

    Args:
        website (str): 
            The website to convert.

    Returns:
        pathlib.Path: 
            The path of the website.
    """
    path_table = {
        "fantia": C.FANTIA_COOKIE_PATH,
        "pixiv_fanbox": C.PIXIV_FANBOX_COOKIE_PATH,
    }
    if (website not in path_table):
        raise ValueError(f"Invalid website: {website}")
    return path_table[website]

class SecureCookie(UserData):
    """Creates a way to securely deal with the user's saved
    cookies that is stored on the user's machine."""
    def __init__(self, website: str, cookie_data: Optional[dict] = None) -> None:
        """Initializes the SecureCookie class.

        Args:
            website (str):
                The website that the cookie data is for.
            cookie_data (dict, Optional): 
                The cookie data to be handled. If None, the cookie data will be loaded 
                from the saved file in the application's directory.
        """
        if (not isinstance(cookie_data, Union[None, dict])):
            raise TypeError("cookie_data must be of type dict or None")

        super().__init__(
            data=cookie_data, 
            data_path=convert_website_to_path(website)
        )

    def save_data(self) -> None:
        """Saves the data to the user's machine."""
        return self.encrypt_data(data=json.dumps(self.data))

    def load_data(self) -> Union[dict, None]:
        """Loads the data from the user's machine from the saved file."""
        return self.decrypt_data(decode=True, schema=CookieSchema)

    def __str__(self) -> str:
        return json.dumps(self.data)

    def __repr__(self) -> str:
        return f"Cookie<{self.data}>"

class SecureGoogleOAuth2(UserData):
    """Creates a way to securely deal with the user's saved
    Google OAuth2 files that are stored on the user's machine."""
    def __init__(self, is_token: bool, client_data: Optional[Union[str, dict]] = None) -> None:
        """Initializes the SecureGDriveAPIKey class.

        Args:
            is_token (bool):
                Whether the data is the secret token or not.
            client_data (str | dict, Optional): 
                The client JSON data to be handled. If None, the client JSON data will be loaded 
                from the saved file in the application's directory.
        """
        if (client_data is not None and not isinstance(client_data, Union[dict, str])):
            raise TypeError("Google client_data must be of type str, dict, or None")

        if (isinstance(client_data, dict)):
            client_data = json.dumps(client_data)

        self.__is_token = is_token
        if (self.__is_token):
            data_path = C.GOOGLE_OAUTH_CLIENT_TOKEN
        else:
            data_path = C.GOOGLE_OAUTH_CLIENT_SECRET

        super().__init__(
            data=client_data, 
            data_path=data_path
        )

    def save_data(self) -> None:
        """Saves the data to the user's machine."""
        return self.encrypt_data(data=self.data)

    def load_data(self) -> Union[dict, None]:
        """Loads the data from the user's machine from the saved file."""
        if (self.__is_token):
            schema = ClientToken
        else:
            schema = ClientSecret

        return self.decrypt_data(decode=True, schema=schema)

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)

    def __repr__(self) -> str:
        return f"SecureGoogleOAuth2<{self.__str__()}>"

def save_key_with_retries(obj: Union[SecureCookie, SecureGoogleOAuth2], save_key_locally: bool) -> bool:
    """Saves the user's key to the API server.

    Args:
        obj (SecureCookie | SecureGoogleOAuth2): 
            The UserData object to save the key with.
        save_key_locally (bool):
            Whether or not to save the key locally.

    Returns:
        Boolean to indicate whether or not the key was saved successfully.
    """
    for retry_counter in range(C.MAX_RETRIES):
        try:
            obj.save_key(save_locally=save_key_locally)
        except (APIServerError, httpx.ReadTimeout, httpx.ConnectTimeout, json.JSONDecodeError):
            if (retry_counter == C.MAX_RETRIES_CHECK):
                return False
            time.sleep(C.RETRY_WAIT_TIME)
        else:
            return True

def load_key_with_retries(obj: Union[SecureCookie, SecureGoogleOAuth2], *args: Any, **kwargs: Any) -> Union[SecureCookie, SecureGoogleOAuth2, None]:
    """Loads the user's key from the API server.

    Args:
        obj (UserData): 
            The UserData object to load the key with.
        *args (Any):
            The arguments to pass to the object.
        **kwargs (Any):
            The keyword arguments to pass to the object.

    Returns:
        SecureCookie | SecureGoogleOAuth2 | None:
            The UserData object that was passed in or None if the key could not be loaded.
    """
    for retry_counter in range(C.MAX_RETRIES):
        try:
            return obj(*args, **kwargs)
        except (APIServerError, httpx.ReadTimeout, httpx.ConnectTimeout, json.JSONDecodeError):
            if (retry_counter == C.MAX_RETRIES_CHECK):
                return None
            time.sleep(C.RETRY_WAIT_TIME)

def save_data(obj: Union[SecureCookie, SecureGoogleOAuth2], save_key_locally: bool, *args, **kwargs) -> bool:
    """Saves the data to the user's machine.

    Args:
        obj (SecureCookie | SecureGoogleOAuth2):
            The object to use to save the data.
        save_key_locally (bool):
            Whether to save the key locally or not.
        *args (list):
            The arguments to pass to the object.
        **kwargs (dict):
            The keyword arguments to pass to the object.

    Returns:
        bool: 
            Whether the data was saved successfully or not.
    """
    secure_obj = load_key_with_retries(obj, *args, **kwargs)
    if (secure_obj is None):
        return False

    if (save_key_with_retries(secure_obj, save_key_locally=save_key_locally)):
        secure_obj.save_data()
        return True
    else:
        return False

def load_data(obj: Union[SecureCookie, SecureGoogleOAuth2], *args, **kwargs) -> Union[str, dict, bytes, None, Literal[False]]:
    """Loads the data from the user's machine from the saved file.

    Args:
        obj (SecureCookie | SecureGoogleOAuth2):
            The object to use to load the data.
        *args (list):
            The arguments to pass to the object.
        **kwargs (dict):
            The keyword arguments to pass to the object.

    Returns:
        str | dict | bytes | None | False:
            The data that was loaded from the user's machine,
            False if the key could not be loaded, or None if the data could not be decrypted.
    """
    secure_obj = load_key_with_retries(obj, *args, **kwargs)
    if (secure_obj is None):
        return False
    else:
        return secure_obj.data

class SaveGoogleOAuth2Thread(threading.Thread):
    """Thread to securely save the cookie to a file."""
    def __init__(self, client_data: Union[dict, str], is_token: bool, save_locally: bool, **threading_kwargs) -> None:
        """Constructor for the SaveCookieThread class.

        Args:
            client_data (dict | str):
                The client data to save.
            is_token (bool):
                Whether the data is the secret token or not.
            save_locally (bool):
                Whether to save the key locally or not.
            threading_kwargs (dict):
                The keyword arguments for the threading.Thread class.
        """
        super().__init__(**threading_kwargs)
        self.client_data = client_data
        self.is_token = is_token
        self.save_locally = save_locally

    def run(self) -> None:
        """Runs the thread."""
        self.result = save_data(
            SecureGoogleOAuth2, 
            save_key_locally=self.save_locally, 
            client_data=self.client_data, 
            is_token=self.is_token
        )

class LoadGoogleOAuth2Thread(threading.Thread):
    """Thread to securely load the cookie from a file."""
    def __init__(self, is_token: bool, **threading_kwargs) -> None:
        """Constructor for the LoadCookieThread class.

        Args:
            is_token (bool):
                Whether the data is the secret token or not.
            threading_kwargs (dict):
                The keyword arguments for the threading.Thread class.
        """
        super().__init__(**threading_kwargs)
        self.is_token = is_token

    def run(self) -> None:
        """Runs the thread."""
        self.result = load_data(
            SecureGoogleOAuth2,
            is_token=self.is_token
        )

class SaveCookieThread(threading.Thread):
    """Thread to securely save the cookie to a file."""
    def __init__(self, cookie: dict, website: str, save_locally: bool, **threading_kwargs) -> None:
        """Constructor for the SaveCookieThread class.

        Args:
            cookie (dict):
                The cookie to save.
            website (str):
                The website to save the cookie for.
            save_locally (bool):
                Whether to save the cookie locally or on Cultured Downloader API.
            threading_kwargs (dict):
                The keyword arguments for the threading.Thread class.
        """
        super().__init__(**threading_kwargs)
        self.cookie = cookie
        self.website = website
        self.readable_website = website_to_readable_format(self.website)
        self.save_locally = save_locally
        self.result = None

    def run(self) -> None:
        """Runs the thread."""
        self.result = save_data(
            SecureCookie,
            save_key_locally=self.save_locally,
            website=self.website, 
            cookie_data=self.cookie
        )

class LoadCookieThread(threading.Thread):
    """Thread to securely load the cookie from a file."""
    def __init__(self, website: str, **threading_kwargs):
        """Constructor for the LoadCookieThread class.

        Args:
            website (str):
                The website to load the cookie for.
            threading_kwargs (dict):
                The keyword arguments for the threading.Thread class.
        """
        super().__init__(**threading_kwargs)
        self.website = website
        self.readable_website = website_to_readable_format(self.website)
        self.result = None

    def run(self) -> None:
        """Runs the thread."""
        self.result = load_data(
            SecureCookie, 
            website=self.website
        )

def load_cookies(*websites: list[str]) -> list[LoadCookieThread]:
    """Loads the cookie from the user's machine.

    Args:
        websites (list[str]):
            The websites to load the cookies for.

    Returns:
        list[LoadCookieThread]:
            The list of LoadCookieThread objects that have finished loading the cookies.
    """
    threads_arr: list[SaveCookieThread] = []
    for website in websites:
        cookie_path = convert_website_to_path(website)
        if (not cookie_path.exists() or not cookie_path.is_file()):
            continue

        thread = LoadCookieThread(website=website)
        thread.start()
        threads_arr.append(thread)

    for thread in threads_arr:
        thread.join()
    return threads_arr

def save_cookies(*login_results: Union[tuple[dict, str, bool], None]) -> None:
    """Saves the cookies to the user's machine in separate threads if the user chose to do so.

    Args:
        login_results (list[tuple[dict, str, bool]]):
            The login result from the website.

    Returns:
        None
    """
    threads_arr: list[SaveCookieThread] = []
    with Spinner(
        message="Saving cookies...",
        colour="light_yellow",
        spinner_position="left",
        spinner_type="arc"
    ):
        for result in login_results:
            if (not isinstance(result, tuple) or len(result) != 3):
                continue

            thread_task = SaveCookieThread(
                cookie=result[0], 
                website=result[1], 
                save_locally=result[2]
            )
            thread_task.start()
            threads_arr.append(thread_task)

        for thread in threads_arr:
            thread.join()

    for thread in threads_arr:
        if (not thread.result):
            print_danger(f"Failed to save {thread.readable_website} cookie.")
        else:
            print_success(f"Successfully saved {thread.readable_website} cookie.")

def save_google_oauth_json(*json_data: tuple[tuple[Union[dict, str]], bool]) -> None:
    """Save the Google OAuth2 JSON data to the user's machine.

    Args:
        *json_data (tuple[tuple[dict | str], bool]):
            An iterable of tuple of the JSON data to save and a boolean to indicate if it is a secret token or not.

    Returns:
        None
    """
    save_key_locally = save_key_prompt()
    threads_arr: list[SaveGoogleOAuth2Thread] = []
    with Spinner(
        message="Saving Google OAuth2 JSON...",
        colour="light_yellow",
        spinner_position="left",
        spinner_type="arc"
    ):
        for data, is_token in json_data:
            if (not isinstance(data, dict) and not isinstance(data, str)):
                continue

            thread_task = SaveGoogleOAuth2Thread(
                client_data=data,
                is_token=is_token,
                save_locally=save_key_locally
            )
            thread_task.start()
            threads_arr.append(thread_task)

        for thread in threads_arr:
            thread.join()

    for thread in threads_arr:
        if (thread.is_token):
            file_type = "Secret Token"
        else:
            file_type = "Client Secret"

        if (not thread.result):
            print_danger(
                f"Could not save your Google OAuth2 {file_type} JSON data either due to " \
                "connectivity issues or a problem with Cultured Downloader API."
            )
        else:
            print_success(f"Successfully saved Google OAuth2 {file_type} JSON data.")

@Spinner(
    message="Loading Google OAuth2 JSON (if found)...",
    colour="light_yellow",
    spinner_position="left",
    spinner_type="arc"
)
def load_google_oauth_json(get_client: Optional[bool] = True, get_token: Optional[bool] = True) -> Union[dict, tuple[dict, dict]]:
    """Load the Google OAuth2 JSON data from the user's machine.

    Args:
        get_client (bool, Optional):
            Whether to get the client secret JSON data. (Default: True)
        get_token (bool, Optional):
            Whether to get the secret token JSON data. (Default: True)

    Returns:
        dict | tuple[dict, dict]:
            The Google OAuth2 JSON data.
    """
    if (not get_client and not get_token):
        raise ValueError("You must get either the client secret or secret token JSON data.")

    path_arr = []
    if (get_client):
        path_arr.append(C.GOOGLE_OAUTH_CLIENT_SECRET)
    if (get_token):
        path_arr.append(C.GOOGLE_OAUTH_CLIENT_TOKEN)

    threads_arr: list[LoadGoogleOAuth2Thread] = []
    for file_path in path_arr:
        if (not file_path.exists() or not file_path.is_file()):
            continue

        is_token = (file_path == C.GOOGLE_OAUTH_CLIENT_TOKEN)
        thread = LoadGoogleOAuth2Thread(is_token=is_token)
        thread.start()
        threads_arr.append(thread)

    for thread in threads_arr:
        thread.join()

    google_token = google_client = None
    for thread in threads_arr:
        if (thread.is_token and thread.result):
            google_token = thread.result
        elif (not thread.is_token and thread.result):
            google_client = thread.result

    if (get_token and get_client):
        return (google_token, google_client)
    elif (get_token and not get_client):
        return google_token
    else:
        return google_client

__all__ = [
    "SecureCookie",
    "SecureGoogleOAuth2",
    "SaveCookieThread",
    "LoadCookieThread",
    "SaveGoogleOAuth2Thread",
    "LoadGoogleOAuth2Thread",
    "save_data",
    "load_data",
    "save_cookies",
    "load_cookies",
    "save_google_oauth_json",
    "load_google_oauth_json",
    "convert_website_to_path"
]

# test codes
if (__name__ == "__main__"):
    s = SecureCookie("pixiv_fanbox")
    print(s.data)