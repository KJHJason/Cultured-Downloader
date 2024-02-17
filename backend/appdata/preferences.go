package appdata

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

type Preferences struct {
	DlPostThumbnail   bool
	DlPostImages      bool
	DlpostAttachments bool
	OverwriteFiles    bool

	DlGDrive         bool
	DetectOtherLinks bool

	// Fantia
	AutoSolveReCaptcha bool

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
	PixivArtworkTypeIllustAndUgoira = iota
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
	return "Unknown"
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
	return "Unknown"
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
	return "Unknown"
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
	return "Unknown"
}

func (a *AppData) GetPreferences() Preferences {
	pref := Preferences{
		DlPostThumbnail:   a.GetBool(constants.DlThumbnailKey),
		DlPostImages:      a.GetBool(constants.DlImagesKey),
		DlpostAttachments: a.GetBool(constants.DlAttachmentsKey),
		OverwriteFiles:    a.GetBool(constants.OverwriteFilesKey),

		DlGDrive:         a.GetBool(constants.DlGdriveKey),
		DetectOtherLinks: a.GetBool(constants.DetectOtherUrlsKey),

		AutoSolveReCaptcha: a.GetBool(constants.AutoSolveReCaptchaKey),

		ArtworkType:        a.GetInt(constants.PixivArtworkTypeKey),
		DeleteUgoiraZip:    a.GetBool(constants.PixivDeleteUgoiraZipKey),
		RatingMode:         a.GetInt(constants.PixivRatingModeKey),
		SearchMode:         a.GetInt(constants.PixivSearchModeKey),
		SortOrder:          a.GetInt(constants.PixivSortOrderKey),
		UgoiraOutputFormat: a.GetInt(constants.PixivUgoiraOutputFormatKey),
		UgoiraQuality:      uint8(a.GetInt(constants.PixivUgoiraQualityKey)),
	}
	return pref
}
