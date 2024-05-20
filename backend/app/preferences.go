package app

import (
	"fmt"

	cdlerrors "github.com/KJHJason/Cultured-Downloader-Logic/errors"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) GetDarkMode() bool {
	return a.appData.GetBool(constants.DARK_MODE_KEY)
}

func (a *App) SetDarkMode(darkMode bool) {
	a.appData.SetBool(constants.DARK_MODE_KEY, darkMode)
}

type preferences struct {
	DlPostThumbnail   bool
	DlPostImages      bool
	DlPostAttachments bool
	OverwriteFiles    bool

	DlGDrive         bool
	DetectOtherLinks bool
	UseCacheDb       bool

	// Fantia
	OrganisePostImages bool

	// Pixiv
	ArtworkType        int
	DeleteUgoiraZip    bool
	RatingMode         int
	SearchMode         int
	AiSearchMode       int
	SortOrder          int
	UgoiraOutputFormat int
	UgoiraQuality      int
}

func (a *App) GetPreferences() *preferences {
	// 0-51 for mp4, 0-63 for webm
	ugoiraQuality := a.appData.GetIntWithFallback(constants.PIXIV_UGOIRA_QUALITY_KEY, 10)
	if ugoiraQuality < 0 || ugoiraQuality > 63 {
		ugoiraQuality = 10
		a.appData.SetInt(constants.PIXIV_UGOIRA_QUALITY_KEY, ugoiraQuality)
	}

	pref := &preferences{
		DlPostThumbnail:   a.appData.GetBool(constants.DL_THUMBNAIL_KEY),
		DlPostImages:      a.appData.GetBool(constants.DL_IMAGES_KEY),
		DlPostAttachments: a.appData.GetBool(constants.DL_ATTACHMENT_KEY),
		OverwriteFiles:    a.appData.GetBool(constants.OVERWRITE_FILES_KEY),

		DlGDrive:         a.appData.GetBool(constants.DL_GDRIVE_KEY),
		DetectOtherLinks: a.appData.GetBool(constants.DETECT_OTHER_URLS_KEY),
		UseCacheDb:       a.appData.GetBoolWithFallback(constants.USE_CACHE_DB_KEY, true),

		OrganisePostImages: a.appData.GetBoolWithFallback(constants.FANTIA_ORGANISE_IMAGES_KEY, true),

		ArtworkType:        a.appData.GetIntWithFallback(constants.PIXIV_ARTWORK_TYPE_KEY, 3),
		DeleteUgoiraZip:    a.appData.GetBoolWithFallback(constants.PIXIV_DELETE_UGOIRA_ZIP_KEY, true),
		RatingMode:         a.appData.GetIntWithFallback(constants.PIXIV_RATING_MODE_KEY, 6),
		SearchMode:         a.appData.GetIntWithFallback(constants.PIXIV_SEARCH_MODE_KEY, 8),
		AiSearchMode:       a.appData.GetIntWithFallback(constants.PIXIV_AI_SEARCH_MODE_KEY, 24),
		SortOrder:          a.appData.GetIntWithFallback(constants.PIXIV_SORT_ORDER_KEY, 11),
		UgoiraOutputFormat: a.appData.GetIntWithFallback(constants.PIXIV_UGOIRA_OUTPUT_FORMAT_KEY, 18),
		UgoiraQuality:      ugoiraQuality,
	}
	return pref
}

func (a *App) GetDownloadDir() (string, error) {
	dlDirPath, err, _ := a.getDownloadDir()
	return dlDirPath, err
}

func (a *App) SetGeneralPreferences(p *preferences) error {
	if p == nil {
		return fmt.Errorf(
			"error %d: preferences is nil in SetGeneralPreferences()",
			cdlerrors.DEV_ERROR,
		)
	}

	var err error
	if err = a.appData.SetBool(constants.DL_THUMBNAIL_KEY, p.DlPostThumbnail); err != nil {
		return err
	}
	if err = a.appData.SetBool(constants.DL_IMAGES_KEY, p.DlPostImages); err != nil {
		return err
	}
	if err = a.appData.SetBool(constants.DL_ATTACHMENT_KEY, p.DlPostAttachments); err != nil {
		return err
	}
	if err = a.appData.SetBool(constants.OVERWRITE_FILES_KEY, p.OverwriteFiles); err != nil {
		return err
	}

	if err = a.appData.SetBool(constants.DL_GDRIVE_KEY, p.DlGDrive); err != nil {
		return err
	}
	if err = a.appData.SetBool(constants.DETECT_OTHER_URLS_KEY, p.DetectOtherLinks); err != nil {
		return err
	}

	if err = a.appData.SetBool(constants.USE_CACHE_DB_KEY, p.UseCacheDb); err != nil {
		return err
	}
	return nil
}
