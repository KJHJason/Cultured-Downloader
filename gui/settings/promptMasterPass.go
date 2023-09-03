package settings

import (
	"encoding/base64"
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader/constants"
	"github.com/KJHJason/Cultured-Downloader/cryptography"
	"github.com/KJHJason/Cultured-Downloader/validators"
	"github.com/KJHJason/Cultured-Downloader/gui"
)

func showSensitiveEntries(app fyne.App, win fyne.Window) {
	if masterPassword == "" {
		gdriveApiKeyEntry.SetText(app.Preferences().String(constants.GdriveApiKeyKey))
	} else {
		decrypted, err := cryptography.DecryptEncryptedField(app, constants.GdriveApiKeyKey, masterPassword, false)
		if err != nil {
			app.Preferences().SetString(constants.GdriveApiKeyKey, "")
			gui.PanicWithDialog(err, win)
		}
		gdriveApiKeyEntry.SetText(decrypted)
	}
}

func PromptMasterPassword(app fyne.App, win fyne.Window) {
	savedMasterPasswordHashStr := app.Preferences().String(constants.MasterPasswordHashKey)
	if savedMasterPasswordHashStr == "" {
		showSensitiveEntries(app, win)
		securityForm.Show()
		resetSecurityContainer.Hide()
		return
	}
	savedMasterPasswordHash, err := base64.StdEncoding.DecodeString(savedMasterPasswordHashStr)
	if err != nil {
		// shouldn't happen unless the user manually edited the preferences file
		app.Preferences().SetString(constants.MasterPasswordHashKey, "")
		gui.PanicWithDialog(err, win)
	}

	masterPasswordEntry := widget.NewPasswordEntry()
	masterPasswordEntry.Validator = validators.EmptyStr

	var modal *widget.PopUp
	forgotPassBtn := widget.NewButton("Forgot Password?", func() {
		resetDialog := dialog.NewConfirm(
			"Reset Encrypted Fields?",
			"Forgot your password? Cultured Downloader will reset all\nyour encrypted fields so that you can use the program again!",
			func(confirm bool) {
				if confirm {
					app.Preferences().SetString(constants.MasterPasswordHashKey, "")
					masterPassword = ""
					cryptography.ResetEncryptedFields(app)
					modal.Hide()
					securityForm.Show()
					resetSecurityContainer.Hide()
				}
			},
			win,
		)
		resetDialog.SetDismissText("Cancel")
		resetDialog.SetConfirmText("Reset")
		resetDialog.Show()
	})
	submitBtn := widget.NewButton("Submit", func() {
		if cryptography.VerifyPassword(masterPasswordEntry.Text, savedMasterPasswordHash) {
			masterPassword = masterPasswordEntry.Text
			modal.Hide()
			showSensitiveEntries(app, win)
			securityForm.Hide()
			resetSecurityContainer.Show()
		} else {
			gui.ShowErrDialog(fmt.Errorf("incorrect password"), win)
			return
		}
	})
	modal = widget.NewModalPopUp(
		container.New(
			layout.NewVBoxLayout(),
			widget.NewLabel("Enter Master Password:"),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
			masterPasswordEntry,
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer(), forgotPassBtn, submitBtn),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
		),
		win.Canvas(),
	)
	modal.Resize(fyne.NewSize(300, 150))
	modal.Show()
}
