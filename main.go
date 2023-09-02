package main

import (
	xtheme "fyne.io/x/fyne/theme"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader/icons"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
)

func errDialog(err error, exit bool, win fyne.Window) {
	dialog.ShowError(err, win)
	logger.LogError(err, exit, logger.ERROR)
}

func panicWithDialog(err error, win fyne.Window) {
	errDialog(err, true, win)
}

func showErrDialog(err error, win fyne.Window) {
	errDialog(err, false, win)
}

func main() {
	myApp := app.NewWithID("cultured.downloader")
	myApp.Settings().SetTheme(xtheme.AdwaitaTheme())
	myApp.SetIcon(icons.ResourceCulturedDownloaderLogoPng)
	myWindow := myApp.NewWindow("Cultured Downloader")
	myWindow.Resize(fyne.NewSize(800, 600))

	homeCanvas := widget.NewLabel("Home")
	fantiaCanvas := getFantiaGUI(myWindow)
	pixivFanboxCanvas := widget.NewLabel("Pixiv Fanbox")
	pixivCanvas := widget.NewLabel("Pixiv")
	kemonoCanvas := widget.NewLabel("Kemono")
	downloadQueueCanvas := widget.NewLabel("Download Queue")
	settingsCanvas := getSettingsGUI(myApp, myWindow)

	tabs := container.NewAppTabs(
		container.NewTabItemWithIcon("", theme.HomeIcon(), homeCanvas),
		container.NewTabItemWithIcon("", icons.ResourceFantiaLogoPng, fantiaCanvas),
		container.NewTabItemWithIcon("", icons.ResourcePixivFanboxLogoPng, pixivFanboxCanvas),
		container.NewTabItemWithIcon("", icons.ResourcePixivLogoPng, pixivCanvas),
		container.NewTabItemWithIcon("", icons.ResourceKemonoLogoPng, kemonoCanvas),
		container.NewTabItemWithIcon("", theme.DownloadIcon(), downloadQueueCanvas),
		container.NewTabItemWithIcon("", theme.SettingsIcon(), settingsCanvas),
	)
	tabs.SetTabLocation(container.TabLocationLeading)

	myWindow.SetContent(tabs)
	myWindow.Show()
	promptMasterPassword(myApp, myWindow)
	myApp.Run()
}
