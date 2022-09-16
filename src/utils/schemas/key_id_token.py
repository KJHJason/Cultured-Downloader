# import Python's standard libraries
import base64
import binascii

# import third-party libraries
from pydantic import BaseModel, validator

class KeyIdToken(BaseModel):
    """This class is used to validate the key-id-token.json file."""
    key_id_token: str

    @validator("key_id_token")
    def precheck_if_is_valid_jwt(cls, value: str) -> str:
        """Do a simple pre-check if the key-id-token is a valid JWT."""
        jwt_parts = value.split(sep=".")
        if (len(jwt_parts) != 3):
            raise ValueError("The key_id_token does not have a valid JWT format!")

        for part in jwt_parts:
            try:
                base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)) # add missing padding
            except (binascii.Error, TypeError, ValueError):
                raise ValueError("The key_id_token is not base64 encoded!")

        return value