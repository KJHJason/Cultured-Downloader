__author__ = "KJHJason"
__copyright__ = "Copyright 2022 KJHJason"
__license__ = "MIT License"
__version__ = "2.0.1"

# Import Third-party Libraries
from Crypto.Random import get_random_bytes

# Import Standard Libraries
from base64 import b64encode
from random import randint

class EncryptedData:
    """
    Used for data encapsulation.

    Note that this class do not have any setter methods since this is used for encrypting the cookie data and will be overwritten every time when saving the cookie to the user's PC.
    """
    def __init__(self, data):
        self.__encryptedData = data
        self.__hints = None
        self.obfuscate()
    
    def get_encrypted_data(self):
        return self.deobfuscate_data()
    
    def obfuscate(self):
        randomBytes = b64encode(get_random_bytes(self.get_random_number())).decode()
        self.__hints = len(randomBytes)
        self.__encryptedData["cipherText"] += randomBytes

    def deobfuscate_data(self):
        copyOfEncryptedData = self.__encryptedData.copy()
        copyOfEncryptedData["cipherText"] = copyOfEncryptedData["cipherText"][:-self.__hints]
        return copyOfEncryptedData

    @staticmethod
    def get_random_number():
        return randint(80, 150)