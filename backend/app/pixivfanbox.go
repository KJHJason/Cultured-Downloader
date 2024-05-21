package app

import (
	"context"
	"errors"
	"net/http"
	"os"
	"path/filepath"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/pixivfanbox"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func validatePixivFanboxUrls(inputs []string) (bool, []Input, *pixivfanbox.PixivFanboxDl) {
	pixivFanboxDl := pixivfanbox.PixivFanboxDl{}
	inputsForRef := make([]Input, len(inputs))
	for idx, input := range inputs {
		var id string
		var pageNum string
		if postUrl1Match := cdlconsts.PIXIV_FANBOX_POST_URL_REGEX1.FindStringSubmatch(input); len(postUrl1Match) > 0 {
			id = postUrl1Match[cdlconsts.PIXIV_FANBOX_POST_ID_IDX1]
			pixivFanboxDl.PostIds = append(pixivFanboxDl.PostIds, id)
		} else if postUrl2Match := cdlconsts.PIXIV_FANBOX_POST_URL_REGEX2.FindStringSubmatch(input); len(postUrl2Match) > 0 {
			id = postUrl2Match[cdlconsts.PIXIV_FANBOX_POST_ID_IDX2]
			pixivFanboxDl.PostIds = append(pixivFanboxDl.PostIds, id)
		} else if creatorUrl2Match := cdlconsts.PIXIV_FANBOX_CREATOR_URL_REGEX2.FindStringSubmatch(input); len(creatorUrl2Match) > 0 {
			id = creatorUrl2Match[cdlconsts.PIXIV_FANBOX_CREATOR_ID_IDX2]
			pageNum = creatorUrl2Match[cdlconsts.PIXIV_FANBOX_CREATOR_PAGE_NUM_IDX2]

			pixivFanboxDl.CreatorIds = append(pixivFanboxDl.CreatorIds, id)
			pixivFanboxDl.CreatorPageNums = append(pixivFanboxDl.CreatorPageNums, pageNum)
		} else if creatorUrl1Match := cdlconsts.PIXIV_FANBOX_CREATOR_URL_REGEX1.FindStringSubmatch(input); len(creatorUrl1Match) > 0 {
			id = creatorUrl1Match[cdlconsts.PIXIV_FANBOX_CREATOR_ID_IDX1]
			pageNum = creatorUrl1Match[cdlconsts.PIXIV_FANBOX_CREATOR_PAGE_NUM_IDX1]

			pixivFanboxDl.CreatorIds = append(pixivFanboxDl.CreatorIds, id)
			pixivFanboxDl.CreatorPageNums = append(pixivFanboxDl.CreatorPageNums, pageNum)
		} else {
			return false, nil, nil
		}

		inputsForRef[idx] = Input{
			Input: input,
			Url:   input,
		}
	}

	err := pixivFanboxDl.ValidateArgs()
	if err != nil {
		return false, nil, nil
	}

	return true, inputsForRef, &pixivFanboxDl
}

// returns true if it's valid, false otherwise.
func (a *App) ValidatePixivFanboxUrls(inputs []string) bool {
	valid, _, _ := validatePixivFanboxUrls(inputs)
	return valid
}

func (a *App) parsePixivFanboxSettingsMap(ctx context.Context, pref *Preferences) (pixivFanboxDlOptions *pixivfanbox.PixivFanboxDlOptions, mainProgBar *ProgressBar, err error) {
	pixivFanboxSession := a.appData.GetSecuredString(constants.PIXIV_FANBOX_COOKIE_VALUE_KEY)
	var pixivFanboxSessions []*http.Cookie
	if pixivFanboxSession == "" {
		pixivFanboxSessions, err = a.getSessionCookies(constants.PIXIV_FANBOX)
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
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.PIXIV_FANBOX_TITLE)
	os.MkdirAll(baseDlDirPath, cdlconsts.DEFAULT_PERMS)
	mainProgBar.UpdateFolderPath(baseDlDirPath)

	pixivFanboxDlOptions = &pixivfanbox.PixivFanboxDlOptions{
		DlThumbnails:        pref.DlPostThumbnail,
		DlImages:            pref.DlPostImages,
		DlAttachments:       pref.DlPostAttachments,
		DlGdrive:            pref.DlGDrive,
		UseCacheDb:          pref.UseCacheDb,
		BaseDownloadDirPath: baseDlDirPath,

		GdriveClient: a.GetGdriveClient(),

		Configs: &configs.Config{
			DownloadPath:   downloadPath,
			FfmpegPath:     "",
			OverwriteFiles: pref.OverwriteFiles,
			LogUrls:        pref.DetectOtherLinks,
			UserAgent:      userAgent,
		},

		SessionCookieId: pixivFanboxSession,
		SessionCookies:  pixivFanboxSessions,

		Notifier: a.notifier,

		MainProgBar:          mainProgBar,
		DownloadProgressBars: &[]*progress.DownloadProgressBar{},
	}
	pixivFanboxDlOptions.SetContext(ctx)
	err = pixivFanboxDlOptions.ValidateArgs(userAgent)
	if err != nil {
		return nil, nil, err
	}
	return pixivFanboxDlOptions, mainProgBar, nil
}

func (a *App) SubmitPixivFanboxToQueue(inputs []string, prefs *Preferences) error {
	if prefs == nil {
		return errors.New("preferences is nil in SubmitFantiaToQueue()")
	}

	valid, inputsForRef, pixivFanboxDl := validatePixivFanboxUrls(inputs)
	if !valid {
		return errors.New("invalid Pixiv Fanbox URL(s)")
	}

	ctx, cancel := context.WithCancel(a.ctx)
	pixivFanboxDlOptions, mainProgBar, err := a.parsePixivFanboxSettingsMap(ctx, prefs)
	if err != nil {
		cancel()
		return err
	}

	a.addNewDownloadQueue(ctx, cancel, &dlInfo{
		website:        cdlconsts.PIXIV_FANBOX,
		inputs:         inputsForRef,
		mainProgBar:    mainProgBar,
		dlProgressBars: pixivFanboxDlOptions.DownloadProgressBars,
		taskHandler: func() []error {
			defer cancel()
			errSlice := cdlogic.PixivFanboxDownloadProcess(pixivFanboxDl, pixivFanboxDlOptions)
			mainProgBar.MakeLatestSnapshotMain()
			return errSlice
		},
	})
	return nil
}
