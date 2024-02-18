package constants

import (
	"os"
	"path/filepath"
)

const (
	DefaultPerm                 = 0755
	LocalUserAssetDirName       = "assets"
	HashOfMasterPasswordHashKey = "master-password-hash"
	MasterPasswordSaltKey       = "master-password-salt"
	DarkModeKey                 = "dark-mode"
	UsernameKey                 = "username"
	ProfilePicPathKey           = "profile-pic-path"

	// Platform names
	Fantia = "fantia"
	Pixiv  = "pixiv"
	PixivFanbox = "pixiv_fanbox"
	Kemono = "kemono"

	GdriveApiKeyKey     = "gdrive-api-key"
	GdriveServiceAccKey = "gdrive-service-acc"

	DlThumbnailKey     = "dl-thumbnail"
	DlImagesKey        = "dl-images"
	DlAttachmentsKey   = "dl-attachments"
	OverwriteFilesKey  = "overwrite-files"
	DlGdriveKey        = "dl-gdrive"
	DetectOtherUrlsKey = "detect-other-urls"

	AutoSolveReCaptchaKey = "auto-solve-recaptcha"
	FantiaCookieValueKey  = "fantia-cookie-value"

	PixivFanboxCookieValueKey = "pixiv-fanbox-cookie-value"

	PixivCookieValueKey        = "pixiv-cookie-value"
	PixivArtworkTypeKey        = "pixiv-artwork-type"
	PixivDeleteUgoiraZipKey    = "pixiv-delete-ugoira-zip"
	PixivRatingModeKey         = "pixiv-rating-mode"
	PixivSearchModeKey         = "pixiv-search-mode"
	PixivSortOrderKey          = "pixiv-sort-order"
	PixivUgoiraOutputFormatKey = "pixiv-ugoira-output-format"
	PixivUgoiraQualityKey      = "pixiv-ugoira-quality"

	KemonoCookieValueKey = "kemono-cookie-value"
)

var (
	UserConfigDir    string
	UserConfigDirErr error
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
