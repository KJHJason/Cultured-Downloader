# Import Standard Libraries
import secrets
from typing import Union, Optional, Callable

# import local files
if (__package__ is None or __package__ == ""):
    from logger import logger
    from errors import APIServerError
    from constants import CONSTANTS as C
    from schemas.api_response import APIPublicKeyResponse
    from functional import validate_schema
else:
    from .logger import logger
    from .errors import APIServerError
    from .constants import CONSTANTS as C
    from .schemas.api_response import APIPublicKeyResponse
    from .functional import validate_schema

# Import Third-party Libraries
import httpx
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa, types
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def generate_rsa_key_pair() -> tuple[bytes, bytes]:
    """Generates a 2048 bits private and public key pair.

    Returns:
        A tuple containing the private and public keys (bytes).
            (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, # as recommended by the cryptography library documentation
        key_size=4096, # gives more lee-way for future-proofing and larger data sizes
    )
    public_key = private_key.public_key()
    return (
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
    )

def convert_str_to_digest_method(digest_method: str | None) -> hashes.HashAlgorithm:
    """Converts a string to a digest method

    Args:
        digest_method (str): 
            The digest method to convert to a callable.
            Valid values are "sha1", "sha256", "sha384", "sha512".
            If the digest method is not valid, the default digest method will be used.

    Returns:
        The digest method as a callable (cryptography.hazmat.primitives.hashes.HashAlgorithm).
    """
    if (digest_method is None):
        return hashes.SHA512
    elif (isinstance(digest_method, str)):
        digest_method = digest_method.lower()
    else:
        raise TypeError("digest_method must be a string!")

    if (digest_method == "sha1"):
        return hashes.SHA1
    elif (digest_method == "sha256"):
        return hashes.SHA256
    elif (digest_method == "sha384"):
        return hashes.SHA384
    elif (digest_method == "sha512"):
        return hashes.SHA512
    else:
        raise ValueError("digest_method must be one of the following: SHA1, SHA256, SHA384, SHA512")

def rsa_encrypt(plaintext: Union[str, bytes], digest_method: Optional[Callable] = hashes.SHA512) -> bytes:
    """Encrypts a plaintext using the public key (RSA-OAEP-SHA) from Cultured Downloader API.

    Args:
        plaintext (str|bytes): 
            The plaintext to encrypt.
        digest_method (cryptography.hazmat.primitives.hashes.HashAlgorithm):
            The hash algorithm to use for the encryption (defaults to SHA512).

    Returns:
        The encrypted plaintext (bytes).

    Raises:
        TypeError:
            If the digest method is not a subclass of cryptography.hazmat.primitives.hashes.HashAlgorithm.
        Exception:
            If the JSON response from the Cultured Downloader API does not match the schema or the response status code was not 200 OK.
    """
    if (isinstance(digest_method, str)):
        digest_method = convert_str_to_digest_method(digest_method)
    elif (not issubclass(digest_method, hashes.HashAlgorithm)):
        raise TypeError("digest_method must be a subclass of cryptography.hazmat.primitives.hashes.HashAlgorithm")

    json_data = {
        "algorithm": "rsa",
        "digest_method": digest_method.name,
    }
    with httpx.Client(headers=C.JSON_REQ_HEADERS, http2=True, timeout=30) as client:
        try:
            res = client.post(f"{C.API_URL}/public-key", json=json_data)
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
            logger.error(f"httpx error while retrieving API's public key:\n{e}")
            raise

    if (res.status_code != 200):
        raise APIServerError(f"Server Response: {res.status_code}\n{res.text}")

    res = res.json()
    if (not validate_schema(schema=APIPublicKeyResponse, data=res)):
        raise APIServerError("Invalid json response from Cultured Downloader website")

    public_key = serialization.load_pem_public_key(
        data=res["public_key"].encode("utf-8"), 
        backend=default_backend()
    )

    if (isinstance(plaintext, str)):
        plaintext = plaintext.encode("utf-8")

    # Construct the padding
    hash_algo = digest_method()
    mgf = padding.MGF1(algorithm=hash_algo)
    pad = padding.OAEP(mgf=mgf, algorithm=hash_algo, label=None)

    # Encrypt the plaintext using the public key
    return public_key.encrypt(plaintext=plaintext, padding=pad)

def rsa_decrypt(ciphertext: bytes, private_key: str | types.PRIVATE_KEY_TYPES,
                digest_method: Optional[Union[Callable, str]] = hashes.SHA512, decode: Optional[bool] = False) -> Union[str, bytes]:
    """Decrypts a ciphertext using the private key (RSA-OAEP-SHA) that was generated by generate_rsa_key_pair().

    Args:
        ciphertext (bytes): 
            The ciphertext to decrypt.
        digest_method (str|cryptography.hazmat.primitives.hashes.HashAlgorithm):
            The hash algorithm to use for the decryption (defaults to SHA512).
        decode (bool):
            Whether to decode the decrypted plaintext to a string (defaults to False).

    Returns:
        The decrypted ciphertext (bytes|str).

    Raises:
        TypeError:
            If the digest method is not a subclass of cryptography.hazmat.primitives.hashes.HashAlgorithm or
            the private key is not a subclass of cryptography.hazmat.primitives.asymmetric.rsa.RSAprivate_key.
    """
    if (isinstance(digest_method, str)):
        digest_method = convert_str_to_digest_method(digest_method)
    elif (not issubclass(digest_method, hashes.HashAlgorithm)):
        raise TypeError("digest_method must be a subclass of cryptography.hazmat.primitives.hashes.HashAlgorithm")

    if (isinstance(private_key, str)):
        # Extract and parse the public key as a PEM-encoded RSA private key
        private_key = serialization.load_pem_private_key(
            data=private_key.encode("utf-8"), 
            password=None,
            backend=default_backend()
        )
    elif (not isinstance(private_key, types.PRIVATE_KEY_TYPES)):
        raise TypeError("private_key must be an instance of cryptography.hazmat.primitives.asymmetric.types.PRIVATE_KEY_TYPES")

    # Construct the padding
    hash_algo = digest_method()
    mgf = padding.MGF1(algorithm=hash_algo)
    pad = padding.OAEP(mgf=mgf, algorithm=hash_algo, label=None)

    # Decrypt the ciphertext using the private key
    ciphertext = private_key.decrypt(ciphertext=ciphertext, padding=pad)
    return ciphertext.decode("utf-8") if (decode) else ciphertext

def generate_chacha20_key() -> bytes:
    """Generates a 256-bits ChaCha20 key.

    Returns:
        The ChaCha20 key (bytes).
    """
    return secrets.token_bytes(32)

def generate_chacha20_nonce() -> bytes:
    """Generates a 96-bits ChaCha20 nonce.

    Returns:
        The ChaCha20 nonce (bytes).
    """
    return secrets.token_bytes(12)

def chacha_encrypt(plaintext: Union[str, bytes], key: bytes) -> tuple[bytes, bytes]:
    """Encrypts a plaintext using the ChaCha20-Poly1305 algorithm.

    Args:
        plaintext (str|bytes): 
            The plaintext to encrypt.
        key (bytes): 
            The key to use for the encryption.

    Returns:
        The encrypted plaintext (bytes) and the nonce used.
        (ciphertext, nonce)
    """
    if (isinstance(plaintext, str)):
        plaintext = plaintext.encode("utf-8")

    # Construct the cipher
    chacha = ChaCha20Poly1305(key=key)

    # Encrypt the plaintext
    nonce = secrets.token_bytes(12)
    ciphertext = chacha.encrypt(nonce=nonce, data=plaintext, associated_data=C.TAG)

    return ciphertext, nonce

def chacha_decrypt(ciphertext: bytes, key: bytes, nonce: bytes, decode: Optional[bool] = False) -> bytes:
    """Decrypts a ciphertext using the ChaCha20-Poly1305 algorithm.

    Args:
        ciphertext (bytes): 
            The ciphertext to decrypt.
        key (bytes): 
            The key to use for the decryption.
        nonce (bytes): 
            The nonce to use for the decryption.
        decode (bool):
            Whether to decode the decrypted plaintext to a string (defaults to False).

    Returns:
        The decrypted ciphertext (bytes | str).
    """
    # Construct the cipher
    chacha = ChaCha20Poly1305(key=key)

    # Decrypt the ciphertext
    plaintext = chacha.decrypt(nonce=nonce, data=ciphertext, associated_data=C.TAG)

    return plaintext.decode("utf-8") if (decode) else plaintext