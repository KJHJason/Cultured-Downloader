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

const (
	title = "Culture Downloader"
	errTitle = "Uh Oh! A fatal error has occurred!"
	dismiss = "Close"
)

var defaultSize = fyne.NewSize(500, 300)

func GetDefaultLabelWithWrap(text string) *widget.Label {
	return widget.NewLabelWithStyle(text, fyne.TextAlign(fyne.TextWrapWord), fyne.TextStyle{Monospace: true})
}

func errDialog(err error, exit bool, win fyne.Window) {
	if !exit {
		errContent := container.New(
			layout.NewVBoxLayout(),
			widget.NewLabel("An error has occurred!\nPlease report this error on GitHub!"),
			GetDefaultLabelWithWrap(err.Error()),
		)
		errScroll := container.NewHScroll(errContent)
		d := dialog.NewCustom(
			errTitle,
			dismiss,
			container.NewStack(errScroll),
			win,
		)
		d.Resize(defaultSize)
		d.Show()
		return
	}

	errContent := container.New(
		layout.NewVBoxLayout(),
		widget.NewLabel("Would you like to log the error and close the application?\nPlease report this error on GitHub!"),
		widget.NewLabelWithStyle(err.Error(), fyne.TextAlign(fyne.TextWrapWord), fyne.TextStyle{Monospace: true}),
	)
	errScroll := container.NewHScroll(errContent)
	d := dialog.NewCustomConfirm(
		errTitle,
		"Log and Close",
		dismiss,
		container.NewStack(errScroll),
		func(log bool) {
			if log {
				logger.LogError(err, exit, logger.ERROR)
			} else {
				os.Exit(1)
			}
		},
		win,
	)
	d.Resize(defaultSize)
	d.Show()
}

func PanicWithDialog(err error, win fyne.Window) {
	errDialog(err, true, win)
}

func ShowErrDialog(err error, win fyne.Window) {
	errDialog(err, false, win)
}

type DialogText struct {
	Title, 
	Dismiss string

	Messages []*widget.Label
}

func (d *DialogText) validate() {
	if d.Title == "" {
		d.Title = title
	}
	if d.Dismiss == "" {
		d.Dismiss = dismiss
	}
}

func ShowDialogWithWordWrap(dialogText DialogText, win fyne.Window) {
	dialogText.validate()

	content := container.New(
		layout.NewVBoxLayout(),
	)
	for _, message := range dialogText.Messages {
		content.Add(message)
	}
	contentScroll := container.NewHScroll(content)

	d := dialog.NewCustom(
		dialogText.Title,
		dialogText.Dismiss,
		container.NewStack(contentScroll),
		win,
	)
	d.Resize(defaultSize)
	d.Show()
}
