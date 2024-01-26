package app

import (
	"context"
	"fmt"

	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx					context.Context
	masterPassword		string
	masterPasswordHash	[]byte
	appData				*appdata.AppData
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

func (a *App) resetMasterPassword() {
	a.masterPassword = ""
	a.masterPasswordHash = nil
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
