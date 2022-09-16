# import Python's standard libraries
import enum
import pathlib
from typing import  Optional

# import third-party libraries
from pydantic import BaseModel, Field

@enum.unique
class Languages(str, enum.Enum):
    """This enum is used to store all the languages supported by the application."""
    # Only en is supported (considering jp)
    EN: str = "en"

@enum.unique
class ClientDigestMethod(str, enum.Enum):
    """This enum is used to store all the digest methods supported by Cultured Downloader API."""
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

class ConfigSchema(BaseModel):
    """This class is used to validate the config.json file."""
    download_directory: Optional[str] = Field(
        default=str(pathlib.Path.home().joinpath("Desktop", "cultured-downloader")),
    )
    language: Languages = Field(default=Languages.EN)
    client_digest_method: Optional[ClientDigestMethod] = None