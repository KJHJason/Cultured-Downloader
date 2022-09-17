# import Python's standard libraries
import enum
from typing import Optional

# import third-party libraries
from pydantic import BaseModel, validator, AnyHttpUrl

# import local files
from utils.constants import CONSTANTS as C

@enum.unique
class AuthURI(str, enum.Enum):
    """This class is used to validate the Google OAuth 2.0 authorization URI."""
    AUTH_URI = "https://accounts.google.com/o/oauth2/auth"

@enum.unique
class TokenURI(str, enum.Enum):
    """This class is used to validate the Google OAuth 2.0 token URI."""
    TOKEN_URI = "https://oauth2.googleapis.com/token"

@enum.unique
class AuthProviderX509CertURL(str, enum.Enum):
    """This class is used to validate the Google OAuth 2.0 authentication provider's X.509 certificate URL."""
    AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"

class ClientBase(BaseModel):
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
    client_id: str
    project_id: str
    auth_uri: AuthURI
    token_uri: TokenURI
    auth_provider_x509_cert_url: AuthProviderX509CertURL
    client_secret: str
    redirect_uris: Optional[list[AnyHttpUrl]]
    javascript_origins: Optional[list[AnyHttpUrl]]

class ClientSecretBase(BaseModel):
    """This class is used to validate the client_secret.json file."""
    web: ClientSecretValues

class ClientToken(ClientBase):
    """This class is used to validate the client_token.json file."""
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]
    expiry: str

    @validator("scopes")
    def validate_scopes(cls, scopes: list[str]) -> list[str]:
        """This method is used to validate the scopes."""
        for scope in scopes:
            if (scope not in C.GOOGLE_OAUTH_SCOPES):
                raise ValueError(f"The scope '{scope}' is not allowed!")

        return scopes

    @validator("token")
    def validate_token(cls, token: str) -> str:
        """This method validates the token."""
        if (not token.startswith("ya29.")):
            raise ValueError("The token must start with 'ya29.'")
        return token

    @validator("refresh_token")
    def validate_refresh_token(cls, refresh_token: str) -> str:
        """This method validates the refresh token."""
        if (not refresh_token.startswith("1/")):
            raise ValueError("The refresh token must start with '1/'")
        return refresh_token