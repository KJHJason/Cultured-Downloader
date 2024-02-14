package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/crypto"
)

func (app *App) PromptMasterPassword() bool {
	hashOfMasterPasswordHash, masterPasswordSalt := app.appData.GetMasterPasswordHash()
	return len(hashOfMasterPasswordHash) > 0 && len(masterPasswordSalt) > 0
}

func (app *App) CheckMasterPassword(password string) bool {
	hashOfMasterPasswordHash, masterPasswordSalt := app.appData.GetMasterPasswordHash()
	hashedPassword := crypto.HashStringWithSalt(password, masterPasswordSalt)
	if !crypto.VerifyBytes(hashedPassword, hashOfMasterPasswordHash) {
		return false
	}
	app.appData.SetMasterPassword(password)
	return true
}

func (app *App) SetMasterPassword(password string) error {
	return app.appData.ChangeMasterPassword("", password)
}

func (app *App) ChangeMasterPassword(oldPassword, newPassword string) error {
	return app.appData.ChangeMasterPassword(oldPassword, newPassword)
}

func (app *App) ResetEncryptedFields() {
	app.appData.Unset(constants.MasterPasswordSaltKey)
	app.appData.Unset(constants.HashOfMasterPasswordHashKey)
	app.appData.ResetMasterPassword()
}
