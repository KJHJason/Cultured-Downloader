package progress

import (
	"sync"
	"errors"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

type ProgressBar struct {
	mu       *sync.Mutex

	win      fyne.Window
	bar      *widget.ProgressBar
	label    *canvas.Text

	errMsg   error
}

func NewProgressBar(label, errMsg string, win fyne.Window) (*fyne.Container, *ProgressBar) {
	progressLabel :=  canvas.NewText(label, color.White)
	progressBar := widget.NewProgressBar()
	progressLabel.Hide()
	progressBar.Hide()

	con := container.New(
		layout.NewVBoxLayout(),
		container.NewPadded(progressLabel),
		container.NewPadded(progressBar),
	)

	return con, &ProgressBar{
		mu:       &sync.Mutex{},
		win:      win,
		bar:      progressBar,
		label:    progressLabel,
		errMsg:   errors.New(errMsg),
	}
}

func (p *ProgressBar) SetMax(max float64) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.bar.Max = max
}

func (p *ProgressBar) Start() {
	p.bar.Show()
	p.label.Show()
}

func (p *ProgressBar) Stop(hasErr bool) {
	p.bar.Hide()
	p.label.Hide()
	p.bar.SetValue(0)
	p.bar.Refresh()

	if hasErr {
		dialog.ShowError(p.errMsg, p.win)
	}
}

func (p *ProgressBar) SetProgress(val float64) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.bar.SetValue(val)
}

func (p *ProgressBar) Increment() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.bar.SetValue(p.bar.Value + 1)
	p.bar.Refresh()
}
