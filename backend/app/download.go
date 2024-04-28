package app

import (
	"container/list"
	"context"
	"sync"

	"time"

	cdlConst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

var (
	count = 0

	// no. of workers used for each platform
	workerMu           = &sync.Mutex{}
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

type dlProgressBars  *[]*DownloadProgressBar
type taskHandlerFunc func(progBars dlProgressBars) error

type DownloadQueue struct {
	id			int
	ctx			context.Context
	cancel		context.CancelFunc
	website     string
	taskHandler taskHandlerFunc // function to handle the API request and downloads
	finished    bool
	mu          sync.Mutex

	mainProgressBar *ProgressBar
	dlProgressBars   dlProgressBars
}

type FrontendDownloadQueue struct {
	Id             int
	Website        string
	Msg            string
	SuccessMsg     string
	ErrMsg         string
	ProgressBar    *ProgressBar
	DlProgressBars []FrontendDownloadDetails
	Finished       bool
}

type FrontendDownloadDetails struct {
	Msg           string
	SuccessMsg    string
	ErrMsg        string
	Filename      string
	DownloadSpeed float64
	DownloadETA   float64
	Percentage    int
}

// For the frontend
func (app *App) GetDownloadQueues() []FrontendDownloadQueue {
	var queues []FrontendDownloadQueue
	for e := app.downloadQueues.Back(); e != nil; e = e.Prev() {
		val := e.Value.(*DownloadQueue)

		dlDetails := make([]FrontendDownloadDetails, len(*val.dlProgressBars))
		for i, dlProg := range *val.dlProgressBars {
			dlDetails[i] = FrontendDownloadDetails{
				Msg:           dlProg.msg,
				SuccessMsg:    dlProg.successMsg,
				ErrMsg:        dlProg.errMsg,
				Filename:      dlProg.filename,
				DownloadSpeed: dlProg.downloadSpeed,
				DownloadETA:   dlProg.downloadETA,
				Percentage:    dlProg.percentage,
			}
		}

		queues = append(queues, FrontendDownloadQueue{
			Id:             val.id,
			Website:        val.website,
			Msg:			val.mainProgressBar.msg,
			SuccessMsg:     val.mainProgressBar.successMsg,
			ErrMsg:         val.mainProgressBar.errMsg,
			ProgressBar:    val.mainProgressBar,
			DlProgressBars: dlDetails,
			Finished:       val.finished,
		})
	}
	return queues
}

func getDemoProgressBar(ctx context.Context) *ProgressBar {
	msgs := Messages{
		Msg:        "Downloading...",
		SuccessMsg: "Download complete!",
		ErrMsg:     "Download failed!",
	}
	progressDetails := ProgressDetails{
		Title:        "Demo Title",
		ThumbnailUrl: "https://pbs.twimg.com/media/GMBZzHdbkAAntIt?format=jpg&name=4096x4096",
		FolderPath:   `C:\Users\Admin\Pictures`,
		MainUrl:      "https://fantia.jp",
	}
	demo := NewProgressBar(ctx, msgs, progressDetails, 10)
	return demo
}

func getDemoDlProgressBar(ctx context.Context) *DownloadProgressBar {
	msgs := Messages{
		Msg:        "Downloading...",
		SuccessMsg: "Download complete!",
		ErrMsg:     "Download failed!",
	}
	return NewDlProgressBar(ctx, msgs)
}

func (app *App) NewDownloadQueue(taskHandler taskHandlerFunc) {
	id := count
	ctx, cancel := context.WithCancel(app.ctx)
	count++

	// TODO: remove demo progress bar and dl progress bars
	dlProgressBars := make([]*DownloadProgressBar, 3)
	for i := 0; i < 3; i++ {
		dlProgressBars[i] = getDemoDlProgressBar(ctx)
	}
	dlQueue := &DownloadQueue{
		id:			     id,
		ctx:             ctx,
		cancel:          cancel,
		website:         cdlConst.FANTIA,
		taskHandler:     taskHandler,
		finished:        false,
		mainProgressBar: getDemoProgressBar(ctx),
		dlProgressBars:  &dlProgressBars,
		mu:              sync.Mutex{},
	}
	app.downloadQueues.PushBack(dlQueue)
}

func (app *App) DeleteQueue(id int) {
	if app.downloadQueues.Len() == 0 {
		return
	}

	// check if id is valid since we are using a counter based id system
	firstEl := app.downloadQueues.Front()
	lastEl := app.downloadQueues.Back()
	firstQueue := firstEl.Value.(*DownloadQueue)
	lastQueue := lastEl.Value.(*DownloadQueue)
	if id < firstQueue.id || id > lastQueue.id {
		return
	}

	// Decide which direction is the best to iterate through the list
	// by comparing the distance between the first and last element of the list
	var dlQueue *list.Element
	var direction int
	if id - firstQueue.id < lastQueue.id - id {
		dlQueue = firstEl
		direction = 1
	} else {
		dlQueue = lastEl
		direction = -1
	}

	for dlQueue != nil {
		el := dlQueue.Value.(*DownloadQueue)
		if el.id == id {
			el.CancelQueue()
			app.downloadQueues.Remove(dlQueue)
			return
		}

		if direction == 1 {
			dlQueue = dlQueue.Next()
		} else {
			dlQueue = dlQueue.Prev()
		}
	}
}

func (app *App) StartNewQueues() {
	workerMu.Lock()
	defer workerMu.Unlock()

	// loop through the doubly linked list of download queues
	for e := app.downloadQueues.Front(); e != nil; e = e.Next() {
		dq := e.Value.(*DownloadQueue)
		if dq.mainProgressBar.active || dq.finished {
			continue
		}

		website := dq.website
		var workersUsed int
		var maxWorkers  int
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

		if workersUsed + 1 > maxWorkers {
			continue
		}

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

		go dq.Start()
	}
}

func (q *DownloadQueue) releaseWorker() {
	releaseWorker(q.website)
}

func (q *DownloadQueue) Start() {
	// TODO: call the taskHandler function in a goroutine and handle releaseWorker and change finished to true 
	// err := q.taskHandler(q.dlProgressBars)

	prog := q.mainProgressBar
	prog.Start()
	go func() {
		for range 10 {
			time.Sleep(5 * time.Second)
			prog.Increment()
		}
		prog.Stop(false)
		q.finished = true
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
