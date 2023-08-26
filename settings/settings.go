package settings

import (
	"fmt"
	"image/color"

	"fyne.io/fyne/v2"
	// "fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	// "fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

func validatorTest(s string) error {
	if s == "" {
		return fmt.Errorf("cannot be empty")
	}
	return nil
}

func GetSettingsGUI() *fyne.Container {
	title := canvas.NewText("Settings", color.White)
	title.TextStyle = fyne.TextStyle{
		Bold: true,
	}
	title.Alignment = fyne.TextAlignCenter
	title.TextSize = 24

	entry := widget.NewEntry()
	textArea := widget.NewMultiLineEntry()
	entry.Validator = validatorTest
	textArea.Validator = validatorTest

	form := &widget.Form{
		Items: []*widget.FormItem{ 
			{Text: "Entry", Widget: entry},
			{Text: "Multiline", Widget: textArea},
		},
		OnSubmit: func() { 
			fmt.Println("Form submitted:", entry.Text)
			fmt.Println("multiline:", textArea.Text)
		},
		SubmitText: "Save",
		CancelText: "Cancel",
	}

	hBox := container.New(layout.NewHBoxLayout(), layout.NewSpacer(), layout.NewSpacer())
	vBox := container.New(layout.NewVBoxLayout(), title, hBox, widget.NewSeparator(), form)
	return vBox
}
