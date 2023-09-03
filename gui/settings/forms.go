package settings

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/storage"
	"fyne.io/fyne/v2/widget"
	"github.com/KJHJason/Cultured-Downloader/gui"
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

		filepathEntry.SetText(reader.URI().String())
	}, win)

	if len(extensionFilter) > 0 {
		filePicker.SetFilter(storage.NewExtensionFileFilter(extensionFilter))
	}
	return filePicker
}
