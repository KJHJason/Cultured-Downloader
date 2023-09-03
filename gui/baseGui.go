package gui

import (
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

type baseGuiElements struct {
	title     *canvas.Text
	grid      *fyne.Container
	delBtn    *widget.Button
	addBtn    *widget.Button
	addTenBtn *widget.Button
	resetBtn  *widget.Button
}

func (b baseGuiElements) Title() *canvas.Text {
	return b.title
}

func (b baseGuiElements) Grid() *fyne.Container {
	return b.grid
}

func (b baseGuiElements) DelBtn() *widget.Button {
	return b.delBtn
}

func (b baseGuiElements) AddBtn() *widget.Button {
	return b.addBtn
}

func (b baseGuiElements) AddTenBtn() *widget.Button {
	return b.addTenBtn
}

func (b baseGuiElements) ResetBtn() *widget.Button {
	return b.resetBtn
}

const (
	H1 = 24
	H2 = 18
)

func GetBaseGuiElements(titleStr string, getNewEntry func() *widget.Entry) baseGuiElements {
	title := canvas.NewText(titleStr, color.White)
	title.TextStyle = fyne.TextStyle{
		Bold: true,
	}
	title.Alignment = fyne.TextAlignCenter
	title.TextSize = H1

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
		grid.Objects = []fyne.CanvasObject{getNewEntry()}
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
