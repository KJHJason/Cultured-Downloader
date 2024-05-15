package app

import (
	"context"
	"errors"
	"net/http"
	"os"
	"path/filepath"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/kemono"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func validateKemonoInputs(inputs []string) (bool, []Input, *kemono.KemonoDl) {
	kemonoDl := kemono.KemonoDl{}
	inputsForRef := make([]Input, len(inputs))
	for idx, input := range inputs {
		url := input
		isFavAndNonUrl := (input == "favourites" || input == "favorites")
		if input == "https://kemono.su/favorites" || isFavAndNonUrl {
			if isFavAndNonUrl {
				url = "https://kemono.su/favorites"
			}
			kemonoDl.DlFav = true
		} else if postUrlMatch := cdlconsts.KEMONO_POST_URL_REGEX.FindStringSubmatch(input); len(postUrlMatch) > 0 {
			kemonoDl.PostsToDl = append(kemonoDl.PostsToDl, &kemono.KemonoPostToDl{
				CreatorId: postUrlMatch[cdlconsts.KEMONO_POST_URL_REGEX_CREATOR_ID_IDX],
				Service:   postUrlMatch[cdlconsts.KEMONO_POST_URL_REGEX_SERVICE_IDX],
				PostId:    postUrlMatch[cdlconsts.KEMONO_POST_URL_REGEX_POST_ID_IDX],
			})
		} else if creatorUrlMatch := cdlconsts.KEMONO_CREATOR_URL_REGEX.FindStringSubmatch(input); len(creatorUrlMatch) > 0 {
			kemonoDl.CreatorsToDl = append(kemonoDl.CreatorsToDl, &kemono.KemonoCreatorToDl{
				Service:   creatorUrlMatch[cdlconsts.KEMONO_CREATOR_URL_REGEX_SERVICE_IDX],
				CreatorId: creatorUrlMatch[cdlconsts.KEMONO_CREATOR_URL_REGEX_CREATOR_ID_IDX],
				PageNum:   creatorUrlMatch[cdlconsts.KEMONO_CREATOR_URL_REGEX_PAGE_NUM_IDX],
			})
		} else {
			return false, nil, nil
		}

		inputsForRef[idx] = Input{
			Input: input,
			Url:   url,
		}
	}
	err := kemonoDl.ValidateArgs()
	if err != nil {
		return false, nil, nil
	}

	return true, inputsForRef, &kemonoDl
}

// returns true if it's valid, false otherwise.
func (a *App) ValidateKemonoInputs(inputs []string) bool {
	valid, _, _ := validateKemonoInputs(inputs)
	return valid
}

func (a *App) parseKemonoSettingsMap(ctx context.Context, pref *preferences) (kemonoDlOptions *kemono.KemonoDlOptions, mainProgBar *ProgressBar, err error) {
	kemonoSession := a.appData.GetSecuredString(constants.KEMONO_COOKIE_VALUE_KEY)
	var kemonoSessions []*http.Cookie
	if kemonoSession == "" {
		kemonoSessions, err = a.getSessionCookies(constants.KEMONO)
		if err != nil {
			return nil, nil, err
		}
	}

	downloadPath, err, _ := a.GetDownloadDir()
	if err != nil {
		return nil, nil, err
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, httpfuncs.DEFAULT_USER_AGENT)

	mainProgBar = NewProgressBar(ctx)
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.KEMONO_TITLE)
	os.MkdirAll(baseDlDirPath, cdlconsts.DEFAULT_PERMS)
	mainProgBar.UpdateFolderPath(baseDlDirPath)

	kemonoDlOptions = &kemono.KemonoDlOptions{
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

		SessionCookieId: kemonoSession,
		SessionCookies:  kemonoSessions,

		Notifier: a.notifier,

		MainProgBar:          mainProgBar,
		DownloadProgressBars: &[]*progress.DownloadProgressBar{},
	}
	kemonoDlOptions.SetContext(ctx)
	err = kemonoDlOptions.ValidateArgs(userAgent)
	if err != nil {
		return nil, nil, err
	}
	return kemonoDlOptions, mainProgBar, nil
}

func (a *App) SubmitKemonoToQueue(inputs []string, prefs *preferences) error {
	if prefs == nil {
		return errors.New("preferences is nil in SubmitKemonoToQueue()")
	}

	valid, inputsForRef, kemonoDl := validateKemonoInputs(inputs)
	if !valid {
		return errors.New("invalid Kemono URL(s)")
	}

	ctx, cancel := context.WithCancel(context.Background())
	kemonoDlOptions, mainProgBar, err := a.parseKemonoSettingsMap(ctx, prefs)
	if err != nil {
		cancel()
		return err
	}

	a.addNewDownloadQueue(ctx, cancel, &dlInfo{
		website:        cdlconsts.KEMONO,
		inputs:         inputsForRef,
		mainProgBar:    mainProgBar,
		dlProgressBars: kemonoDlOptions.DownloadProgressBars,
		taskHandler: func() []error {
			defer cancel()
			errSlice := cdlogic.KemonoDownloadProcess(kemonoDl, kemonoDlOptions)
			mainProgBar.MakeLatestSnapshotMain()
			return errSlice
		},
	})
	return nil
}
