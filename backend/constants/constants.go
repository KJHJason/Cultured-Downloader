package constants

import (
	"github.com/KJHJason/Cultured-Downloader-Logic/constants"
)

const (
	PROGRAM_NAME                 = "Cultured Downloader"
	PROGRAM_VER                  = "5.2.0a"
	CATCH_SIGINT                 = false
	LOCAL_USER_ASSET_DIR_NAME    = "assets"
	LANGUAGE_KEY                 = "lang"
	HASH_OF_MASTER_PASS_HASH_KEY = "master-password-hash"
	MASTER_PASS_SALT_KEY         = "master-password-salt"
	DARK_MODE_KEY                = "dark-mode"
	USERNAME_KEY                 = "username"
	USER_AGENT_KEY               = "user-agent"
	PROFILE_PIC_PATH_KEY         = "profile-pic-path"
	DOWNLOAD_KEY                 = "download"
	FFMPEG_KEY                   = "ffmpeg"
	USE_CACHE_DB_KEY             = "use-cache-db"

	// For wails file dialog
	// https://github.com/search?q=repo%3Awailsapp%2Fwails+%22shellItem+is+nil%22&type=code
	// https://github.com/wailsapp/wails/blob/1fb6403e7dfc266b952dbfd1484aeaaa0f66d6f1/v2/internal/go-common-file-dialog/cfd/iShellItemArray.go#L60
	WAILS_FILE_NONE_SELECTED = "shellItem is nil"

	// Platform names
	FANTIA       = constants.FANTIA
	PIXIV        = constants.PIXIV
	PIXIV_FANBOX = constants.PIXIV_FANBOX
	KEMONO       = constants.KEMONO

	GDRIVE_API_KEY_KEY       = "gdrive-api-key"
	GDRIVE_SERVICE_ACC_KEY   = "gdrive-service-acc"
	GDRIVE_CLIENT_SECRET_KEY = "gdrive-client-secret"
	GDRIVE_OAUTH_TOKEN_KEY   = "gdrive-oauth-token"

	DL_THUMBNAIL_KEY      = "dl-thumbnail"
	DL_IMAGES_KEY         = "dl-images"
	DL_ATTACHMENT_KEY     = "dl-attachments"
	OVERWRITE_FILES_KEY   = "overwrite-files"
	DL_GDRIVE_KEY         = "dl-gdrive"
	DETECT_OTHER_URLS_KEY = "detect-other-urls"

	FANTIA_ORGANISE_IMAGES_KEY = "fantia-organise-images"
	FANTIA_COOKIE_VALUE_KEY    = "fantia-cookie-value"
	FANTIA_COOKIE_JSON_KEY     = "fantia-cookie-json"
	FANTIA_COOKIE_TXT_KEY      = "fantia-cookie-txt"

	PIXIV_FANBOX_COOKIE_VALUE_KEY = "fanbox-cookie-value"
	PIXIV_FANBOX_COOKIE_JSON_KEY  = "fanbox-cookie-json"
	PIXIV_FANBOX_COOKIE_TXT_KEY   = "fanbox-cookie-txt"

	PIXIV_MOBILE_REFRESH_TOKEN_KEY = "pixiv-mobile-refresh-token"
	PIXIV_COOKIE_VALUE_KEY         = "pixiv-cookie-value"
	PIXIV_COOKIE_JSON_KEY          = "pixiv-cookie-json"
	PIXIV_COOKIE_TXT_KEY           = "pixiv-cookie-txt"
	PIXIV_ARTWORK_TYPE_KEY         = "pixiv-artwork-type"
	PIXIV_DELETE_UGOIRA_ZIP_KEY    = "pixiv-delete-ugoira-zip"
	PIXIV_RATING_MODE_KEY          = "pixiv-rating-mode"
	PIXIV_SEARCH_MODE_KEY          = "pixiv-search-mode"
	PIXIV_AI_SEARCH_MODE_KEY       = "pixiv-ai-search-mode"
	PIXIV_SORT_ORDER_KEY           = "pixiv-sort-order"
	PIXIV_UGOIRA_OUTPUT_FORMAT_KEY = "pixiv-ugoira-output-format"
	PIXIV_UGOIRA_QUALITY_KEY       = "pixiv-ugoira-quality"

	KEMONO_COOKIE_VALUE_KEY = "kemono-cookie-value"
	KEMONO_COOKIE_JSON_KEY  = "kemono-cookie-json"
	KEMONO_COOKIE_TXT_KEY   = "kemono-cookie-txt"

	// For download workers
	FANTIA_WORKERS       = 2
	PIXIV_WORKERS        = 1
	PIXIV_FANBOX_WORKERS = 1
	KEMONO_WORKERS       = 1
)
