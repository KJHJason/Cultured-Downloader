# Import Standard Libraries
import pathlib
import json

# import local files
if (__name__ == "__main__"):
    from crucial import install_dependency
else:
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

# import secrets
# testKey = secrets.token_bytes(nbytes=32)
# nonce = secrets.token_bytes(nbytes=16)

# AES_GCM = AESGCM(key=testKey)

# pt = "This is a plaintext message.".encode("utf-8")

# ct = AES_GCM.encrypt(nonce=nonce, data=pt, associated_data=None)
# print(ct)

# pt = AES_GCM.decrypt(nonce=nonce, data=ct, associated_data=None)
# print(pt)