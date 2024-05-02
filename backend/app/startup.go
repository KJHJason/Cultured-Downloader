package app

import (
	"context"
	"os"
	"time"
	"path/filepath"

	cdconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) GetDownloadDir() (dirPath string, hasErr bool) {
	savedDirPath := a.appData.GetString(constants.DOWNLOAD_KEY)
	if savedDirPath != "" && iofuncs.PathExists(savedDirPath) {
		return savedDirPath, false
	}

	desktopDir, err := os.UserHomeDir()
	if err != nil {
		logger.MainLogger.Errorf("Error getting user home directory: %w", err)
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error getting user home directory!",
			Message: "Please manually set the download directory in the settings.",
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v", 
				err, err,
			)
		}	
		return "", true
	}

	desktopDir = filepath.Join(desktopDir, "Cultured Downloader")
	if err := os.MkdirAll(desktopDir, constants.DEFAULT_PERM); err != nil {
		panic(err)
	}
	a.appData.SetString(constants.DOWNLOAD_KEY, desktopDir)
	return desktopDir, false
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx
	if constants.UserConfigDirErr != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error getting config directory path!",
			Message: "Your OS might not be supported. Please refer to the logs or report this issue on GitHub.",
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v", err, constants.UserConfigDirErr)
		}
		panic("Error getting config directory path!")
	}

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

	userAgent := a.appData.GetString(constants.UserAgentKey)
	if userAgent == "" {
		userAgent = cdconst.USER_AGENT
		a.appData.SetString(constants.UserAgentKey, userAgent)
	}

	lang := a.appData.GetString(constants.LANGUAGE_KEY)
	if lang == "" {
		lang = "en"
	}
	a.lang = lang

	

	ticker := time.NewTicker(2 * time.Second) // check for new queues every few second
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
