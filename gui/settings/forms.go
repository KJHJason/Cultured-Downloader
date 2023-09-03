package settings

import (
	"context"
	"encoding/base64"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/storage"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader/constants"
	"github.com/KJHJason/Cultured-Downloader/cryptography"
	"github.com/KJHJason/Cultured-Downloader/gui"

	"github.com/KJHJason/Cultured-Downloader-Logic"
	cdlconstants "github.com/KJHJason/Cultured-Downloader-Logic/constants"
)

func getFilePicker(win fyne.Window, filepathEntry *widget.Entry, extensionFilter... string) *dialog.FileDialog {
	var filePicker *dialog.FileDialog
	filePicker = dialog.NewFileOpen(func(reader fyne.URIReadCloser, err error) {
		if err != nil {
			filePicker.Hide()
			gui.ShowErrDialog(err, win)
			return
		}

		if reader == nil {
			filePicker.Hide()
			return
		}

		filePath := reader.URI().String()
		filepathEntry.SetText(strings.TrimPrefix(filePath, "file://"))
	}, win)

	if len(extensionFilter) > 0 {
		filePicker.SetFilter(storage.NewExtensionFileFilter(extensionFilter))
	}
	return filePicker
}

func getGdriveApiKeyEntry(validator func(s string) error) *widget.Entry {
	gdriveApiKeyEntry := widget.NewEntry()
	gdriveApiKeyEntry.Validator = validator
	return gdriveApiKeyEntry
}

func gdriveApiKeySubmitLogic(entry string, app fyne.App, win fyne.Window) {
	_, err := cdlogic.GetNewGDrive(entry, cdlconstants.USER_AGENT, nil, 5, context.Background())
	if err != nil {
		gui.ShowErrDialog(err, win)
		return
	}

	gdriveApiKeyEntry1.SetText(entry)
	gdriveApiKeyEntry2.SetText(entry)

	apiKeyToSave := entry
	if masterPassword != "" {
		encryptedApiKey, err := cryptography.EncryptWithPassword([]byte(gdriveApiKeyEntry1.Text), masterPassword)
		if err != nil {
			gui.PanicWithDialog(err, win)
		}
		apiKeyToSave = base64.StdEncoding.EncodeToString(encryptedApiKey)
	}

	app.Preferences().SetString(constants.GdriveApiKeyKey, apiKeyToSave)
	dialog.ShowInformation("Success!", "Your Google Drive API key has been saved!", win)
}
