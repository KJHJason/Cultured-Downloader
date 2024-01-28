package app

import (
	"context"
	"container/list"
	"fmt"

	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx					context.Context
	masterPassword		string
	masterPasswordHash	[]byte
	appData				*appdata.AppData
	downloadQueues		list.List // doubly linked list of DownloadQueue
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

func (a *App) GetName() string {
	return a.appData.GetString("name")
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	if err := a.appData.SetString("name", name); err != nil {
		runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:          runtime.ErrorDialog,
			Title:         "Error saving name!",
			Message:       "Please refer to the logs or report this issue on GitHub.",
		})
	}
	return fmt.Sprintf("Hello %s, Your name has been saved!", name)
}

func (app *App) GetDarkMode() bool {
	return app.appData.GetBool(constants.DarkModeKey)
}

func (app *App) SetDarkMode(darkMode bool) {
	app.appData.SetBool(constants.DarkModeKey, darkMode)
}
