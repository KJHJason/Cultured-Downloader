package constants

import (
	"os"
	"path/filepath"
)

const (
	PROGRAM_NAME                = "Cultured Downloader"
	DEFAULT_PERM                = 0755
	LOCAL_USER_ASSET_DIR_NAME   = "assets"
	LANGUAGE_KEY                = "lang"
	// TODO: uppercase all consts
	HashOfMasterPasswordHashKey = "master-password-hash"
	MasterPasswordSaltKey       = "master-password-salt"
	DarkModeKey                 = "dark-mode"
	UsernameKey                 = "username"
	UserAgentKey                = "user-agent"
	ProfilePicPathKey           = "profile-pic-path"
	DOWNLOAD_KEY                = "download"

	// Platform names
	Fantia      = "fantia"
	Pixiv       = "pixiv"
	PixivFanbox = "pixiv_fanbox"
	Kemono      = "kemono"

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
	FantiaCookieJsonKey   = "fantia-cookie-json"
	FantiaCookieTxtKey    = "fantia-cookie-txt"

	PixivFanboxCookieValueKey = "fanbox-cookie-value"
	PixivFanboxCookieJsonKey  = "fanbox-cookie-json"
	PixivFanboxCookieTxtKey   = "fanbox-cookie-txt"

	PixivCookieValueKey        = "pixiv-cookie-value"
	PixivCookieJsonKey         = "pixiv-cookie-json"
	PixivCookieTxtKey          = "pixiv-cookie-txt"
	PixivArtworkTypeKey        = "pixiv-artwork-type"
	PixivDeleteUgoiraZipKey    = "pixiv-delete-ugoira-zip"
	PixivRatingModeKey         = "pixiv-rating-mode"
	PixivSearchModeKey         = "pixiv-search-mode"
	PixivSortOrderKey          = "pixiv-sort-order"
	PixivUgoiraOutputFormatKey = "pixiv-ugoira-output-format"
	PixivUgoiraQualityKey      = "pixiv-ugoira-quality"

	KemonoCookieValueKey = "kemono-cookie-value"
	KemonoCookieJsonKey  = "kemono-cookie-json"
	KemonoCookieTxtKey   = "kemono-cookie-txt"

	// For download workers
	FANTIA_WORKERS       = 2
	PIXIV_WORKERS        = 1
	PIXIV_FANBOX_WORKERS = 1
	KEMONO_WORKERS       = 1
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
	os.MkdirAll(UserConfigDir, DEFAULT_PERM)
}
