package gui

import (
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
)

func errDialog(err error, exit bool, win fyne.Window) {
	if !exit {
		dialog.ShowError(err, win)
		return
	}

	dialog.ShowCustomConfirm(
		"Uh Oh! A fatal error has occurred!",
		"Log and Close",
		"Close",
		container.New(
			layout.NewVBoxLayout(),
			widget.NewLabel("Would you like to log the error and close the application?\nPlease report this error on GitHub!"),
			widget.NewLabelWithStyle(err.Error(), fyne.TextAlign(fyne.TextWrapWord), fyne.TextStyle{Monospace: true}),
		),
		func(log bool) {
			if log {
				logger.LogError(err, exit, logger.ERROR)
			} else {
				os.Exit(1)
			}
		},
		win,
	)
}

func PanicWithDialog(err error, win fyne.Window) {
	errDialog(err, true, win)
}

func ShowErrDialog(err error, win fyne.Window) {
	errDialog(err, false, win)
}
