package constants

import (
	"os"
	"path/filepath"
)

const (
	DefaultPerm = 0755
	LocalUserAssetDirName = "assets"
	MasterPasswordHashKey = "masterPasswordHash"

	GdriveApiKeyKey     = "gdriveApiKey"
	GdriveServiceAccKey = "gdriveServiceAcc"

	DlThumbnailKey     = "dlThumbnail"
	DlImagesKey        = "dlImages"
	DlAttachmentsKey   = "dlAttachments"
	DlGdriveKey        = "dlGdrive"
	DetectOtherUrlsKey = "detectOtherUrls"

	FantiaCookieValueKey = "fantiaCookieValue"
	FantiaCookiePathKey  = "fantiaCookiePath"
)

var (
	UserConfigDir		string
	UserConfigDirErr	error
)

func init() {
	// Try to get the OS specific path to the user config directory
	UserConfigDir, UserConfigDirErr = os.UserConfigDir()
	if UserConfigDirErr != nil {
		panic(UserConfigDirErr)
	}

	// If we got the path, append the app name to it
	UserConfigDir = filepath.Join(UserConfigDir, "cultured.downloader")

	// Create the directory if it doesn't exist
	os.MkdirAll(UserConfigDir, DefaultPerm)
}
