package app

import (
	"context"
	"sync"
	"time"
)

type ProgressBar struct {
	msg        string
	successMsg string
	errMsg     string

	// For the frontend
	Count          int
	MaxCount       int
	Active         bool
	Finished       bool
	HasError       bool
	Percentage     int
	FolderPath     string
	DateTime       time.Time
	NestedProgBars []NestedProgressBar

	count    int
	maxCount int
	active   bool
	mu       *sync.RWMutex
}

type NestedProgressBar struct {
	Msg 	   string
	SuccessMsg string
	ErrMsg 	   string

	HasError   bool
	Finished   bool
	Percentage int
	DateTime   time.Time
}

type Messages struct {
	Msg        string
	SuccessMsg string
	ErrMsg     string
}

type ProgressDetails struct {
	FolderPath   string
}

func NewProgressBar(ctx context.Context, messages Messages, progressDetails ProgressDetails, maxCount int) *ProgressBar {
	return &ProgressBar{
		msg:        messages.Msg,
		successMsg: messages.SuccessMsg,
		errMsg:     messages.ErrMsg,

		Count:          0,
		MaxCount:       maxCount,
		Active:         false,
		Finished:       false,
		HasError:       false,
		Percentage:     0,
		FolderPath:     progressDetails.FolderPath,
		DateTime:       time.Now().UTC(),
		NestedProgBars: []NestedProgressBar{
			// TODO: REMOVE TEST DATA
			{
				Msg:        "Downloading...",
				SuccessMsg: "Download complete!",
				ErrMsg:     "Download failed!",
			
				HasError:   false,
				Finished:   true,
				Percentage: 100,

				DateTime: time.Now().UTC(),
			},
		},

		count:    0,
		maxCount: maxCount,
		active:   false,
		mu:       &sync.RWMutex{},
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

func (p *ProgressBar) SnapshotTask() {
	p.mu.Lock()
	defer p.mu.Unlock()

	p.NestedProgBars = append(p.NestedProgBars, NestedProgressBar{
		Msg:        p.msg,
		SuccessMsg: p.successMsg,
		ErrMsg:     p.errMsg,
		HasError:   p.HasError,
		Percentage: p.Percentage,
		DateTime:   time.Now().UTC(),
	})

	p.Count = p.count
	p.count = 0
	p.MaxCount = 0
	p.maxCount = 0
	p.active = false
	p.Active = false
	p.Finished = false
	p.HasError = false
	p.Percentage = 0
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
