package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) PromptMasterPassword() bool {
	hashOfMasterPasswordHash, masterPasswordSalt := a.appData.GetMasterPasswordHash()
	return len(hashOfMasterPasswordHash) > 0 && len(masterPasswordSalt) > 0
}

func (a *App) CheckMasterPassword(password string) bool {
	return a.appData.VerifyMasterPassword(password)
}

func (a *App) SetMasterPassword(password string) error {
	return a.appData.ChangeMasterPassword("", password)
}

func (a *App) ChangeMasterPassword(oldPassword, newPassword string) error {
	return a.appData.ChangeMasterPassword(oldPassword, newPassword)
}

func (a *App) RemoveMasterPassword() error {
	err := a.appData.Unset(constants.MASTER_PASS_SALT_KEY)
	if err != nil {
		return err
	}

	err = a.appData.Unset(constants.HASH_OF_MASTER_PASS_HASH_KEY)
	if err != nil {
		return err
	}

	return a.appData.ResetMasterPassword()
}
