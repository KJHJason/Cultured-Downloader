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

func getChangeDialogContent(app fyne.App, win fyne.Window) *dialog.CustomDialog {
	oldMasterPasswordEntry := widget.NewPasswordEntry()
	oldMasterPasswordEntry.Validator = validators.EmptyStr

	masterPasswordEntry := widget.NewPasswordEntry()
	masterPasswordEntry.Validator = validators.EmptyStr

	confirmMasterPasswordEntry := widget.NewPasswordEntry()
	confirmMasterPasswordEntry.Validator = validators.EmptyStr

	changeDialog := dialog.NewCustomWithoutButtons(
		"Change Master Password?",
		container.New(
			layout.NewVBoxLayout(),
			widget.NewLabel("Enter your old master password:"),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),

			oldMasterPasswordEntry,
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),

			widget.NewLabel("Enter your new master password:"),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
			masterPasswordEntry,

			widget.NewLabel("Confirm your new master password:"),
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
			confirmMasterPasswordEntry,
			container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
		),
		win,
	)
	changeDialog.SetButtons([]fyne.CanvasObject{
		widget.NewButton("Cancel", func() {
			changeDialog.Hide()
		}),
		widget.NewButton("Change", func() {
			if masterPasswordEntry.Validate() != nil || confirmMasterPasswordEntry.Validate() != nil || oldMasterPasswordEntry.Validate() != nil {
				return
			}

			if masterPasswordEntry.Text != confirmMasterPasswordEntry.Text {
				gui.ShowErrDialog(fmt.Errorf("passwords do not match"), win)
				return
			}

			if oldMasterPasswordEntry.Text != masterPassword {
				gui.ShowErrDialog(fmt.Errorf("incorrect password"), win)
				return
			}

			hash := cryptography.HashPassword(masterPasswordEntry.Text)
			app.Preferences().SetString(constants.MasterPasswordHashKey, base64.StdEncoding.EncodeToString(hash))
			if err := cryptography.ReEncryptEncryptedFields(app, oldMasterPasswordEntry.Text, masterPasswordEntry.Text); err != nil {
				cryptography.ResetEncryptedFields(app)
				gui.PanicWithDialog(err, win)
			}
			masterPassword = masterPasswordEntry.Text
			changeDialog.Hide()
			dialog.ShowInformation("Success!", "Your master password has been changed!", win)
		}),
	})
	return changeDialog
}
