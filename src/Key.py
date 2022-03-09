__author__ = "KJHJason"
__copyright__ = "Copyright 2022 KJHJason"
__credits__ = ["KJHJason"]
__license__ = "MIT License"
__version__ = "1.00"

from cryptography.fernet import Fernet

class Key:
    def __init__(self):
        self.__decKey = self.get_key()
    
    def get_decKey(self):
        return self.__decKey
    def update_decKey(self):
        self.__decKey = self.get_key()
    
    @staticmethod
    def get_key():
        return Fernet.generate_key()