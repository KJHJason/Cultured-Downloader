package app

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/KJHJason/Cultured-Downloader-Logic/cache"
	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/language"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/notifier"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) getDownloadDir() (dirPath string, err error, hadToFallback bool) {
	savedDirPath := a.appData.GetString(constants.DOWNLOAD_KEY)
	if savedDirPath != "" && iofuncs.PathExists(savedDirPath) {
		return savedDirPath, nil, false
	}

	desktopDir, err := os.UserHomeDir()
	if err != nil {
		logger.MainLogger.Errorf("Error getting user home directory: %v", err)
		return "", fmt.Errorf("error getting user home directory: %w\nPlease manually set the download directory in the settings", err), false
	}

	desktopDir = filepath.Join(desktopDir, "Desktop", "Cultured Downloader")
	if err := os.MkdirAll(desktopDir, cdlconst.DEFAULT_PERMS); err != nil {
		panic(err)
	}
	a.appData.SetString(constants.DOWNLOAD_KEY, desktopDir)
	return desktopDir, nil, true
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx
	appData, initialLoadErr := appdata.NewAppData()
	if initialLoadErr != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error loading data from file!",
			Message: "Please refer to the logs or report this issue on GitHub.",
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v", err, initialLoadErr)
		}
		panic("Error loading data from file!")
	}
	a.appData = appData

	// retrieve user's download directory
	_, err, hadToFallback := a.getDownloadDir()
	if err != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error getting download directory!",
			Message: err.Error(),
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v", err, initialLoadErr)
		}
	} else if hadToFallback {
		// try retrieving the old download directory path from config.json (*Cultured-Downloader-CLI)
		oldSavedDlDirPath := iofuncs.DOWNLOAD_PATH
		if oldSavedDlDirPath != "" { // if it's not empty, set it as the download directory path
			if setErr := a.appData.SetString(constants.DOWNLOAD_KEY, oldSavedDlDirPath); setErr != nil {
				logger.MainLogger.Errorf("Error setting old download directory path: %v", setErr)
			}
		}
	}

	a.gdriveClient = a.GetGdriveClient()
	a.notifier = notifier.NewNotifier(a.ctx, constants.PROGRAM_NAME)
	a.lang = a.appData.GetStringWithFallback(constants.LANGUAGE_KEY, cdlconst.EN)

	if a.appData.GetBoolWithFallback(constants.USE_CACHE_DB_KEY, true) {
		if err := cache.InitCacheDb(a.appData.GetString(constants.CACHE_DB_PATH_KEY)); err != nil {
			logger.MainLogger.Fatalf("Error initialising cache db: %v", err)
		}
	}
	language.InitLangDb()

	ticker := time.NewTicker(1 * time.Second) // check for new queues every few second
	go func() {
		for {
			select {
			case <-ctx.Done():
				ticker.Stop()
				return
			case <-ticker.C:
				a.startNewQueues()
			}
		}
	}()
}
