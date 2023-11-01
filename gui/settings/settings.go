package settings

import (
	"context"
	"encoding/base64"
	"fmt"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader/constants"
	"github.com/KJHJason/Cultured-Downloader/cryptography"
	"github.com/KJHJason/Cultured-Downloader/validators"
	"github.com/KJHJason/Cultured-Downloader/gui"

	"github.com/KJHJason/Cultured-Downloader-Logic"
	cdlconstants "github.com/KJHJason/Cultured-Downloader-Logic/constants"
)

var (
	masterPassword string

	securityForm           *widget.Form
	resetSecurityContainer *fyne.Container

	gdriveApiKeyEntry1 *widget.Entry
	gdriveApiKeyEntry2 *widget.Entry
)

func GetSettingsGUI(app fyne.App, win fyne.Window) *container.Scroll {
	title := canvas.NewText("Settings", color.White)
	title.TextStyle = fyne.TextStyle{
		Bold: true,
	}
	title.Alignment = fyne.TextAlignCenter
	title.TextSize = gui.H1

	masterPasswordEntry := widget.NewPasswordEntry()
	masterPasswordEntry.Validator = validators.EmptyStr
	confirmMasterPasswordEntry := widget.NewPasswordEntry()
	confirmMasterPasswordEntry.Validator = validators.EmptyStr

	securityTitle := canvas.NewText("Security", color.White)
	securityTitle.TextSize = gui.H2

	securityForm = &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Master Password:", Widget: masterPasswordEntry},
			{Text: "Confirm Master Password:", Widget: confirmMasterPasswordEntry, HintText: "Leave blank to disable encryption"},
		},
		OnSubmit: func() {
			if masterPasswordEntry.Text != confirmMasterPasswordEntry.Text {
				gui.ShowErrDialog(fmt.Errorf("passwords do not match"), win)
				return
			}

			var err error
			hash := cryptography.HashPassword(masterPasswordEntry.Text)
			app.Preferences().SetString(constants.MasterPasswordHashKey, base64.StdEncoding.EncodeToString(hash))
			if masterPassword != "" {
				err = cryptography.ReEncryptEncryptedFields(app, masterPassword, masterPasswordEntry.Text)
			} else {
				err = cryptography.EncryptPlainFields(app, masterPasswordEntry.Text)
			}

			if err != nil {
				cryptography.ResetEncryptedFields(app)
				gui.PanicWithDialog(err, win)
			}

			masterPassword = masterPasswordEntry.Text
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
			widget.NewButton("Change Master Password", func() {
				getChangeDialogContent(app, win).Show()
			}),
			widget.NewButton("Remove Master Password", func() {
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

	gdriveApiKeyEntry1 = getGdriveApiKeyEntry(validators.GdriveApiKey)

	gdriveServiceAccPathEntry := widget.NewEntry()
	gdriveServiceAccPathEntry.Validator = validators.Filepath

	driveFilePicker := getFilePicker(win, gdriveServiceAccPathEntry, ".json")

	driveTitle := canvas.NewText("Google Drive API", color.White)
	driveTitle.TextSize = gui.H2

	var driveForm, driveFormWithPath *widget.Form
	driveForm = &widget.Form{
		Items: []*widget.FormItem{
			{Text: "API Key:", Widget: gdriveApiKeyEntry1},
			{Text: "Service Account Filepath:", Widget: container.New(
				layout.NewVBoxLayout(),
				gdriveServiceAccPathEntry,
				widget.NewButtonWithIcon("Browse", theme.FileIcon(), func() {
					driveFilePicker.Show()
				}),
			)},
		},
		OnSubmit: func() {
			if gdriveServiceAccPathEntry.Text != "" {
				fileBytes, err := readPath(gdriveServiceAccPathEntry.Text)
				if err != nil {
					gui.ShowErrDialog(err, win)
					return
				}

				if _, err := cdlogic.GetNewGDrive("", cdlconstants.USER_AGENT, fileBytes, 5, context.Background()); err != nil {
					gui.ShowDialogWithWordWrap(
						gui.DialogText{
							Title:    "Error Validating Service Account JSON",
							Messages: []*widget.Label{
								widget.NewLabel("Could not validate the service account\nJSON file due to the following error:"),
								gui.GetDefaultLabelWithWrap(err.Error()),
							},
						},
						win,
					)
					return
				}

				var encodedFileBytes string
				if masterPassword != "" {
					encryptedFileBytes, err := cryptography.EncryptWithPassword(fileBytes, masterPassword)
					if err != nil {
						gui.PanicWithDialog(err, win)
					}

					encodedFileBytes = base64.StdEncoding.EncodeToString(encryptedFileBytes)
				} else {
					encodedFileBytes = base64.StdEncoding.EncodeToString(fileBytes)
				}
				app.Preferences().SetString(constants.GdriveServiceAccKey, encodedFileBytes)
				driveForm.Hide()
				driveFormWithPath.Show()
				dialog.ShowInformation("Success!", "Your Google Drive service account JSON has been saved!", win)
			}

			if gdriveApiKeyEntry1.Text != "" {
				gdriveApiKeySubmitLogic(gdriveApiKeyEntry1.Text, app, win)
			}
		},
		SubmitText: "Save",
	}

	gdriveApiKeyEntry2 = getGdriveApiKeyEntry(validators.GdriveApiKeyNoEmpty)
	driveFormWithPath = &widget.Form{
		Items: []*widget.FormItem{
			{Text: "API Key:", Widget: gdriveApiKeyEntry2},
			{Text: "Service Account JSON:", Widget: container.New(
				layout.NewVBoxLayout(),
				widget.NewButtonWithIcon("View Service Account JSON", theme.FileIcon(), func() {
					var err error
					var gdriveJson []byte
					if masterPassword != "" {
						gdriveJson, err = cryptography.DecryptEncryptedFieldBytes(app, constants.GdriveServiceAccKey, masterPassword)
					} else {
						encodedGdriveJson := app.Preferences().String(constants.GdriveServiceAccKey)
						gdriveJson, err = base64.StdEncoding.DecodeString(encodedGdriveJson)
					}

					if err != nil {
						gui.ShowErrDialog(err, win)
						return
					}

					gui.ShowDialogWithWordWrap(
						gui.DialogText{
							Title:    "Service Account JSON",
							Messages: []*widget.Label{gui.GetDefaultLabelWithWrap(string(gdriveJson))},
						}, 
						win,
					)
				}),
				widget.NewButtonWithIcon("Remove", theme.DeleteIcon(), func() {
					app.Preferences().SetString(constants.GdriveServiceAccKey, "")
					driveFormWithPath.Hide()
					driveForm.Show()
				}),
			)},
		},
		OnSubmit: func() {
			if gdriveApiKeyEntry2.Text != "" {
				gdriveApiKeySubmitLogic(gdriveApiKeyEntry2.Text, app, win)
			}
		},
	}

	if app.Preferences().String(constants.GdriveServiceAccKey) != "" {
		driveForm.Hide()
		driveFormWithPath.Show()
	} else {
		driveForm.Show()
		driveFormWithPath.Hide()
	}

	dlPrefTitle := canvas.NewText("Download Preferences", color.White)
	dlPrefTitle.TextSize = gui.H2
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
	fantiaTitle.TextSize = gui.H2

	fantiaFilePicker := getFilePicker(win, fantiaCookiePathEntry, ".txt", ".json")
	fantiaCookiePathEntryContainer := container.New(
		layout.NewVBoxLayout(),
		fantiaCookiePathEntry,
		widget.NewButtonWithIcon("Browse", theme.FileIcon(), func() {
			fantiaFilePicker.Show()
		}),
	)

	fantiaForm := &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Session cookie value:", Widget: fantiaCookieValueEntry},
			{Text: "Cookie text filepath:", Widget: fantiaCookiePathEntryContainer},
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
		driveFormWithPath,
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