package app

import (
	"container/list"
	"context"
	"fmt"
	"strings"
	"sync"

	cdlConst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

var (
	count = 0

	// no. of workers used for each platform
	workerMu           = sync.Mutex{}
	fantiaWorking      = 0
	pixivWorking       = 0
	pixivFanboxWorking = 0
	kemonoWorking      = 0
)

func releaseWorker(website string) {
	workerMu.Lock()
	defer workerMu.Unlock()

	switch website {
	case cdlConst.FANTIA:
		fantiaWorking--
	case cdlConst.PIXIV:
		pixivWorking--
	case cdlConst.PIXIV_FANBOX:
		pixivFanboxWorking--
	case cdlConst.KEMONO:
		kemonoWorking--
	}
}

type taskHandlerFunc func() []error

type Input struct {
	//id      string
	//pageNum string
	Input string
	Url   string
}

type DownloadQueue struct {
	id          int
	ctx         context.Context
	cancel      context.CancelFunc
	website     string
	taskHandler taskHandlerFunc // function to handle the API request and downloads
	active      bool
	finished    bool
	mu          sync.Mutex
	errSlice    []error

	// for frontend
	inputs          []Input
	mainProgressBar *ProgressBar
	dlProgressBars  *[]*progress.DownloadProgressBar
}

type FrontendDownloadQueue struct {
	Id                int
	Website           string
	Msg               string
	SuccessMsg        string
	ErrMsg            string
	ErrSlice          []string
	Inputs            []Input
	ProgressBar       *ProgressBar
	NestedProgressBar []NestedProgressBar
	DlProgressBars    []FrontendDownloadDetails
	Finished          bool
}

type FrontendDownloadDetails struct {
	Msg           string
	SuccessMsg    string
	ErrMsg        string
	Finished      bool
	HasError      bool
	Filename      string
	DownloadSpeed float64
	DownloadETA   float64
	Percentage    int
}

// For the frontend
func (a *App) GetDownloadQueues() []FrontendDownloadQueue {
	var queues []FrontendDownloadQueue
	for e := a.downloadQueues.Back(); e != nil; e = e.Prev() {
		val := e.Value.(*DownloadQueue)

		derefDlDetails := *val.dlProgressBars
		dlDetailsLen := len(derefDlDetails)
		dlDetails := make([]FrontendDownloadDetails, dlDetailsLen)
		if dlDetailsLen > 0 {
			idx := 0
			// reverse the order of the download progress bars
			// so that the latest download progress bar is at the top
			for i := dlDetailsLen - 1; i >= 0; i-- {
				dlProg := derefDlDetails[i]
				dlDetails[idx] = FrontendDownloadDetails{
					Msg:           dlProg.GetMsg(),
					SuccessMsg:    dlProg.GetSuccessMsg(),
					ErrMsg:        dlProg.GetErrMsg(),
					Finished:      dlProg.IsFinished(),
					HasError:      dlProg.HasError(),
					Filename:      dlProg.GetFilename(),
					DownloadSpeed: dlProg.GetDownloadSpeed(),
					DownloadETA:   dlProg.GetDownloadETA(),
					Percentage:    dlProg.GetPercentage(),
				}
				idx++
			}
		}

		// since the latest/main progress bar is at the end of the slice
		var nestedProgressBar []NestedProgressBar
		nestedProgBarLen := len(val.mainProgressBar.nestedProgBars)
		if nestedProgBarLen > 0 {
			lastElIdx := nestedProgBarLen - 1
			nestedProgressBar = make([]NestedProgressBar, lastElIdx)
			for idx, val := range val.mainProgressBar.nestedProgBars {
				if idx == lastElIdx {
					break
				}

				nestedProgressBar[idx] = val
				if val.IsSpinner || !strings.Contains(val.Msg, "%d") {
					continue
				}
				nestedProgressBar[idx].Msg = fmt.Sprintf(val.Msg, val.Count)
			}
		}

		msg := val.mainProgressBar.GetBaseMsg()
		if !val.mainProgressBar.GetIsSpinner() && strings.Contains(msg, "%d") {
			msg = fmt.Sprintf(msg, val.mainProgressBar.count)
		}

		errSlice := val.GetErrSlice()
		errStringSlice := make([]string, len(errSlice))
		for idx, err := range errSlice {
			errStringSlice[idx] = err.Error()
		}

		queues = append(queues, FrontendDownloadQueue{
			Id:                val.id,
			Website:           val.website,
			Msg:               msg,
			SuccessMsg:        val.mainProgressBar.GetSuccessMsg(),
			ErrMsg:            val.mainProgressBar.GetErrorMsg(),
			ErrSlice:          errStringSlice,
			Inputs:            val.inputs,
			ProgressBar:       val.mainProgressBar,
			NestedProgressBar: nestedProgressBar,
			DlProgressBars:    dlDetails,
			Finished:          val.finished,
		})
	}
	return queues
}

func (a *App) newDownloadQueue(website string, inputs []Input, mainProgBar *ProgressBar, dlProgressBars *[]*progress.DownloadProgressBar, taskHandler taskHandlerFunc) *DownloadQueue {
	id := count
	ctx, cancel := context.WithCancel(a.ctx)
	count++

	dlQueue := &DownloadQueue{
		id:              id,
		ctx:             ctx,
		cancel:          cancel,
		website:         website,
		taskHandler:     taskHandler,
		active:          false,
		finished:        false,
		mainProgressBar: mainProgBar,
		dlProgressBars:  dlProgressBars,
		mu:              sync.Mutex{},
		inputs:          inputs,
	}
	a.downloadQueues.PushBack(dlQueue)
	return dlQueue
}

func (a *App) getQueueEl(id int) (*list.Element, *DownloadQueue) {
	if a.downloadQueues.Len() == 0 {
		return nil, nil
	}

	// check if id is valid since we are using a counter based id system
	firstEl := a.downloadQueues.Front()
	lastEl := a.downloadQueues.Back()
	firstQueue := firstEl.Value.(*DownloadQueue)
	lastQueue := lastEl.Value.(*DownloadQueue)
	if id < firstQueue.id || id > lastQueue.id {
		return nil, nil
	}

	// Decide which direction is the best to iterate through the list
	// by comparing the distance between the first and last element of the list
	var dlQueue *list.Element
	var direction int
	if id-firstQueue.id < lastQueue.id-id {
		dlQueue = firstEl
		direction = 1
	} else {
		dlQueue = lastEl
		direction = -1
	}

	for dlQueue != nil {
		el := dlQueue.Value.(*DownloadQueue)
		if el.id == id {
			return dlQueue, el
		}

		if direction == 1 {
			dlQueue = dlQueue.Next()
		} else {
			dlQueue = dlQueue.Prev()
		}
	}
	return nil, nil
}

func (a *App) DeleteQueue(id int) {
	listEl, queue := a.getQueueEl(id)
	if queue == nil || listEl == nil {
		return
	}

	queue.CancelQueue()
	a.downloadQueues.Remove(listEl)
}

func (a *App) CancelQueue(id int) {
	_, queue := a.getQueueEl(id)
	if queue == nil {
		return
	}

	queue.CancelQueue()
}

func (a *App) startNewQueues() {
	// loop through the doubly linked list of download queues
	for e := a.downloadQueues.Front(); e != nil; e = e.Next() {
		dq := e.Value.(*DownloadQueue)
		if active, finished := dq.GetStatus(); active || finished {
			continue
		}

		website := dq.website
		var workersUsed int
		var maxWorkers int
		switch website {
		case cdlConst.FANTIA:
			workersUsed = fantiaWorking
			maxWorkers = constants.FANTIA_WORKERS
		case cdlConst.PIXIV:
			workersUsed = pixivWorking
			maxWorkers = constants.PIXIV_WORKERS
		case cdlConst.PIXIV_FANBOX:
			workersUsed = pixivFanboxWorking
			maxWorkers = constants.PIXIV_FANBOX_WORKERS
		case cdlConst.KEMONO:
			workersUsed = kemonoWorking
			maxWorkers = constants.KEMONO_WORKERS
		}

		if workersUsed+1 > maxWorkers {
			continue
		}

		workerMu.Lock()
		switch website {
		case cdlConst.FANTIA:
			fantiaWorking++
		case cdlConst.PIXIV:
			pixivWorking++
		case cdlConst.PIXIV_FANBOX:
			pixivFanboxWorking++
		case cdlConst.KEMONO:
			kemonoWorking++
		}
		workerMu.Unlock()

		go dq.Start()
	}
}

func (q *DownloadQueue) releaseWorker() {
	releaseWorker(q.website)
}

func (q *DownloadQueue) GetStatus() (active bool, finished bool) {
	q.mu.Lock()
	defer q.mu.Unlock()
	return q.active, q.finished
}

func (q *DownloadQueue) setActive(active bool) {
	q.mu.Lock()
	defer q.mu.Unlock()
	q.active = active
}

func (q *DownloadQueue) SetFinished(finished bool) {
	q.mu.Lock()
	defer q.mu.Unlock()
	q.finished = finished
}

func (q *DownloadQueue) UpdateErrSlice(errSlice []error) {
	q.mu.Lock()
	defer q.mu.Unlock()
	q.errSlice = errSlice
}

func (q *DownloadQueue) GetErrSlice() []error {
	q.mu.Lock()
	defer q.mu.Unlock()
	return q.errSlice
}

func (q *DownloadQueue) Start() {
	q.setActive(true)
	go func() {
		errSlice := q.taskHandler()
		q.UpdateErrSlice(errSlice)
		q.releaseWorker()
		q.SetFinished(true)
		q.setActive(false)
	}()
}

func (q *DownloadQueue) CancelQueue() {
	q.mu.Lock()
	defer q.mu.Unlock()
	if q.finished {
		return
	}

	q.cancel()
	q.mainProgressBar.Stop(true)
	q.releaseWorker()
	q.finished = true
}
