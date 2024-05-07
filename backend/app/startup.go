package app

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) GetDownloadDir() (dirPath string, err error) {
	savedDirPath := a.appData.GetString(constants.DOWNLOAD_KEY)
	if savedDirPath != "" && iofuncs.PathExists(savedDirPath) {
		return savedDirPath, nil
	}

	desktopDir, err := os.UserHomeDir()
	if err != nil {
		logger.MainLogger.Errorf("Error getting user home directory: %v", err)
		return "", fmt.Errorf("error getting user home directory: %w\nPlease manually set the download directory in the settings", err)
	}

	desktopDir = filepath.Join(desktopDir, "Cultured Downloader")
	if err := os.MkdirAll(desktopDir, cdlconst.DEFAULT_PERMS); err != nil {
		panic(err)
	}
	a.appData.SetString(constants.DOWNLOAD_KEY, desktopDir)
	return desktopDir, nil
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

	lang := a.appData.GetString(constants.LANGUAGE_KEY)
	if lang == "" {
		lang = "en"
	}
	a.lang = lang

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
