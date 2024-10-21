package app

import (
	"fmt"
	"regexp"
	"time"

	"github.com/KJHJason/Cultured-Downloader-Logic/cdlerrors"
	"github.com/KJHJason/Cultured-Downloader-Logic/filters"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) GetDarkMode() bool {
	return a.appData.GetBool(constants.DARK_MODE_KEY)
}

func (a *App) SetDarkMode(darkMode bool) {
	a.appData.SetBool(constants.DARK_MODE_KEY, darkMode)
}

type Filters struct {
	// In bytes
	MinFileSize int64  `json:"MinFileSize"`
	MaxFileSize *int64 `json:"MaxFileSize"`

	FileExt []string `json:"FileExt"`

	// Unix time (ms)
	StartDate *int64 `json:"StartDate"`
	EndDate   *int64 `json:"EndDate"`

	FileNameRegex string `json:"FileNameRegex"`
}

func (f *Filters) ConvertUnixToTime() (startDate time.Time, endDate time.Time) {
	if f.StartDate == nil {
		startDate = time.Time{}
	} else {
		startDate = time.Unix(*f.StartDate, 0)
	}

	if f.EndDate == nil {
		endDate = time.Time{}
	} else {
		endDate = time.Unix(*f.EndDate, 0)
	}
	return startDate, endDate
}

func (f *Filters) ConverToCDLFilters() (*filters.Filters, error) {
	var maxFileSize int64
	if f.MaxFileSize == nil {
		maxFileSize = filters.NO_MAX_FILESIZE
	} else {
		maxFileSize = *f.MaxFileSize
	}

	startDate, endDate := f.ConvertUnixToTime()

	var fileNameFilter *regexp.Regexp
	if f.FileNameRegex != "" {
		var err error
		fileNameFilter, err = regexp.Compile(f.FileNameRegex)
		if err != nil {
			fmtErr := fmt.Errorf(
				"error %d: failed to parse %s into regex => %w",
				cdlerrors.INPUT_ERROR,
				f.FileNameRegex,
				err,
			)
			logger.MainLogger.Error(fmtErr.Error())
			return nil, fmtErr
		}
	}

	dlFilters := filters.Filters{
		MinFileSize: f.MinFileSize,
		MaxFileSize: maxFileSize,

		FileExt: f.FileExt,

		StartDate: startDate,
		EndDate:   endDate,

		FileNameFilter: fileNameFilter,
	}
	dlFilters.ConvertFileSizeFromMB()
	dlFilters.RemoveDuplicateFileExt()

	if err := dlFilters.ValidateArgs(); err != nil {
		fmtErr := fmt.Errorf(
			"error %d: download filters validations failed => %w",
			cdlerrors.INPUT_ERROR,
			err,
		)
		logger.MainLogger.Error(fmtErr.Error())
		return nil, fmtErr
	}
	return &dlFilters, nil
}

type Preferences struct {
	DlPostThumbnail   bool `json:"DlPostThumbnail"`
	DlPostImages      bool `json:"DlPostImages"`
	DlPostAttachments bool `json:"DlPostAttachments"`
	OverwriteFiles    bool `json:"OverwriteFiles"`

	DlGDrive         bool `json:"DlGDrive"`
	DetectOtherLinks bool `json:"DetectOtherLinks"`
	UseCacheDb       bool `json:"UseCacheDb"`

	// Fantia
	OrganisePostImages bool `json:"OrganisePostImages"`

	// Pixiv
	ArtworkType        int  `json:"ArtworkType"`
	DeleteUgoiraZip    bool `json:"DeleteUgoiraZip"`
	RatingMode         int  `json:"RatingMode"`
	SearchMode         int  `json:"SearchMode"`
	AiSearchMode       int  `json:"AiSearchMode"`
	SortOrder          int  `json:"SortOrder"`
	UgoiraOutputFormat int  `json:"UgoiraOutputFormat"`
	UgoiraQuality      int  `json:"UgoiraQuality"`
}

type GeneralPreferences struct {
	DlPostThumbnail   bool `json:"DlPostThumbnail"`
	DlPostImages      bool `json:"DlPostImages"`
	DlPostAttachments bool `json:"DlPostAttachments"`
	OverwriteFiles    bool `json:"OverwriteFiles"`

	DlGDrive         bool `json:"DlGDrive"`
	DetectOtherLinks bool `json:"DetectOtherLinks"`
	UseCacheDb       bool `json:"UseCacheDb"`
}

type FantiaPreferences struct {
	OrganisePostImages bool `json:"OrganisePostImages"`
}

type PixivPreferences struct {
	ArtworkType        int  `json:"ArtworkType"`
	DeleteUgoiraZip    bool `json:"DeleteUgoiraZip"`
	RatingMode         int  `json:"RatingMode"`
	SearchMode         int  `json:"SearchMode"`
	AiSearchMode       int  `json:"AiSearchMode"`
	SortOrder          int  `json:"SortOrder"`
	UgoiraOutputFormat int  `json:"UgoiraOutputFormat"`
	UgoiraQuality      int  `json:"UgoiraQuality"`
}

func (a *App) GetPreferences() *Preferences {
	// 0-51 for mp4, 0-63 for webm
	ugoiraQuality := a.appData.GetIntWithFallback(constants.PIXIV_UGOIRA_QUALITY_KEY, 10)
	if ugoiraQuality < 0 || ugoiraQuality > 63 {
		ugoiraQuality = 10
		a.appData.SetInt(constants.PIXIV_UGOIRA_QUALITY_KEY, ugoiraQuality)
	}

	pref := &Preferences{
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

func (a *App) SetGeneralPreferences(p *GeneralPreferences) error {
	if p == nil {
		return fmt.Errorf(
			"error %d: general preferences is nil in SetGeneralPreferences()",
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
