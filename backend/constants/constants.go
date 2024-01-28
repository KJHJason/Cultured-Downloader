package constants

import (
	"os"
	"path/filepath"
)

const (
	DefaultPerm = 0755
	LocalUserAssetDirName = "assets"
	MasterPasswordHashKey = "master-password-hash"
	DarkModeKey           = "dark-mode"

	GdriveApiKeyKey     = "gdrive-api-key"
	GdriveServiceAccKey = "gdrive-service-acc"

	DlThumbnailKey     = "dl-thumbnail"
	DlImagesKey        = "dl-images"
	DlAttachmentsKey   = "dl-attachments"
	DlGdriveKey        = "dl-gdrive"
	DetectOtherUrlsKey = "detect-other-urls"

	FantiaCookieValueKey = "fantia-cookie-value"
	FantiaCookiePathKey  = "fantia-cookie-path"
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
