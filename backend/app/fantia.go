package app

import (
	"context"
	"errors"
	"net/http"
	"os"
	"path/filepath"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/api"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/fantia"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func validateFantiaUrls(inputs []string) (bool, []Input, *fantia.FantiaDl) {
	fantiaDl := fantia.FantiaDl{}
	inputsForRef := make([]Input, len(inputs))
	for idx, input := range inputs {
		if postUrlMatch := cdlconsts.FANTIA_POST_URL_REGEX.FindStringSubmatch(input); len(postUrlMatch) > 0 {
			fantiaDl.PostIds = append(
				fantiaDl.PostIds,
				postUrlMatch[cdlconsts.FANTIA_POST_ID_IDX],
			)
		} else if creatorUrlMatch := cdlconsts.FANTIA_CREATOR_URL_REGEX.FindStringSubmatch(input); len(creatorUrlMatch) > 0 {
			fantiaDl.FanclubIds = append(
				fantiaDl.FanclubIds,
				creatorUrlMatch[cdlconsts.FANTIA_CREATOR_ID_IDX],
			)
			fantiaDl.FanclubPageNums = append(
				fantiaDl.FanclubPageNums,
				creatorUrlMatch[cdlconsts.FANTIA_CREATOR_PAGE_NUM_IDX],
			)
		} else if productUrlMatch := cdlconsts.FANTIA_PRODUCT_URL_REGEX.FindStringSubmatch(input); len(productUrlMatch) > 0 {
			fantiaDl.ProductIds = append(
				fantiaDl.ProductIds,
				productUrlMatch[cdlconsts.FANTIA_PRODUCT_ID_IDX],
			)
		} else if fanclubProductUrlMatch := cdlconsts.FANTIA_FANCLUB_PRODUCT_URL_REGEX.FindStringSubmatch(input); len(fanclubProductUrlMatch) > 0 {
			fantiaDl.ProductFanclubIds = append(
				fantiaDl.ProductFanclubIds,
				fanclubProductUrlMatch[cdlconsts.FANTIA_FANCLUB_PRODUCT_ID_IDX],
			)
			fantiaDl.ProductFanclubPageNums = append(
				fantiaDl.ProductFanclubPageNums,
				fanclubProductUrlMatch[cdlconsts.FANTIA_FANCLUB_PRODUCT_PAGE_NUM_IDX],
			)
		} else {
			return false, nil, nil
		}

		inputsForRef[idx] = Input{
			Input: input,
			Url:   input,
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

func (a *App) parseFantiaSettingsMap(ctx context.Context, pref *Preferences) (fantiaDlOptions *fantia.FantiaDlOptions, mainProgBar *ProgressBar, err error) {
	fantiaSession := a.appData.GetSecuredString(constants.FANTIA_COOKIE_VALUE_KEY)
	var fantiaSessions []*http.Cookie
	if fantiaSession == "" {
		fantiaSessions, err = a.getSessionCookies(constants.FANTIA)
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
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.FANTIA_TITLE)
	os.MkdirAll(baseDlDirPath, cdlconsts.DEFAULT_PERMS)
	mainProgBar.UpdateFolderPath(baseDlDirPath)

	fantiaDlOptions = &fantia.FantiaDlOptions{
		Base: &api.BaseDl{
			DlThumbnails:    pref.DlPostThumbnail,
			DlImages:        pref.DlPostImages,
			OrganiseImages:  pref.OrganisePostImages,
			DlAttachments:   pref.DlPostAttachments,
			DlGdrive:        pref.DlGDrive,
			UseCacheDb:      pref.UseCacheDb,
			DownloadDirPath: baseDlDirPath,

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

			Notifier: a.notifier,

			ProgressBarInfo: &progress.ProgressBarInfo{
				MainProgressBar:      mainProgBar,
				DownloadProgressBars: &[]*progress.DownloadProgressBar{},
			},
		},
	}
	fantiaDlOptions.SetContext(ctx)
	err = fantiaDlOptions.ValidateArgs(userAgent)
	if err != nil {
		return nil, nil, err
	}
	return fantiaDlOptions, mainProgBar, nil
}

func (a *App) SubmitFantiaToQueue(inputs []string, prefs *Preferences) error {
	if prefs == nil {
		return errors.New("preferences is nil in SubmitFantiaToQueue()")
	}

	valid, inputsForRef, fantiaDl := validateFantiaUrls(inputs)
	if !valid {
		return errors.New("invalid Fantia URL(s)")
	}

	ctx, cancel := context.WithCancel(a.ctx)
	fantiaDlOptions, mainProgBar, err := a.parseFantiaSettingsMap(ctx, prefs)
	if err != nil {
		cancel()
		return err
	}

	a.addNewDownloadQueue(ctx, cancel, &dlInfo{
		website:        cdlconsts.FANTIA,
		inputs:         inputsForRef,
		mainProgBar:    mainProgBar,
		dlProgressBars: fantiaDlOptions.Base.DownloadProgressBars(),
		taskHandler: func() []error {
			defer cancel()
			errSlice := cdlogic.FantiaDownloadProcess(
				fantiaDl,
				fantiaDlOptions,
				constants.CATCH_SIGINT,
			)
			mainProgBar.MakeLatestSnapshotMain()
			return errSlice
		},
	})
	return nil
}
