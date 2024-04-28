package app

import (
	"context"
	"sync"
)

type ProgressBar struct {
	msg        string
	successMsg string
	errMsg     string

	// For the frontend
	Count      int
	MaxCount   int
	Active     bool
	Finished   bool
	HasError   bool
	Percentage int
	Title        string
	MainUrl      string
	ThumbnailUrl string
	FolderPath   string

	count    int
	maxCount int
	active   bool
	mu       *sync.RWMutex
}

type DownloadProgressBar struct {
	msg        string
	successMsg string
	errMsg     string

	percentage int // -1 if unknown, 0-100 otherwise if there's a known ETA

	filename      string
	downloadSpeed float64
	downloadETA   float64
	mu            *sync.RWMutex
}

func (dlP *DownloadProgressBar) UpdateFilename(filename string) {
	dlP.mu.Lock()
	defer dlP.mu.Unlock()

	dlP.filename = filename
}

func (dlP *DownloadProgressBar) UpdateDownloadSpeed(speed float64) {
	dlP.mu.Lock()
	defer dlP.mu.Unlock()

	dlP.downloadSpeed = speed
}

func (dlP *DownloadProgressBar) UpdateDownloadETA(eta float64) {
	dlP.mu.Lock()
	defer dlP.mu.Unlock()

	dlP.downloadETA = eta
}

func NewDlProgressBar(ctx context.Context, messages Messages) *DownloadProgressBar {
	return &DownloadProgressBar{
		msg:        messages.Msg,
		successMsg: messages.SuccessMsg,
		errMsg:     messages.ErrMsg,

		percentage: 0,

		filename:   "",
		downloadSpeed: 0,
		downloadETA:   -1,
		mu:        &sync.RWMutex{},
	}
}

type Messages struct {
	Msg        string
	SuccessMsg string
	ErrMsg     string
}

type ProgressDetails struct {
	Title        string
	MainUrl      string
	ThumbnailUrl string
	FolderPath   string
}

func NewProgressBar(ctx context.Context, messages Messages, progressDetails ProgressDetails, maxCount int) *ProgressBar {
	return &ProgressBar{
		msg:        messages.Msg,
		successMsg: messages.SuccessMsg,
		errMsg:     messages.ErrMsg,

		Count:      0,
		MaxCount:   maxCount,
		Active:     false,
		Finished:   false,
		HasError:   false,
		Percentage: 0,

		count:    0,
		maxCount: maxCount,
		active:   false,
		mu:       &sync.RWMutex{},

		Title:        progressDetails.Title,
		MainUrl:      progressDetails.MainUrl,
		ThumbnailUrl: progressDetails.ThumbnailUrl,
		FolderPath:   progressDetails.FolderPath,
	}
}

func (p *ProgressBar) Start() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.Active = true
	p.active = true
}

func (p *ProgressBar) Stop(hasErr bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.Active = false
	p.active = false
	p.Finished = true
	p.HasError = hasErr
}

func (p *ProgressBar) Increment() {
	p.mu.Lock()
	defer p.mu.Unlock()
	if !p.active {
		return
	}

	p.count++
	p.Count = p.count
	p.Percentage = p.count * 100 / p.maxCount
}
