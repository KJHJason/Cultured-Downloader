package main

import (
	"fmt"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	// "fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

func validatorSettingTest(s string) error {
	if s == "" {
		return fmt.Errorf("cannot be empty")
	}
	return nil
}

const (
	gdriveApiKeyKey         = "gdriveApiKey"
	gdriveServiceAccPathKey = "gdriveServiceAccPath"

	dlThumbnailKey     = "dlThumbnail"
	dlImagesKey        = "dlImages"
	dlAttachmentsKey   = "dlAttachments"
	dlGdriveKey        = "dlGdrive"
	detectOtherUrlsKey = "detectOtherUrls"

	fantiaCookieValueKey = "fantiaCookieValue"
	fantiaCookiePathKey  = "fantiaCookiePath"
)

func getSettingsGUI() *container.Scroll {
	app := fyne.CurrentApp()
	title := canvas.NewText("Settings", color.White)
	title.TextStyle = fyne.TextStyle{
		Bold: true,
	}
	title.Alignment = fyne.TextAlignCenter
	title.TextSize = h1

	// TODO: add encryption for sensitive data
	masterPasswordEntry := widget.NewPasswordEntry()
	masterPasswordEntry.Validator = validatorSettingTest

	generalTitle := canvas.NewText("General", color.White)
	generalTitle.TextSize = h2
	generalForm := &widget.Form{
		Items: []*widget.FormItem{ 
			{Text: "Master Password:", Widget: masterPasswordEntry, HintText: "Leave blank to disable encryption"},
		},
		OnSubmit: func() { 
			fmt.Println("Master password submitted:", masterPasswordEntry.Text)
		},
		SubmitText: "Save",
	}

	gdriveApiKeyEntry := widget.NewEntry()
	gdriveApiKeyEntry.SetText(app.Preferences().String(gdriveApiKeyKey))
	gdriveApiKeyEntry.Validator = validatorSettingTest

	gdriveServiceAccPathEntry := widget.NewEntry()
	gdriveServiceAccPathEntry.SetText(app.Preferences().String(gdriveServiceAccPathKey))
	gdriveServiceAccPathEntry.Validator = validatorSettingTest

	driveTitle := canvas.NewText("Google Drive API", color.White)
	driveTitle.TextSize = h2
	driveForm := &widget.Form{
		Items: []*widget.FormItem{ 
			{Text: "API Key:", Widget: gdriveApiKeyEntry},
			{Text: "Service Account Filepath:", Widget: gdriveServiceAccPathEntry},
		},
		OnSubmit: func() { 
			fmt.Println("GDrive API Key submitted:", gdriveApiKeyEntry.Text)
			fmt.Println("GDrive Service Account JSON filepath submitted:", gdriveServiceAccPathEntry.Text)
			app.Preferences().SetString(gdriveApiKeyKey, gdriveApiKeyEntry.Text)
			app.Preferences().SetString(gdriveServiceAccPathKey, gdriveServiceAccPathEntry.Text)
		},
		SubmitText: "Save",
	}

	dlPrefTitle := canvas.NewText("Download Preferences", color.White)
	dlPrefTitle.TextSize = h2
	dlPrefDesc := canvas.NewText("These settings are automatically saved and will be applied to all supported platforms like Fantia.", color.White)

	dlThumbnail := widget.NewCheck("Post Thumbnail", func(value bool) {
		app.Preferences().SetBool(dlThumbnailKey, value)
	})
	dlThumbnail.SetChecked(app.Preferences().Bool(dlThumbnailKey))

	dlImages := widget.NewCheck("Post Images", func(value bool) {
		app.Preferences().SetBool(dlImagesKey, value)
	})
	dlImages.SetChecked(app.Preferences().Bool(dlImagesKey))

	dlAttachments := widget.NewCheck("Post Attachments", func(value bool) {
		app.Preferences().SetBool(dlAttachmentsKey, value)
	})
	dlAttachments.SetChecked(app.Preferences().Bool(dlAttachmentsKey))

	dlGdrive := widget.NewCheck("GDrive Links", func(value bool) {
		app.Preferences().SetBool(dlGdriveKey, value)
	})
	dlGdrive.SetChecked(app.Preferences().Bool(dlGdriveKey))

	detectOtherUrls := widget.NewCheck("Detect other URLs like MEGA", func(value bool) {
		app.Preferences().SetBool(detectOtherUrlsKey, value)
	})
	detectOtherUrls.SetChecked(app.Preferences().Bool(detectOtherUrlsKey))

	dlPrefGrid := container.New(
		layout.NewGridLayout(2), 
		dlThumbnail, dlImages,
		dlAttachments, dlGdrive,
		detectOtherUrls,
	)

	fantiaCookieValueEntry := widget.NewEntry()
	fantiaCookieValueEntry.Validator = validatorSettingTest
	fantiaCookiePathEntry := widget.NewEntry()
	fantiaCookiePathEntry.Validator = validatorSettingTest
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

		generalTitle,
		generalForm,
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
