package app

import (
	"errors"
	"github.com/KJHJason/Cultured-Downloader-Logic/api/kemono"
	"net/http"
	"os"
	"path/filepath"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/notifier"
)

func validateKemonoUrls(inputs []string) (bool, []Input, *kemono.KemonoDl) {
	kemonoDl := kemono.KemonoDl{}
	inputsForRef := make([]Input, len(inputs))
	for idx, input := range inputs {
		isFavAndNonUrl := (input == "favourite" || input == "favorites")
		if input == "https://kemono.su/favorites" || isFavAndNonUrl {
			if isFavAndNonUrl {
				input = "https://kemono.su/favorites"
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
			Url:   input,
		}
	}
	err := kemonoDl.ValidateArgs()
	if err != nil {
		return false, nil, nil
	}

	return true, inputsForRef, &kemonoDl
}

// returns true if it's valid, false otherwise.
func (a *App) ValidateKemonoUrls(inputs []string) bool {
	valid, _, _ := validateKemonoUrls(inputs)
	return valid
}

func (a *App) parseKemonoSettingsMap(pref appdata.Preferences) (kemonoDlOptions *kemono.KemonoDlOptions, mainProgBar *ProgressBar, err error) {
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

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, cdlconsts.USER_AGENT)

	mainProgBar = NewProgressBar(a.ctx)
	baseDlDirPath := filepath.Join(downloadPath, cdlconsts.PIXIV_FANBOX_TITLE)
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

		Notifier: notifier.NewNotifier(a.ctx, constants.PROGRAM_NAME),

		MainProgBar:          mainProgBar,
		DownloadProgressBars: &[]*progress.DownloadProgressBar{},
	}
	kemonoDlOptions.SetContext(a.ctx)
	err = kemonoDlOptions.ValidateArgs(userAgent)
	if err != nil {
		return nil, nil, err
	}
	return kemonoDlOptions, mainProgBar, nil
}

func (a *App) SubmitKemonoToQueue(inputs []string, prefs appdata.Preferences) error {
	valid, inputsForRef, kemonoDl := validateKemonoUrls(inputs)
	if !valid {
		return errors.New("invalid Kemono URL(s)")
	}

	kemonoDlOptions, mainProgBar, err := a.parseKemonoSettingsMap(prefs)
	if err != nil {
		return errors.New("error getting download directory")
	}

	a.newDownloadQueue(cdlconsts.KEMONO, inputsForRef, mainProgBar, kemonoDlOptions.DownloadProgressBars, func() []error {
		defer kemonoDlOptions.Notifier.Release()

		errSlice := cdlogic.KemonoDownloadProcess(kemonoDl, kemonoDlOptions)
		mainProgBar.MakeLatestSnapshotMain()
		return errSlice
	})
	return nil
}
