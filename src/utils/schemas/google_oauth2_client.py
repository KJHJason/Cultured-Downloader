# import Python's standard libraries
from typing import Optional, Union

# import third-party libraries
from pydantic import BaseModel, validator, AnyHttpUrl

# For Google Drive API if 
# the user has added their credentials.json file
# If modifying the scopes, you will need to 
# delete the old token.json file.
# Google Drive API v3 scopes:
#   https://developers.google.com/identity/protocols/oauth2/scopes#drive
GOOGLE_OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/drive.readonly"
]

class ClientBase(BaseModel):
    client_id: str
    client_secret: str
    token_uri: str

    @validator("token_uri")
    def validate_token_uri(cls, value: str) -> str:
        """This method is used to validate the token URI."""
        if (value != "https://oauth2.googleapis.com/token"):
            raise ValueError("Invalid token URI")
        return value

    @validator("client_id")
    def validate_client_id(cls, value: str) -> str:
        """This method validates the client ID."""
        if (not value.endswith(".apps.googleusercontent.com")):
            raise ValueError("The client ID must end with '.apps.googleusercontent.com'")
        return value

    @validator("client_secret")
    def validate_client_secret(cls, client_secret: str) -> str:
        """This method is used to validate the client secret."""
        if (not client_secret.startswith("GOCSPX-")):
            raise ValueError("The client secret must start with 'GOCSPX-'")
        return client_secret

class ClientSecretValues(ClientBase):
    """This class is used to validate the values of client_secret.json file."""
    project_id: str
    auth_uri: str
    auth_provider_x509_cert_url: str
    redirect_uris: Optional[list[AnyHttpUrl]]
    javascript_origins: Optional[list[AnyHttpUrl]]

    @validator("auth_uri")
    def validate_auth_uri(cls, value: str) -> str:
        """This method is used to validate the authorization URI."""
        if (value != "https://accounts.google.com/o/oauth2/auth"):
            raise ValueError("Invalid authorization URI")
        return value

    @validator("auth_provider_x509_cert_url")
    def validate_auth_provider_x509_cert_url(cls, value: str) -> str:
        """This method is used to validate the authentication provider's X.509 certificate URL."""
        if (value != "https://www.googleapis.com/oauth2/v1/certs"):
            raise ValueError("Invalid authentication provider's X.509 certificate URL")
        return value

class ClientSecret(BaseModel):
    """This class is used to validate the client_secret.json file."""
    web: ClientSecretValues

class ClientToken(ClientBase):
    """This class is used to validate the client_token.json file."""
    token: Optional[str]
    refresh_token: str
    scopes: list[str]
    expiry: str

    @validator("scopes")
    def validate_scopes(cls, scopes: list[str]) -> list[str]:
        """This method is used to validate the scopes."""
        for scope in scopes:
            if (scope not in GOOGLE_OAUTH_SCOPE):
                raise ValueError(f"The scope '{scope}' is not allowed!")

        return scopes

    @validator("token")
    def validate_token(cls, token: Union[str, None]) -> str:
        """This method validates the token."""
        if (token is not None and not token.startswith("ya29.")):
            raise ValueError("The token must start with 'ya29.'")
        return token

    @validator("refresh_token")
    def validate_refresh_token(cls, refresh_token: str) -> str:
        """This method validates the refresh token."""
        if (not refresh_token.startswith("1/")):
            raise ValueError("The refresh token must start with '1/'")
        return refresh_token

__all__ = [
    "GOOGLE_OAUTH_SCOPE",
    "ClientSecret",
    "ClientToken"
]