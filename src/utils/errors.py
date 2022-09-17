class CulturedDownloaderBaseError(Exception):
    """The base exception for Cultured Downloader."""
    pass

class FailedToDownloadError(CulturedDownloaderBaseError):
    """Exception raised when a download fails."""
    pass

class APIServerError(CulturedDownloaderBaseError):
    """Exception raised when the API server returns an error."""
    pass

class ChangedHTMLStructureError(CulturedDownloaderBaseError):
    """Exception raised when the HTML structure of the website has changed 
    in which the user has to raise an issue on GitHub."""
    pass