package app

import (
	"context"
	"fmt"
	"strings"
	"sync"
	"time"

	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
)

type ProgressBar struct {
	msg        string
	successMsg string
	errMsg     string

	// For the frontend
	IsSpinner      bool      `json:"IsSpinner"`
	Count          int       `json:"Count"`
	MaxCount       int       `json:"MaxCount"`
	Active         bool      `json:"Active"`
	Finished       bool      `json:"Finished"`
	HasError       bool      `json:"HasError"`
	Percentage     int       `json:"Percentage"`
	FolderPath     string    `json:"FolderPath"`
	DateTime       time.Time `json:"DateTime"`
	nestedProgBars []*NestedProgressBar

	// download progress bars for more detailed information
	DownloadProgressBars []*progress.DownloadProgressBar

	count     int
	maxCount  int
	active    bool
	isSpinner bool
	mu        *sync.RWMutex
}

type NestedProgressBar struct {
	Msg        string `json:"Msg"`
	SuccessMsg string `json:"SuccessMsg"`
	ErrMsg     string `json:"ErrMsg"`

	IsSpinner bool `json:"IsSpinner"`

	Count      int       `json:"Count"`
	HasError   bool      `json:"HasError"`
	Percentage int       `json:"Percentage"`
	DateTime   time.Time `json:"DateTime"`
}

type Messages struct {
	Msg        string
	SuccessMsg string
	ErrMsg     string
}

func NewProgressBar(ctx context.Context) *ProgressBar {
	return &ProgressBar{
		Count:          0,
		Active:         false,
		Finished:       false,
		HasError:       false,
		Percentage:     0,
		DateTime:       time.Now().UTC(),
		nestedProgBars: []*NestedProgressBar{},

		count:     0,
		active:    false,
		isSpinner: false,
		mu:        &sync.RWMutex{},
	}
}

func (p *ProgressBar) Add(i int) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if !p.active || p.isSpinner {
		return
	}

	p.count += i
	p.Count = p.count
	p.Percentage = p.count * 100 / p.maxCount
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

func (p *ProgressBar) SetToSpinner() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.IsSpinner = true
	p.isSpinner = true
}

func (p *ProgressBar) SetToProgressBar() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.IsSpinner = false
	p.isSpinner = false
}

func (p *ProgressBar) GetIsSpinner() bool {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return p.isSpinner
}

func (p *ProgressBar) GetIsProgBar() bool {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return !p.isSpinner
}

func (p *ProgressBar) StopInterrupt(errMsg string) {
	p.UpdateErrorMsg(errMsg)
	p.Stop(true)
}

func (p *ProgressBar) UpdateBaseMsg(msg string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.msg = msg
}

func (p *ProgressBar) GetBaseMsg() string {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return p.msg
}

func (p *ProgressBar) UpdateMax(max int) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.maxCount = max
	p.MaxCount = max
}

func (p *ProgressBar) Increment() {
	p.Add(1)
}

func (p *ProgressBar) UpdateSuccessMsg(successMsg string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.successMsg = successMsg
}

func (p *ProgressBar) GetSuccessMsg() string {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return p.successMsg
}

func (p *ProgressBar) UpdateErrorMsg(errMsg string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.errMsg = errMsg
}

func (p *ProgressBar) GetErrorMsg() string {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return p.errMsg
}

func (p *ProgressBar) SnapshotTask() {
	p.mu.Lock()
	defer p.mu.Unlock()

	msg := p.msg
	if strings.Contains(msg, "%d") {
		msg = fmt.Sprintf(msg, p.count)
	}

	p.nestedProgBars = append(p.nestedProgBars, &NestedProgressBar{
		Msg:        msg,
		SuccessMsg: p.successMsg,
		ErrMsg:     p.errMsg,
		IsSpinner:  p.IsSpinner,
		Count:      p.Count,
		HasError:   p.HasError,
		Percentage: p.Percentage,
		DateTime:   time.Now().UTC(),
	})

	p.Count = 0
	p.count = 0
	p.MaxCount = 0
	p.maxCount = 0
	p.active = false
	p.Active = false
	p.isSpinner = false
	p.Finished = false
	p.HasError = false
	p.Percentage = 0
}

func (p *ProgressBar) MakeLatestSnapshotMain() {
	p.mu.Lock()
	defer p.mu.Unlock()
	if len(p.nestedProgBars) == 0 {
		return
	}

	latest := p.nestedProgBars[len(p.nestedProgBars)-1]
	p.msg = latest.Msg
	p.successMsg = latest.SuccessMsg
	p.errMsg = latest.ErrMsg
	p.IsSpinner = latest.IsSpinner
	p.Count = latest.Count
	p.HasError = latest.HasError
	p.Percentage = latest.Percentage
	p.DateTime = latest.DateTime
}

func (p *ProgressBar) UpdateFolderPath(folderPath string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.FolderPath = folderPath
}
