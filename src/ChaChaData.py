class ChaChaData:
    """
    Used for data encapsulation.

    Note that this class only has one getter method as the cookie files will be overwritten.

    Hence, not needing any setter methods.
    """
    def __init__(self, data):
        self.__encrypted_data = data
    
    def get_encrypted_data(self):
        return self.__encrypted_data