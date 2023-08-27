package main

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"

	"github.com/KJHJason/Cultured-Downloader/progress"
)

func getNewFantiaEntry() *widget.Entry {
	entry := widget.NewEntry()
	entry.PlaceHolder = "Enter URL:"
	entry.Validator = validatorTest
	return entry
}

func getFantiaGUI(win fyne.Window) *container.Scroll {
	baseGuiEl := getBaseGuiElements("Fantia")
	grid := baseGuiEl.grid
	delBtn := baseGuiEl.delBtn
	addBtn := baseGuiEl.addBtn
	addTenBtn := baseGuiEl.addTenBtn
	resetBtn := baseGuiEl.resetBtn

	retrieveJsonCon, _ := progress.NewProgressBar(progress.RetrieveJsonLabel, "Something went wrong when obtaining posts details from Fantia!", win)

	instructions := widget.NewLabel("Enter the URLs of the posts you want to download.\nExample: https://fantia.jp/posts/123456, https://fantia.jp/fanclubs/123456")
	execute := widget.NewButtonWithIcon("Download!", theme.DownloadIcon(), func() {
		if len(grid.Objects) == 1 && grid.Objects[0].(*widget.Entry).Text == "" {
			dialog.ShowError(fmt.Errorf("There is no URL to download!"), win)
			return
		}

		for _, obj := range grid.Objects {
			entry := obj.(*widget.Entry)
			fmt.Println("text:", entry.Text)
		}
		grid.Objects = []fyne.CanvasObject{getNewFantiaEntry()}
	})

	hBtnBox := container.New(
		layout.NewHBoxLayout(),
		layout.NewSpacer(),
		resetBtn,
		delBtn,
		addBtn,
		addTenBtn,
	)
	dlBtnBox := container.New(
		layout.NewHBoxLayout(),
		layout.NewSpacer(),
		execute,
	)
	vBox := container.New(
		layout.NewVBoxLayout(), 
		baseGuiEl.title, 
		widget.NewSeparator(),

		retrieveJsonCon,

		instructions,
		grid,
		widget.NewSeparator(),

		hBtnBox,
		widget.NewSeparator(),
		dlBtnBox,
	)
	return container.NewVScroll(vBox)
}
