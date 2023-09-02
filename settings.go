package main

import (
	"encoding/base64"
	"fmt"
	"image/color"
	"math/rand"
	"os"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"

	// "fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader/constants"
	"github.com/KJHJason/Cultured-Downloader/cryptography"
	"github.com/KJHJason/Cultured-Downloader/validators"
)

func readPath(path string) ([]byte, error) {
	if !iofuncs.PathExists(path) {
		return nil, fmt.Errorf("filepath does not exist")
	}

	fileBytes, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return fileBytes, nil
}

var masterPassword string
var securityForm *widget.Form
var resetSecurityContainer *fyne.Container
func promptMasterPassword(app fyne.App, win fyne.Window) {
	savedMasterPasswordHashStr := app.Preferences().String(constants.MasterPasswordHashKey)
	if savedMasterPasswordHashStr == "" {
		securityForm.Show()
		resetSecurityContainer.Hide()
		return
	}
	savedMasterPasswordHash, err := base64.StdEncoding.DecodeString(savedMasterPasswordHashStr)
	if err != nil {
		// shouldn't happen unless the user manually edited the preferences file
		app.Preferences().SetString(constants.MasterPasswordHashKey, "")
		panicWithDialog(err, win)
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
			securityForm.Hide()
			resetSecurityContainer.Show()
		} else {
			showErrDialog(fmt.Errorf("incorrect password"), win)
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

func getSettingsGUI(app fyne.App, win fyne.Window) *container.Scroll {
	title := canvas.NewText("Settings", color.White)
	title.TextStyle = fyne.TextStyle{
		Bold: true,
	}
	title.Alignment = fyne.TextAlignCenter
	title.TextSize = h1

	masterPasswordEntry := widget.NewPasswordEntry()
	masterPasswordEntry.Validator = validators.EmptyStr
	confirmMasterPasswordEntry := widget.NewPasswordEntry()
	confirmMasterPasswordEntry.Validator = validators.EmptyStr

	securityTitle := canvas.NewText("Security", color.White)
	securityTitle.TextSize = h2

	securityForm = &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Master Password:", Widget: masterPasswordEntry},
			{Text: "Confirm Master Password:", Widget: confirmMasterPasswordEntry, HintText: "Leave blank to disable encryption"},
		},
		OnSubmit: func() {
			if masterPasswordEntry.Text != confirmMasterPasswordEntry.Text {
				showErrDialog(fmt.Errorf("passwords do not match"), win)
				return
			}

			hash := cryptography.HashPassword(masterPasswordEntry.Text)
			app.Preferences().SetString(constants.MasterPasswordHashKey, base64.StdEncoding.EncodeToString(hash))
			if err := cryptography.ReEncryptEncryptedFields(app, masterPassword, masterPasswordEntry.Text); err != nil {
				cryptography.ResetEncryptedFields(app)
				panicWithDialog(err, win)
			}
			dialog.ShowInformation("Success!", "Your master password has been set!", win)
			securityForm.Hide()
			resetSecurityContainer.Show()
		},
		SubmitText: "Save",
	}

	resetNote := canvas.NewText("You already have set a master password to encrypt your sensitive data on your computer.", color.White)
	resetNote.Alignment = fyne.TextAlignCenter
	resetSecurityContainer = container.New(
		layout.NewVBoxLayout(),
		resetNote,
		container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
		container.New(
			layout.NewHBoxLayout(),
			layout.NewSpacer(),
			widget.NewButton("Reset Master Password", func() {
				oldMasterPasswordEntry := widget.NewPasswordEntry()
				oldMasterPasswordEntry.Validator = validators.EmptyStr

				masterPasswordEntry := widget.NewPasswordEntry()
				masterPasswordEntry.Validator = validators.EmptyStr

				confirmMasterPasswordEntry := widget.NewPasswordEntry()
				confirmMasterPasswordEntry.Validator = validators.EmptyStr

				var changeDialog *dialog.CustomDialog
				changeDialogContent := container.New(
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
					container.New(
						layout.NewHBoxLayout(),
						layout.NewSpacer(),
						widget.NewButton("Cancel", func() {
							changeDialog.Hide()
						}),
						widget.NewButton("Change", func() {
							if masterPasswordEntry.Validate() != nil || confirmMasterPasswordEntry.Validate() != nil || oldMasterPasswordEntry.Validate() != nil {
								return
							}

							if masterPasswordEntry.Text != confirmMasterPasswordEntry.Text {
								showErrDialog(fmt.Errorf("passwords do not match"), win)
								return
							}

							time.Sleep(time.Duration(rand.Intn(1500)) * time.Millisecond)
							if oldMasterPasswordEntry.Text != masterPassword {
								showErrDialog(fmt.Errorf("incorrect password"), win)
								return
							}

							hash := cryptography.HashPassword(masterPasswordEntry.Text)
							app.Preferences().SetString(constants.MasterPasswordHashKey, base64.StdEncoding.EncodeToString(hash))
							if err := cryptography.ReEncryptEncryptedFields(app, oldMasterPasswordEntry.Text, masterPasswordEntry.Text); err != nil {
								cryptography.ResetEncryptedFields(app)
								panicWithDialog(err, win)
							}
							masterPassword = masterPasswordEntry.Text
							changeDialog.Hide()
							dialog.ShowInformation("Success!", "Your master password has been changed!", win)
						}),
					),
				)
				changeDialog = dialog.NewCustomWithoutButtons(
					"Change Master Password?",
					changeDialogContent,
					win,
				)
				changeDialog.Show()
			}),
			widget.NewButton("Reset Security", func() {
				resetDialog := dialog.NewConfirm(
					"Reset Security?",
					"Are you sure you want to reset your security settings?\nThis will delete your master password and will decrypt all encrypted fields!",
					func(confirm bool) {
						if confirm {
							app.Preferences().SetString(constants.MasterPasswordHashKey, "")
							cryptography.DecryptEncryptedFields(app, masterPassword)
							cryptography.ResetMasterKeySalt(app)
							masterPassword = ""
							resetSecurityContainer.Hide()
							securityForm.Show()
						}
					},
					win,
				)
				resetDialog.SetDismissText("Cancel")
				resetDialog.SetConfirmText("Reset")
				resetDialog.Show()
			}),
			layout.NewSpacer(),
		),
		container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
	)

	gdriveApiKeyEntry := widget.NewEntry()
	gdriveApiKeyEntry.SetText(app.Preferences().String(constants.GdriveApiKeyKey))
	gdriveApiKeyEntry.Validator = validators.EmptyStr

	gdriveServiceAccPathEntry := widget.NewEntry()
	gdriveServiceAccPathEntry.SetText(app.Preferences().String(constants.GdriveServiceAccKey))
	gdriveServiceAccPathEntry.Validator = validators.Filepath

	driveTitle := canvas.NewText("Google Drive API", color.White)
	driveTitle.TextSize = h2
	driveForm := &widget.Form{
		Items: []*widget.FormItem{
			{Text: "API Key:", Widget: gdriveApiKeyEntry},
			{Text: "Service Account Filepath:", Widget: gdriveServiceAccPathEntry},
		},
		OnSubmit: func() {
			if gdriveServiceAccPathEntry.Text != "" {
				serviceAccPath := iofuncs.CleanPathName(gdriveServiceAccPathEntry.Text)
				fileBytes, err := readPath(serviceAccPath)
				if err != nil {
					showErrDialog(err, win)
					return
				}

				var encodedFileBytes string
				if masterPassword != "" {
					encryptedFileBytes, err := cryptography.EncryptWithPassword(fileBytes, masterPassword)
					if err != nil {
						panicWithDialog(err, win)
					}

					encodedFileBytes = base64.StdEncoding.EncodeToString(encryptedFileBytes)
				} else {
					encodedFileBytes = base64.StdEncoding.EncodeToString(fileBytes)
				}
				fmt.Println("GDrive Service Account JSON:", encodedFileBytes)
				app.Preferences().SetString(constants.GdriveServiceAccKey, encodedFileBytes)
			}

			app.Preferences().SetString(constants.GdriveApiKeyKey, gdriveApiKeyEntry.Text)
		},
		SubmitText: "Save",
	}

	dlPrefTitle := canvas.NewText("Download Preferences", color.White)
	dlPrefTitle.TextSize = h2
	dlPrefDesc := canvas.NewText("These settings are automatically saved and will be applied to all supported platforms like Fantia.", color.White)

	dlThumbnail := widget.NewCheck("Post Thumbnail", func(value bool) {
		app.Preferences().SetBool(constants.DlThumbnailKey, value)
	})
	dlThumbnail.SetChecked(app.Preferences().Bool(constants.DlThumbnailKey))

	dlImages := widget.NewCheck("Post Images", func(value bool) {
		app.Preferences().SetBool(constants.DlImagesKey, value)
	})
	dlImages.SetChecked(app.Preferences().Bool(constants.DlImagesKey))

	dlAttachments := widget.NewCheck("Post Attachments", func(value bool) {
		app.Preferences().SetBool(constants.DlAttachmentsKey, value)
	})
	dlAttachments.SetChecked(app.Preferences().Bool(constants.DlAttachmentsKey))

	dlGdrive := widget.NewCheck("GDrive Links", func(value bool) {
		app.Preferences().SetBool(constants.DlGdriveKey, value)
	})
	dlGdrive.SetChecked(app.Preferences().Bool(constants.DlGdriveKey))

	detectOtherUrls := widget.NewCheck("Detect other URLs like MEGA", func(value bool) {
		app.Preferences().SetBool(constants.DetectOtherUrlsKey, value)
	})
	detectOtherUrls.SetChecked(app.Preferences().Bool(constants.DetectOtherUrlsKey))

	dlPrefGrid := container.New(
		layout.NewGridLayout(2),
		dlThumbnail, dlImages,
		dlAttachments, dlGdrive,
		detectOtherUrls,
	)

	fantiaCookieValueEntry := widget.NewEntry()
	fantiaCookieValueEntry.Validator = validators.EmptyStr
	fantiaCookiePathEntry := widget.NewEntry()
	fantiaCookiePathEntry.Validator = validators.EmptyStr
	fantiaTitle := canvas.NewText("Fantia", color.White)
	fantiaTitle.TextSize = h2
	fantiaForm := &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Session cookie value:", Widget: fantiaCookieValueEntry},
			{Text: "Cookie text filepath:", Widget: fantiaCookiePathEntry},
		},
		OnSubmit: func() {
			fmt.Println("cookie value:", fantiaCookieValueEntry.Text)
			fmt.Println("cookie text filepath:", fantiaCookiePathEntry.Text)
		},
		SubmitText: "Save",
	}

	vBox := container.New(
		layout.NewVBoxLayout(),
		title,
		container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
		widget.NewSeparator(),

		securityTitle,
		resetSecurityContainer,
		securityForm,
		widget.NewSeparator(),

		driveTitle,
		driveForm,
		widget.NewSeparator(),

		dlPrefTitle,
		dlPrefDesc,
		dlPrefGrid,
		container.New(layout.NewHBoxLayout(), layout.NewSpacer()),
		widget.NewSeparator(),

		fantiaTitle,
		fantiaForm,
		widget.NewSeparator(),
	)
	return container.NewScroll(vBox)
}
