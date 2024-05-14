package app

import (
	"fmt"

	cdlerrors "github.com/KJHJason/Cultured-Downloader-Logic/errors"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

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

func (a *App) SetPixivPreferences(p *preferences) error {
	if p == nil {
		return fmt.Errorf(
			"pixiv error %d: preferences is nil in SetPixivPreferences()",
			cdlerrors.DEV_ERROR,
		)
	}

	if getReadableArtworkType(p.ArtworkType) == UnknownValue {
		p.ArtworkType = PixivArtworkTypeIllustAndUgoira
	}

	var err error
	if err = a.appData.SetInt(constants.PIXIV_ARTWORK_TYPE_KEY, p.ArtworkType); err != nil {
		return err
	}

	if err = a.appData.SetBool(constants.PIXIV_DELETE_UGOIRA_ZIP_KEY, p.DeleteUgoiraZip); err != nil {
		return err
	}

	if getReadableRatingMode(p.RatingMode) == UnknownValue {
		p.RatingMode = PixivRatingModeSafe
	}
	if err = a.appData.SetInt(constants.PIXIV_RATING_MODE_KEY, p.RatingMode); err != nil {
		return err
	}

	if getReadableSearchMode(p.SearchMode) == UnknownValue {
		p.SearchMode = PixivSearchModeTag
	}
	if err = a.appData.SetInt(constants.PIXIV_SEARCH_MODE_KEY, p.SearchMode); err != nil {
		return err
	}

	if getReadableSortOrder(p.SortOrder) == UnknownValue {
		p.SortOrder = PixivSortOrderDate
	}
	if err = a.appData.SetInt(constants.PIXIV_SORT_ORDER_KEY, p.SortOrder); err != nil {
		return err
	}

	if getReadableUgoiraFileFormat(p.UgoiraOutputFormat) == UnknownValue {
		p.UgoiraOutputFormat = PixivUgoiraOutputFormatGif
	}
	if err = a.appData.SetInt(constants.PIXIV_UGOIRA_OUTPUT_FORMAT_KEY, p.UgoiraOutputFormat); err != nil {
		return err
	}

	if getReadableAiSearchMode(p.AiSearchMode) == UnknownValue {
		p.AiSearchMode = PixivAiSearchAllow
	}
	if err = a.appData.SetInt(constants.PIXIV_AI_SEARCH_MODE_KEY, p.AiSearchMode); err != nil {
		return err
	}

	// 0-51 for mp4, 0-63 for webm
	if p.UgoiraOutputFormat == PixivUgoiraOutputFormatMp4 && p.UgoiraQuality <= 51 {
		err = a.appData.SetInt(constants.PIXIV_UGOIRA_QUALITY_KEY, int(p.UgoiraQuality))
	} else if p.UgoiraOutputFormat == PixivUgoiraOutputFormatWebm && p.UgoiraQuality <= 63 {
		err = a.appData.SetInt(constants.PIXIV_UGOIRA_QUALITY_KEY, int(p.UgoiraQuality))
	}
	return err
}


func getReadableArtworkType(artworkType int) string {
	switch artworkType {
	case PixivArtworkTypeIllustAndUgoira:
		return "Illust and Ugoira"
	case PixivArtworkTypeManga:
		return "Manga"
	case PixivArtworkTypeAll:
		return "All"
	default:
		return UnknownValue
	}
}

func convertArtworkTypeForBackend(artworkType int) string {
	switch artworkType {
	case PixivArtworkTypeIllustAndUgoira:
		return "illust_and_ugoira"
	case PixivArtworkTypeManga:
		return "manga"
	case PixivArtworkTypeAll:
		return "all"
	default:
		return UnknownValue
	}
}

func getReadableRatingMode(ratingMode int) string {
	switch ratingMode {
	case PixivRatingModeR18:
		return "R-18"
	case PixivRatingModeSafe:
		return "Safe"
	case PixivRatingModeAll:
		return "All"
	default:
		return UnknownValue
	}
}

func convertRatingModeForBackend(ratingMode int) string {
	switch ratingMode {
	case PixivRatingModeR18:
		return "r18"
	case PixivRatingModeSafe:
		return "safe"
	case PixivRatingModeAll:
		return "all"
	default:
		return UnknownValue
	}
}

func getReadableSearchMode(searchMode int) string {
	switch searchMode {
	case PixivSearchModeTag:
		return "Similar Tag Names"
	case PixivSearchModeTagFull:
		return "Tags"
	case PixivSearchModeTC:
		return "Title and Caption"
	default:
		return UnknownValue
	}
}

func convertSearchModeForBackend(searchMode int) string {
	switch searchMode {
	case PixivSearchModeTag:
		return "s_tag"
	case PixivSearchModeTagFull:
		return "s_tag_full"
	case PixivSearchModeTC:
		return "s_tc"
	default:
		return UnknownValue
	}
}

func getReadableSortOrder(sortOrder int) string {
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
	default:
		return UnknownValue
	}
}

func convertSortOrderForBackend(sortOrder int) string {
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
func getReadableUgoiraFileFormat(format int) string {
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
	default:
		return UnknownValue
	}
}

func getReadableAiSearchMode(aiSearchMode int) string {
	switch aiSearchMode {
	case PixivAiSearchAllow:
		return "Allow"
	case PixivAiSearchFilter:
		return "Filter"
	default:
		return UnknownValue
	}
}

func convertAiSearchModeForBackend(aiSearchMode int) int {
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
	default:
		return -1
	}
}
