package app

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
	return a.appData.ResetMasterPassword()
}
