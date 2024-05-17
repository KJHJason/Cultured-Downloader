package app

import (
	"context"
	"errors"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/pixiv"
	pixivmobile "github.com/KJHJason/Cultured-Downloader-Logic/api/pixiv/mobile"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/pixiv/ugoira"
	pixivweb "github.com/KJHJason/Cultured-Downloader-Logic/api/pixiv/web"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func validatePixivTag(tagInput string) (valid bool, tag string, pageNum string) {
	if tagInput == "" {
		return false, "", ""
	}
	if strings.HasPrefix(tagInput, "https://www.pixiv.net/en/artworks") || strings.HasPrefix(tagInput, "https://www.pixiv.net/artworks") {
		return false, "", ""
	}

	// split by ";" and get the last element,
	// for the other elements, just join them back with ";"
	tagInput = strings.TrimSpace(tagInput)
	splitTag := strings.Split(tagInput, ";")
	splitTagLen := len(splitTag)
	if splitTagLen == 0 {
		return len(tagInput) > 0, tagInput, ""
	}
	if splitTagLen == 1 { // in the event when the user inputs like "tag;"
		return true, splitTag[0], ""
	}
	if splitTagLen == 2 { // in the event when the user inputs like "tag;1"
		return true, splitTag[0], splitTag[1]
	}

	// in the event the tag has one or more ";"
	pageNum = splitTag[splitTagLen-1]
	tag = strings.Join(splitTag[:splitTagLen-1], ";")
	return true, tag, pageNum
}

var codeVerifier string

func (a *App) StartPixivOAuth() string {
	var url string
	url, codeVerifier = pixivmobile.GetOAuthURL()
	return url
}

func (a *App) VerifyPixivOAuthCode(code string) error {
	if codeVerifier == "" {
		return errors.New("code verifier is empty, please start the OAuth process first")
	}

	refreshToken, err := pixivmobile.VerifyOAuthCode(code, codeVerifier, 15)
	if err != nil {
		return err
	}

	codeVerifier = ""
	return a.appData.SetSecureString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY, refreshToken)
}

func (a *App) SetPixivOAuthRefreshToken(refreshToken string) error {
	if _, _, err := pixivmobile.RefreshAccessToken(a.ctx, 15, refreshToken); err != nil {
		return err
	}
	return a.appData.SetSecureString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY, refreshToken)

}
func (a *App) GetPixivRefreshToken() string {
	return a.appData.GetSecuredString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY)
}

func validatePixivInputs(inputs []string) (bool, []Input, *pixiv.PixivDl) {
	pixivDl := pixiv.PixivDl{}
	inputsForRef := make([]Input, len(inputs))
	for idx, input := range inputs {
		urlForRef := input
		if valid, tag, pageNums := validatePixivTag(input); valid {
			pixivDl.TagNames = append(pixivDl.TagNames, tag)
			pixivDl.TagNamesPageNums = append(pixivDl.TagNamesPageNums, pageNums)
			input = tag
			urlForRef = "https://www.pixiv.net/tags/" + tag
		} else if artworkUrlMatch := cdlconsts.PIXIV_ARTWORK_URL_REGEX.FindStringSubmatch(input); len(artworkUrlMatch) > 0 {
			pixivDl.ArtworkIds = append(pixivDl.ArtworkIds, artworkUrlMatch[cdlconsts.PIXIV_ARTWORK_ID_IDX])
		} else if artistUrlMatch := cdlconsts.PIXIV_ARTIST_URL_REGEX.FindStringSubmatch(input); len(artistUrlMatch) > 0 {
			pixivDl.ArtistIds = append(pixivDl.ArtistIds, artistUrlMatch[cdlconsts.PIXIV_ARTIST_ID_IDX])
			pixivDl.ArtistPageNums = append(pixivDl.ArtistPageNums, artistUrlMatch[cdlconsts.PIXIV_ARTIST_PAGE_NUM_IDX])
		} else {
			return false, nil, nil
		}

		encodedUrl, err := url.Parse(urlForRef)
		if err != nil {
			logger.MainLogger.Errorf("Error parsing URL: %s", urlForRef)
			return false, nil, nil
		}
		inputsForRef[idx] = Input{
			Input: input,
			Url:   encodedUrl.String(),
		}
	}
	err := pixivDl.ValidateArgs()
	if err != nil {
		return false, nil, nil
	}

	return true, inputsForRef, &pixivDl
}

// returns true if it's valid, false otherwise.
func (a *App) ValidatePixivInputs(inputs []string) bool {
	valid, _, _ := validatePixivInputs(inputs)
	return valid
}

func (a *App) parsePixivMobileSettingsMap(ctx context.Context, pixivRefreshToken string, pref *preferences) (pixivMobileDlOptions *pixivmobile.PixivMobileDlOptions, mainProgBar *ProgressBar, err error) {
	if pixivRefreshToken == "" {
		//lint:ignore ST1005 Captialised for frontend use
		return nil, nil, errors.New("Pixiv Refresh Token is empty")
	}

	downloadPath, err, _ := a.getDownloadDir()
	if err != nil {
		return nil, nil, err
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, httpfuncs.DEFAULT_USER_AGENT)

	mainProgBar = NewProgressBar(ctx)
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.PIXIV_MOBILE_TITLE)
	os.MkdirAll(baseDlDirPath, cdlconsts.DEFAULT_PERMS)
	mainProgBar.UpdateFolderPath(baseDlDirPath)

	pixivMobileDlOptions = &pixivmobile.PixivMobileDlOptions{
		BaseDownloadDirPath: baseDlDirPath,
		SortOrder:           convertSortOrderForBackend(pref.SortOrder),
		SearchMode:          convertSearchModeForBackend(pref.SearchMode),
		SearchAiMode:        convertAiSearchModeForBackend(pref.AiSearchMode),
		RatingMode:          convertRatingModeForBackend(pref.RatingMode),
		ArtworkType:         convertArtworkTypeForBackend(pref.ArtworkType),

		Configs: &configs.Config{
			DownloadPath:   downloadPath,
			FfmpegPath:     a.GetFfmpegPath(),
			OverwriteFiles: pref.OverwriteFiles,
			LogUrls:        pref.DetectOtherLinks,
			UserAgent:      userAgent,
		},

		// MobileClient is initialised when ValidateArgs is called

		RefreshToken: pixivRefreshToken,

		Notifier: a.notifier,

		MainProgBar:          mainProgBar,
		DownloadProgressBars: &[]*progress.DownloadProgressBar{},
	}
	pixivMobileDlOptions.SetContext(ctx)
	err = pixivMobileDlOptions.ValidateArgs()
	if err != nil {
		return nil, nil, err
	}
	return pixivMobileDlOptions, mainProgBar, nil
}

func (a *App) parsePixivSettingsMap(ctx context.Context, pref *preferences) (pixivWebDlOptions *pixivweb.PixivWebDlOptions, mainProgBar *ProgressBar, err error) {
	pixivSession := a.appData.GetSecuredString(constants.PIXIV_COOKIE_VALUE_KEY)
	var pixivSessions []*http.Cookie
	if pixivSession == "" {
		pixivSessions, err = a.getSessionCookies(constants.PIXIV)
		if err != nil {
			return nil, nil, err
		}
	}

	downloadPath, err, _ := a.getDownloadDir()
	if err != nil {
		return nil, nil, err
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, httpfuncs.DEFAULT_USER_AGENT)

	mainProgBar = NewProgressBar(ctx)
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.PIXIV_TITLE)
	os.MkdirAll(baseDlDirPath, cdlconsts.DEFAULT_PERMS)
	mainProgBar.UpdateFolderPath(baseDlDirPath)

	pixivWebDlOptions = &pixivweb.PixivWebDlOptions{
		BaseDownloadDirPath: baseDlDirPath,
		SortOrder:           convertSortOrderForBackend(pref.SortOrder),
		SearchMode:          convertSearchModeForBackend(pref.SearchMode),
		SearchAiMode:        convertAiSearchModeForBackend(pref.AiSearchMode),
		RatingMode:          convertRatingModeForBackend(pref.RatingMode),
		ArtworkType:         convertArtworkTypeForBackend(pref.ArtworkType),

		Configs: &configs.Config{
			DownloadPath:   downloadPath,
			FfmpegPath:     a.GetFfmpegPath(),
			OverwriteFiles: pref.OverwriteFiles,
			LogUrls:        pref.DetectOtherLinks,
			UserAgent:      userAgent,
		},

		SessionCookieId: pixivSession,
		SessionCookies:  pixivSessions,

		Notifier: a.notifier,

		MainProgBar:          mainProgBar,
		DownloadProgressBars: &[]*progress.DownloadProgressBar{},
	}
	pixivWebDlOptions.SetContext(ctx)
	err = pixivWebDlOptions.ValidateArgs(userAgent)
	if err != nil {
		return nil, nil, err
	}
	return pixivWebDlOptions, mainProgBar, nil
}

func parsePixivUgoiraSettings(pref *preferences) *ugoira.UgoiraOptions {
	return &ugoira.UgoiraOptions{
		DeleteZip:    pref.DeleteUgoiraZip,
		Quality:      int(pref.UgoiraQuality),
		OutputFormat: getReadableUgoiraFileFormat(pref.UgoiraOutputFormat),
	}
}

func (a *App) SubmitPixivToQueue(inputs []string, prefs *preferences) error {
	if prefs == nil {
		return errors.New("preferences is nil in SubmitPixivToQueue()")
	}

	valid, inputsForRef, pixivDl := validatePixivInputs(inputs)
	if !valid {
		return errors.New("invalid Kemono URL(s)")
	}

	ugoiraOptions := parsePixivUgoiraSettings(prefs)
	ctx, cancel := context.WithCancel(a.ctx)

	var mainProgBar *ProgressBar
	var dlProgBar *[]*progress.DownloadProgressBar
	var fnToAddToQueue func() []error
	if pixivMobileRefreshToken := a.appData.GetSecuredString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY); pixivMobileRefreshToken != "" {
		pixivMobileDlOptions, mainProgBarVal, err := a.parsePixivMobileSettingsMap(ctx, pixivMobileRefreshToken, prefs)
		if err != nil {
			cancel()
			return err
		}

		mainProgBar = mainProgBarVal
		dlProgBar = pixivMobileDlOptions.DownloadProgressBars

		fnToAddToQueue = func() []error {
			defer cancel()
			errSlice := cdlogic.PixivMobileDownloadProcess(pixivDl, pixivMobileDlOptions, ugoiraOptions)
			mainProgBar.MakeLatestSnapshotMain()
			return errSlice
		}
	} else {
		pixivWebDlOptions, mainProgBarVal, err := a.parsePixivSettingsMap(ctx, prefs)
		if err != nil {
			cancel()
			return err
		}

		mainProgBar = mainProgBarVal
		dlProgBar = pixivWebDlOptions.DownloadProgressBars

		fnToAddToQueue = func() []error {
			defer cancel()
			errSlice := cdlogic.PixivWebDownloadProcess(pixivDl, pixivWebDlOptions, ugoiraOptions)
			mainProgBar.MakeLatestSnapshotMain()
			return errSlice
		}
	}

	a.addNewDownloadQueue(ctx, cancel, &dlInfo{
		website:        cdlconsts.PIXIV,
		inputs:         inputsForRef,
		mainProgBar:    mainProgBar,
		dlProgressBars: dlProgBar,
		taskHandler:    fnToAddToQueue,
	})
	return nil
}
