package app

import (
	"context"

	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx
	if constants.UserConfigDirErr != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:          runtime.ErrorDialog,
			Title:         "Error getting config directory path!",
			Message:       "Your OS might not be supported. Please refer to the logs or report this issue on GitHub.",
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
			Type:          runtime.ErrorDialog,
			Title:         "Error loading data from file!",
			Message:       "Please refer to the logs or report this issue on GitHub.",
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v", err, initialLoadErr)
		}
		panic("Error loading data from file!")
	}
	a.appData = appData
}
