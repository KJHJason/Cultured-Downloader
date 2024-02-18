package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
)

func (app *App) GetPreferences() appdata.Preferences {
	return app.appData.GetPreferences()
}

func (app *App) SetPreferences(platform string, preferences appdata.Preferences) error {
	return app.appData.SetPreferences(platform, preferences)
}
