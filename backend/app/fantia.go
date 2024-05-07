package app

import (
	"errors"
	"net/http"
	"os"
	"path/filepath"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/fantia"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/notifier"
)

func validateFantiaUrls(inputs []string) (bool, []Input, *fantia.FantiaDl) {
	fantiaDl := fantia.FantiaDl{}
	inputsForRef := make([]Input, len(inputs))
	for idx, input := range inputs {
		creatorUrlMatch := cdlconsts.FANTIA_CREATOR_URL_REGEX.FindStringSubmatch(input)
		postUrlMatch := cdlconsts.FANTIA_POST_URL_REGEX.FindStringSubmatch(input)
		if len(creatorUrlMatch) == 0 && len(postUrlMatch) == 0 {
			return false, nil, nil
		}

		var id string
		var pageNum string
		if len(creatorUrlMatch) > 0 {
			id = creatorUrlMatch[cdlconsts.FANTIA_CREATOR_ID_IDX]
			pageNum = creatorUrlMatch[cdlconsts.FANTIA_CREATOR_PAGE_NUM_IDX]
			fantiaDl.FanclubIds = append(fantiaDl.FanclubIds, id)
			fantiaDl.FanclubPageNums = append(fantiaDl.FanclubPageNums, pageNum)
		} else {
			id = postUrlMatch[cdlconsts.FANTIA_POST_ID_IDX]
			fantiaDl.PostIds = append(fantiaDl.PostIds, id)
		}

		inputsForRef[idx] = Input{
			id:      id,
			pageNum: pageNum,
			Input:   input,
			Url:     input,
		}
	}
	err := fantiaDl.ValidateArgs()
	if err != nil {
		return false, nil, nil
	}

	return true, inputsForRef, &fantiaDl
}

// returns true if it's valid, false otherwise.
func (a *App) ValidateFantiaUrls(inputs []string) bool {
	valid, _, _ := validateFantiaUrls(inputs)
	return valid
}

func (a *App) parseSettingsMap(pref appdata.Preferences) (fantiaDlOptions *fantia.FantiaDlOptions, mainProgBar *ProgressBar, err error) {
	fantiaSession := a.appData.GetSecuredString(constants.FANTIA_COOKIE_VALUE_KEY)
	var fantiaSessions []*http.Cookie
	if fantiaSession == "" {
		fantiaSessions, err = a.getSessionCookies(constants.FANTIA)
		if err != nil {
			return nil, nil, err
		}
	}

	downloadPath, err := a.GetDownloadDir()
	if err != nil {
		return nil, nil, err
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, cdlconsts.USER_AGENT)

	mainProgBar = NewProgressBar(a.ctx)
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.FANTIA_TITLE)
	os.MkdirAll(baseDlDirPath, cdlconsts.DEFAULT_PERMS)
	mainProgBar.UpdateFolderPath(baseDlDirPath)

	fantiaDlOptions = &fantia.FantiaDlOptions{
		DlThumbnails:        pref.DlPostThumbnail,
		DlImages:            pref.DlPostImages,
		DlAttachments:       pref.DlPostAttachments,
		DlGdrive:            pref.DlGDrive,
		BaseDownloadDirPath: baseDlDirPath,

		GdriveClient: a.GetGdriveClient(),

		Configs: &configs.Config{
			DownloadPath:   downloadPath,
			FfmpegPath:     "",
			OverwriteFiles: pref.OverwriteFiles,
			LogUrls:        pref.DetectOtherLinks,
			UserAgent:      userAgent,
		},

		SessionCookieId: fantiaSession,
		SessionCookies:  fantiaSessions,

		Notifier: notifier.NewNotifier(a.ctx, constants.PROGRAM_NAME),

		MainProgBar:          mainProgBar,
		DownloadProgressBars: &[]*progress.DownloadProgressBar{},
	}
	fantiaDlOptions.SetContext(a.ctx)
	err = fantiaDlOptions.ValidateArgs(userAgent)
	if err != nil {
		return nil, nil, err
	}
	return fantiaDlOptions, mainProgBar, nil
}

func (a *App) SubmitFantiaToQueue(inputs []string, prefs appdata.Preferences) error {
	valid, inputsForRef, fantiaDl := validateFantiaUrls(inputs)
	if !valid {
		return errors.New("invalid Fantia URL(s)")
	}

	fantiaDlOptions, mainProgBar, err := a.parseSettingsMap(prefs)
	if err != nil {
		return errors.New("error getting download directory")
	}

	a.newDownloadQueue(cdlconsts.FANTIA, inputsForRef, mainProgBar, fantiaDlOptions.DownloadProgressBars, func() []error {
		defer fantiaDlOptions.Notifier.Release()

		errSlice := cdlogic.FantiaDownloadProcess(fantiaDl, fantiaDlOptions)
		mainProgBar.MakeLatestSnapshotMain()
		return errSlice
	})
	return nil
}
