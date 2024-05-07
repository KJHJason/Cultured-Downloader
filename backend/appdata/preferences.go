package appdata

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

type Preferences struct {
	DlPostThumbnail   bool
	DlPostImages      bool
	DlPostAttachments bool
	OverwriteFiles    bool

	DlGDrive         bool
	DetectOtherLinks bool

	// Pixiv
	ArtworkType        int
	DeleteUgoiraZip    bool
	RatingMode         int
	SearchMode         int
	SortOrder          int
	UgoiraOutputFormat int
	UgoiraQuality      uint8
}

const (
	None = iota
	PixivArtworkTypeIllustAndUgoira
	PixivArtworkTypeManga
	PixivArtworkTypeAll

	PixivRatingModeR18
	PixivRatingModeSafe
	PixivRatingModeAll

	PixivSearchModeTag
	PixivSearchModeTagFull
	PixivSearchModeTC

	PixivSortOrderDate
	PixivSortOrderDateDesc
	PixivSortOrderPopular
	PixivSortOrderPopularDesc
	PixivSortOrderPopularMale
	PixivSortOrderPopularMaleDesc
	PixivSortOrderPopularFemale
	PixivSortOrderPopularFemaleDesc

	PixivUgoiraOutputFormatGif
	PixivUgoiraOutputFormatApng
	PixivUgoiraOutputFormatWebp
	PixivUgoiraOutputFormatWebm
	PixivUgoiraOutputFormatMp4

	UnknownValue = "Unknown"
)

func GetReadableArtworkType(artworkType int) string {
	switch artworkType {
	case PixivArtworkTypeIllustAndUgoira:
		return "Illust and Ugoira"
	case PixivArtworkTypeManga:
		return "Manga"
	case PixivArtworkTypeAll:
		return "All"
	}
	return UnknownValue
}

func GetReadableRatingMode(ratingMode int) string {
	switch ratingMode {
	case PixivRatingModeR18:
		return "R-18"
	case PixivRatingModeSafe:
		return "Safe"
	case PixivRatingModeAll:
		return "All"
	}
	return UnknownValue
}

func GetReadableSearchMode(searchMode int) string {
	switch searchMode {
	case PixivSearchModeTag:
		return "Similar Tag Names"
	case PixivSearchModeTagFull:
		return "Tags"
	case PixivSearchModeTC:
		return "Title and Caption"
	}
	return UnknownValue
}

func GetReadableSortOrder(sortOrder int) string {
	switch sortOrder {
	case PixivSortOrderDate:
		return "Date"
	case PixivSortOrderDateDesc:
		return "Date (Descending)"
	case PixivSortOrderPopular:
		return "Popular"
	case PixivSortOrderPopularDesc:
		return "Popular (Descending)"
	case PixivSortOrderPopularMale:
		return "Popular (Male)"
	case PixivSortOrderPopularMaleDesc:
		return "Popular (Male/Descending)"
	case PixivSortOrderPopularFemale:
		return "Popular (Female)"
	case PixivSortOrderPopularFemaleDesc:
		return "Popular (Female/Descending)"
	}
	return UnknownValue
}

func GetReadableUgoiraFileFormat(format int) string {
	switch format {
	case PixivUgoiraOutputFormatGif:
		return ".gif"
	case PixivUgoiraOutputFormatApng:
		return ".apng"
	case PixivUgoiraOutputFormatWebp:
		return ".webp"
	case PixivUgoiraOutputFormatWebm:
		return ".webm"
	case PixivUgoiraOutputFormatMp4:
		return ".mp4"
	}
	return UnknownValue
}

func (a *AppData) GetPreferences() Preferences {
	// 0-51 for mp4, 0-63 for webm
	ugoiraQuality := a.GetInt(constants.PIXIV_UGOIRA_QUALITY_KEY)
	if ugoiraQuality < 0 || ugoiraQuality > 63 {
		ugoiraQuality = 0
	}

	pref := Preferences{
		DlPostThumbnail:   a.GetBool(constants.DL_THUMBNAIL_KEY),
		DlPostImages:      a.GetBool(constants.DL_IMAGES_KEY),
		DlPostAttachments: a.GetBool(constants.DL_ATTACHMENT_KEY),
		OverwriteFiles:    a.GetBool(constants.OVERWRITE_FILES_KEY),

		DlGDrive:         a.GetBool(constants.DL_GDRIVE_KEY),
		DetectOtherLinks: a.GetBool(constants.DETECT_OTHER_URLS_KEY),

		ArtworkType:        a.GetIntWithFallback(constants.PIXIV_ARTWORK_TYPE_KEY, 3),
		DeleteUgoiraZip:    a.GetBool(constants.PIXIV_DELETE_UGOIRA_ZIP_KEY),
		RatingMode:         a.GetIntWithFallback(constants.PIXIV_RATING_MODE_KEY, 6),
		SearchMode:         a.GetIntWithFallback(constants.PIXIV_SEARCH_MODE_KEY, 8),
		SortOrder:          a.GetIntWithFallback(constants.PIXIV_SORT_ORDER_KEY, 10),
		UgoiraOutputFormat: a.GetIntWithFallback(constants.PIXIV_UGOIRA_OUTPUT_FORMAT_KEY, 18),
		UgoiraQuality:      uint8(ugoiraQuality),
	}
	return pref
}

func (a *AppData) SetGeneralPreferences(p Preferences) error {
	var err error
	if err = a.SetBool(constants.DL_THUMBNAIL_KEY, p.DlPostThumbnail); err != nil {
		return err
	}
	if err = a.SetBool(constants.DL_IMAGES_KEY, p.DlPostImages); err != nil {
		return err
	}
	if err = a.SetBool(constants.DL_ATTACHMENT_KEY, p.DlPostAttachments); err != nil {
		return err
	}
	if err = a.SetBool(constants.OVERWRITE_FILES_KEY, p.OverwriteFiles); err != nil {
		return err
	}

	if err = a.SetBool(constants.DL_GDRIVE_KEY, p.DlGDrive); err != nil {
		return err
	}
	if err = a.SetBool(constants.DETECT_OTHER_URLS_KEY, p.DetectOtherLinks); err != nil {
		return err
	}
	return nil
}

func (a *AppData) SetPixivPreferences(p Preferences) error {
	if GetReadableArtworkType(p.ArtworkType) == UnknownValue {
		p.ArtworkType = PixivArtworkTypeIllustAndUgoira
	}

	var err error
	if err = a.SetInt(constants.PIXIV_ARTWORK_TYPE_KEY, p.ArtworkType); err != nil {
		return err
	}

	if err = a.SetBool(constants.PIXIV_DELETE_UGOIRA_ZIP_KEY, p.DeleteUgoiraZip); err != nil {
		return err
	}

	if GetReadableRatingMode(p.RatingMode) == UnknownValue {
		p.RatingMode = PixivRatingModeSafe
	}
	if err = a.SetInt(constants.PIXIV_RATING_MODE_KEY, p.RatingMode); err != nil {
		return err
	}

	if GetReadableSearchMode(p.SearchMode) == UnknownValue {
		p.SearchMode = PixivSearchModeTag
	}
	if err = a.SetInt(constants.PIXIV_SEARCH_MODE_KEY, p.SearchMode); err != nil {
		return err
	}

	if GetReadableSortOrder(p.SortOrder) == UnknownValue {
		p.SortOrder = PixivSortOrderDate
	}
	if err = a.SetInt(constants.PIXIV_SORT_ORDER_KEY, p.SortOrder); err != nil {
		return err
	}

	if GetReadableUgoiraFileFormat(p.UgoiraOutputFormat) == UnknownValue {
		p.UgoiraOutputFormat = PixivUgoiraOutputFormatGif
	}
	if err = a.SetInt(constants.PIXIV_UGOIRA_OUTPUT_FORMAT_KEY, p.UgoiraOutputFormat); err != nil {
		return err
	}

	// 0-51 for mp4, 0-63 for webm
	if p.UgoiraOutputFormat == PixivUgoiraOutputFormatMp4 && p.UgoiraQuality <= 51 {
		err = a.SetInt(constants.PIXIV_UGOIRA_QUALITY_KEY, int(p.UgoiraQuality))
	} else if p.UgoiraOutputFormat == PixivUgoiraOutputFormatWebm && p.UgoiraQuality <= 63 {
		err = a.SetInt(constants.PIXIV_UGOIRA_QUALITY_KEY, int(p.UgoiraQuality))
	}
	return err
}
