package app

import (
	"context"
	"sync"
)

type ProgressBar struct {
	Msg        string
	SuccessMsg string
	ErrMsg     string

	// For the frontend
	Count      int
	MaxCount   int
	Active     bool
	Finished   bool
	Percentage int

	count    int
	maxCount int
	active   bool
	mu       *sync.RWMutex

	Title        string
	MainUrl      string
	ThumbnailUrl string
	FolderPath   string
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

func New(ctx context.Context, messages Messages, progressDetails ProgressDetails, maxCount int) *ProgressBar {
	return &ProgressBar{
		Msg:        messages.Msg,
		SuccessMsg: messages.ErrMsg,
		ErrMsg:     messages.SuccessMsg,

		Count:      0,
		MaxCount:   maxCount,
		Active:     false,
		Finished:   false,
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

func (p *ProgressBar) Stop() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.Active = false
	p.active = false
	p.Finished = true
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
