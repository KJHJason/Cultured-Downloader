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
	AiSearchMode       int
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

	PixivAiSearchAllow
	PixivAiSearchFilter

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

func ConvertArtworkTypeForBackend(artworkType int) string {
	switch artworkType {
	case PixivArtworkTypeIllustAndUgoira:
		return "illust_and_ugoira"
	case PixivArtworkTypeManga:
		return "manga"
	case PixivArtworkTypeAll:
		return "all"
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

func ConvertRatingModeForBackend(ratingMode int) string {
	switch ratingMode {
	case PixivRatingModeR18:
		return "r18"
	case PixivRatingModeSafe:
		return "safe"
	case PixivRatingModeAll:
		return "all"
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

func ConvertSearchModeForBackend(searchMode int) string {
	switch searchMode {
	case PixivSearchModeTag:
		return "s_tag"
	case PixivSearchModeTagFull:
		return "s_tag_full"
	case PixivSearchModeTC:
		return "s_tc"
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

func ConvertSortOrderForBackend(sortOrder int) string {
	switch sortOrder {
	case PixivSortOrderDate:
		return "date"
	case PixivSortOrderDateDesc:
		return "date_d"
	case PixivSortOrderPopular:
		return "popular"
	case PixivSortOrderPopularDesc:
		return "popular_d"
	case PixivSortOrderPopularMale:
		return "popular_male"
	case PixivSortOrderPopularMaleDesc:
		return "popular_male_d"
	case PixivSortOrderPopularFemale:
		return "popular_female"
	case PixivSortOrderPopularFemaleDesc:
		return "popular_female_d"
	default:
		return UnknownValue
	}
}

// Note: can be used for backend as well
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

func GetReadableAiSearchMode(aiSearchMode int) string {
	switch aiSearchMode {
	case PixivAiSearchAllow:
		return "Allow"
	case PixivAiSearchFilter:
		return "Filter"
	}
	return UnknownValue
}

func ConvertAiSearchModeForBackend(aiSearchMode int) int {
	// For references...
	//Mobile API:
	//- 0: Filter AI works
	//- 1: Display AI works
	//Web API:
	//- 0: Display AI works
	//- 1: Filter AI works
	//
	// Since the backend logic for PixivMobile will invert the int
	// based off the web API value, just return the web API value.
	switch aiSearchMode {
	case PixivAiSearchAllow:
		return 0
	case PixivAiSearchFilter:
		return 1
	}
	return -1
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
		AiSearchMode:       a.GetIntWithFallback(constants.PIXIV_AI_SEARCH_MODE_KEY, 24),
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

	if GetReadableAiSearchMode(p.AiSearchMode) == UnknownValue {
		p.AiSearchMode = PixivAiSearchAllow
	}
	if err = a.SetInt(constants.PIXIV_AI_SEARCH_MODE_KEY, p.AiSearchMode); err != nil {
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
