package main

import (
	"context"
	"fmt"

	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
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
	if appdata.UserConfigDirErr != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:          runtime.ErrorDialog,
			Title:         "Error getting config directory path!",
			Message:       "Your OS might not be supported. Please report this issue on GitHub.",
		})

		if err != nil {
			panic(err) // TODO: log error
		}
		panic("Error getting config directory path!")
	}
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s, It's show time!", name)
}
