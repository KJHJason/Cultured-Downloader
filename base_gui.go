package main

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

func getNewEntry() *widget.Entry {
	entry := widget.NewEntry()
	entry.PlaceHolder = "Enter URL:"
	entry.Validator = validatorTest
	return entry
}

type baseGuiElements struct {
	title     *canvas.Text
	grid      *fyne.Container
	delBtn    *widget.Button
	addBtn    *widget.Button
	addTenBtn *widget.Button
	resetBtn  *widget.Button
}

const (
	h1 = 24
	h2 = 18
)

func getBaseGuiElements(titleStr string) baseGuiElements {
	title := canvas.NewText(titleStr, color.White)
	title.TextStyle = fyne.TextStyle{
		Bold: true,
	}
	title.Alignment = fyne.TextAlignCenter
	title.TextSize = h1

	grid := container.New(layout.NewGridLayout(1), getNewEntry())
	delBtn := widget.NewButtonWithIcon("Delete", theme.DeleteIcon(), func() {
		if len(grid.Objects) > 1 {
			grid.Objects = grid.Objects[:len(grid.Objects)-1]
		}
	})
	addBtn := widget.NewButtonWithIcon("Add", theme.ContentAddIcon(), func() {
		grid.Add(getNewEntry())
		grid.Refresh()
	})
	addTenBtn := widget.NewButtonWithIcon("Add 10", theme.ContentAddIcon(), func() {
		for i := 0; i < 10; i++ {
			grid.Add(getNewEntry())
		}
		grid.Refresh()
	})
	resetBtn := widget.NewButtonWithIcon("Reset", theme.ContentClearIcon(), func() {
		grid.Objects = []fyne.CanvasObject{getNewFantiaEntry()}
		grid.Refresh()
	})
	return baseGuiElements{
		title:     title,
		grid:      grid,
		delBtn:    delBtn,
		addBtn:    addBtn,
		addTenBtn: addTenBtn,
		resetBtn:  resetBtn,
	}
}
