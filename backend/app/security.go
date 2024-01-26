package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/crypto"
)

func (app *App) CheckMasterPassword(password string) bool {
	if !crypto.VerifyPassword(password, app.appData.GetMasterPasswordHash()) {
		return false
	}
	app.appData.SetMasterPassword(password)
	return true
}

func (app *App) ResetEncryptedFields() {
	app.appData.SetString(constants.MasterPasswordHashKey, "")
	app.resetMasterPassword()
	appdata.ResetEncryptedFields(app.appData)
}
