package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (app *App) PromptMasterPassword() bool {
	hashOfMasterPasswordHash, masterPasswordSalt := app.appData.GetMasterPasswordHash()
	return len(hashOfMasterPasswordHash) > 0 && len(masterPasswordSalt) > 0
}

func (app *App) CheckMasterPassword(password string) bool {
	return app.appData.VerifyMasterPassword(password)
}

func (app *App) SetMasterPassword(password string) error {
	return app.appData.ChangeMasterPassword("", password)
}

func (app *App) ChangeMasterPassword(oldPassword, newPassword string) error {
	return app.appData.ChangeMasterPassword(oldPassword, newPassword)
}

func (app *App) RemoveMasterPassword() error {
	err := app.appData.Unset(constants.MasterPasswordSaltKey)
	if err != nil {
		return err
	}

	err = app.appData.Unset(constants.HashOfMasterPasswordHashKey)
	if err != nil {
		return err
	}

	return app.appData.ResetMasterPassword()
}
