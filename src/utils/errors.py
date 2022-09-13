class CulturedDownloaderBaseError(Exception):
    """The base exception for Cultured Downloader."""
    pass

class FailedToDownload(CulturedDownloaderBaseError):
    """Exception raised when a download fails."""
    pass

class APIServerError(CulturedDownloaderBaseError):
    """Exception raised when the API server returns an error."""
    pass