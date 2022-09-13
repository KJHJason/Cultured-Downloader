# import third-party libraries
from pydantic import BaseModel

class APICsrfResponse(BaseModel):
    """This class is used to validate the API's response after retrieving a CSRF token."""
    csrf_token: str

class APIKeyResponse(BaseModel):
    """This class is used to validate the API's response after retrieving the user's secret key."""
    secret_key: str

class APIKeyIDResponse(BaseModel):
    """This class is used to validate the API's response after saving the user's secret key."""
    key_id_token: str

class APIPublicKeyResponse(BaseModel):
    """This class is used to validate the API's response after retrieving the API's public key."""
    public_key: str