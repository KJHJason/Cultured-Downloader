package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader/icons"
)

func main() {
	myApp := app.NewWithID("cultured.downloader")
	myApp.SetIcon(icons.CulturedDownloaderIcon)
	myWindow := myApp.NewWindow("Cultured Downloader")
	myWindow.Resize(fyne.NewSize(800, 600))

	fantiaWidget := widget.NewLabel("Fantia")
	pixivFanboxWidget := widget.NewLabel("Pixiv Fanbox")
	pixivWidget := widget.NewLabel("Pixiv")
	kemonoWidget := widget.NewLabel("Kemono")
	settingsWidget := widget.NewLabel("Settings")

	tabs := container.NewAppTabs(
		container.NewTabItemWithIcon("", icons.FantiaIcon, fantiaWidget),
		container.NewTabItemWithIcon("", icons.PixivFanboxIcon, pixivFanboxWidget),
		container.NewTabItemWithIcon("", icons.PixivIcon, pixivWidget),
		container.NewTabItemWithIcon("", icons.KemonoIcon, kemonoWidget),
		container.NewTabItemWithIcon("", theme.SettingsIcon(), settingsWidget),
	)
	tabs.SetTabLocation(container.TabLocationLeading)

	myWindow.SetContent(tabs)
	myWindow.ShowAndRun()
}
