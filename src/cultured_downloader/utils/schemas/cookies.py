# import Python's standard libraries
import enum
from typing import Optional

# import third-party libraries
from pydantic import BaseModel, validator

@enum.unique
class CookieDomain(str, enum.Enum):
    """This class is used to validate the domain of a cookie."""
    FANTIA = "fantia.jp"
    PIXIV_FANBOX = ".fanbox.cc"

@enum.unique
class CookieName(str, enum.Enum):
    """This class is used to validate the name of a cookie."""
    FANTIA = "_session_id"
    PIXIV_FANBOX = "FANBOXSESSID"

class CookieSchema(BaseModel):
    """This class is used to validate the saved cookie files."""
    domain: CookieDomain
    expiry: int
    httpOnly: bool
    name: CookieName
    path: str
    sameSite: Optional[str]
    secure: bool
    value: str

    @validator("httpOnly", "secure")
    def validate_httpOnly_and_secure(cls, value: bool) -> bool:
        """Validate the httpOnly and the secure attributes of a cookie."""
        if (not value):
            raise ValueError("The httpOnly attribute and the secure attribute of the cookie must be true!")
        return value

    @validator("path")
    def validate_path(cls, value: str) -> str:
        """Validate the path attribute of a cookie."""
        if (value != "/"):
            raise ValueError("path attribute of the cookie must be '/'!")
        return value