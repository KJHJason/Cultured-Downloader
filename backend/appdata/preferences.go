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

	// Fantia only as of 02/2024
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
	ugoiraQuality := a.GetInt(constants.PixivUgoiraQualityKey)
	if ugoiraQuality < 0 || ugoiraQuality > 63 {
		ugoiraQuality = 0
	}

	pref := Preferences{
		DlPostThumbnail:   a.GetBool(constants.DlThumbnailKey),
		DlPostImages:      a.GetBool(constants.DlImagesKey),
		DlPostAttachments: a.GetBool(constants.DlAttachmentsKey),
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
		UgoiraQuality:      uint8(ugoiraQuality),
	}
	return pref
}

func (a *AppData) SetPreferences(platform string, p Preferences) error {
	var err error
	if err = a.SetBool(constants.DlThumbnailKey, p.DlPostThumbnail); err != nil {
		return err
	}
	if err = a.SetBool(constants.DlImagesKey, p.DlPostImages); err != nil {
		return err
	}
	if err = a.SetBool(constants.DlAttachmentsKey, p.DlPostAttachments); err != nil {
		return err
	}
	if err = a.SetBool(constants.OverwriteFilesKey, p.OverwriteFiles); err != nil {
		return err
	}

	if err = a.SetBool(constants.DlGdriveKey, p.DlGDrive); err != nil {
		return err
	}
	if err = a.SetBool(constants.DetectOtherUrlsKey, p.DetectOtherLinks); err != nil {
		return err
	}

	if platform == constants.Fantia {
		if err = a.SetBool(constants.AutoSolveReCaptchaKey, p.AutoSolveReCaptcha); err != nil {
			return err
		}
	}

	// Below are Pixiv specific settings
	if platform != constants.Pixiv {
		return nil
	}
	if GetReadableArtworkType(p.ArtworkType) == UnknownValue {
		p.ArtworkType = PixivArtworkTypeIllustAndUgoira
	}
	if err = a.SetInt(constants.PixivArtworkTypeKey, p.ArtworkType); err != nil {
		return err
	}

	if err = a.SetBool(constants.PixivDeleteUgoiraZipKey, p.DeleteUgoiraZip); err != nil {
		return err
	}

	if GetReadableRatingMode(p.RatingMode) == UnknownValue {
		p.RatingMode = PixivRatingModeSafe
	}
	if err = a.SetInt(constants.PixivRatingModeKey, p.RatingMode); err != nil {
		return err
	}

	if GetReadableSearchMode(p.SearchMode) == UnknownValue {
		p.SearchMode = PixivSearchModeTag
	}
	if err = a.SetInt(constants.PixivSearchModeKey, p.SearchMode); err != nil {
		return err
	}

	if GetReadableSortOrder(p.SortOrder) == UnknownValue {
		p.SortOrder = PixivSortOrderDate
	}
	if err = a.SetInt(constants.PixivSortOrderKey, p.SortOrder); err != nil {
		return err
	}

	if GetReadableUgoiraFileFormat(p.UgoiraOutputFormat) == UnknownValue {
		p.UgoiraOutputFormat = PixivUgoiraOutputFormatGif
	}
	if err = a.SetInt(constants.PixivUgoiraOutputFormatKey, p.UgoiraOutputFormat); err != nil {
		return err
	}

	// 0-51 for mp4, 0-63 for webm
	if p.UgoiraOutputFormat == PixivUgoiraOutputFormatMp4 && p.UgoiraQuality <= 51 {
		err = a.SetInt(constants.PixivUgoiraQualityKey, int(p.UgoiraQuality))
	} else if p.UgoiraOutputFormat == PixivUgoiraOutputFormatWebm && p.UgoiraQuality <= 63 {
		err = a.SetInt(constants.PixivUgoiraQualityKey, int(p.UgoiraQuality))
	}
	return err
}
