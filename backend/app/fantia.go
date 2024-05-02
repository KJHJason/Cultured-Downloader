package app

import (
	"errors"

	"github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/fantia"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func validateFantiaUrls(inputs []string) (bool, []Input, *fantia.FantiaDl) {
	fantiaDl := fantia.FantiaDl{}
	inputsForRef := make([]Input, len(inputs)) 
	for idx, input := range inputs {
		creatorUrlMatch := cdconsts.FANTIA_CREATOR_URL_REGEX.FindStringSubmatch(input)
		postUrlMatch := cdconsts.FANTIA_POST_URL_REGEX.FindStringSubmatch(input)
		if len(creatorUrlMatch) == 0 && len(postUrlMatch) == 0 {
			return false, nil, nil
		}

		var id string
		var pageNum string
		if len(creatorUrlMatch) > 0 {
			id = creatorUrlMatch[cdconsts.FANTIA_CREATOR_ID_IDX]
			pageNum = creatorUrlMatch[cdconsts.FANTIA_CREATOR_PAGE_NUM_IDX]
			fantiaDl.FanclubIds = append(fantiaDl.FanclubIds, id)
			fantiaDl.FanclubPageNums = append(fantiaDl.FanclubPageNums, pageNum)
		} else {
			id = postUrlMatch[cdconsts.FANTIA_POST_ID_IDX]
			fantiaDl.PostIds = append(fantiaDl.PostIds, id)
		}

		inputsForRef[idx] = Input{
			id:      id,
			pageNum: pageNum,
			Input:   input,
			Url:     input,
		}
	}
	return true, inputsForRef, &fantiaDl
}

// returns true if it's valid, false otherwise.
func (a *App) ValidateFantiaUrls(inputs []string) bool {
	valid, _, _ := validateFantiaUrls(inputs)
	return valid
}

func (a *App) parseSettingsMap(settings map[string]bool, dlProgBars []*progress.DownloadProgressBar) (fantiaDlOptions *fantia.FantiaDlOptions, hasErr bool) {
	fantiaSession := a.appData.GetSecuredString(constants.FantiaCookieValueKey)
	downloadPath, hasErr := a.GetDownloadDir()
	if hasErr {
		return nil, hasErr
	}

	userAgent := a.appData.GetString(constants.UserAgentKey)
	if userAgent == "" {
		userAgent = cdconsts.USER_AGENT
	}

	fantiaDlOptions = &fantia.FantiaDlOptions{
		DlThumbnails: settings["DlPostThumbnail"],
		DlImages: settings["DlPostImages"],
		DlAttachments: settings["DlPostAttachments"],
		DlGdrive: settings["DlGDrive"],

		GdriveClient: a.GetGdriveClient(),

		Configs: &configs.Config{
			DownloadPath: downloadPath,
			FfmpegPath:     "",
			OverwriteFiles: settings["OverwriteFiles"],
			LogUrls:        settings["DetectOtherLinks"],
			UserAgent:      userAgent,
		},

		SessionCookieId: fantiaSession,
		SessionCookies: nil,

		Notifier: nil,

		MainProgBar:          NewProgressBar(a.ctx),
		DownloadProgressBars: &dlProgBars,
	}
	fantiaDlOptions.SetContext(a.ctx)
	return fantiaDlOptions, false
} 

func (a *App) SubmitFantiaToQueue(inputs []string, settings map[string]bool) {
	valid, inputsForRef, fantiaDl := validateFantiaUrls(inputs)
	if !valid {
		return
	}

	mainProgBar := NewProgressBar(a.ctx)
	a.newDownloadQueue(inputsForRef, mainProgBar, func() []*error {
		fantiaDlOptions, hasErr := a.parseSettingsMap(settings, []*progress.DownloadProgressBar{})
		if hasErr {
			err := errors.New("error getting download directory")
			return []*error{&err}
		}
		return cdlogic.FantiaDownloadProcess(fantiaDl, fantiaDlOptions)
	})
}
