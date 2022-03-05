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