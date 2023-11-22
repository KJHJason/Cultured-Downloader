package main

import (
	"context"
	"fmt"

	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx context.Context
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
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

	if appdata.InitialLoadErr != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:          runtime.ErrorDialog,
			Title:         "Error loading data from file!",
			Message:       "Please refer to the logs or report this issue on GitHub.",
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v", err, appdata.InitialLoadErr)
		}
		panic("Error loading data from file!")
	}
}

func (a *App) GetName() string {
	return appdata.Data.GetString("name")
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	if err := appdata.Data.SetString("name", name); err != nil {
		runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:          runtime.ErrorDialog,
			Title:         "Error saving name!",
			Message:       "Please refer to the logs or report this issue on GitHub.",
		})
	}
	return fmt.Sprintf("Hello %s, Your name has been saved!", name)
}
