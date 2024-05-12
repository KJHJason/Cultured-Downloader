package app

import (
	"container/list"
	"context"
	"sync"

	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
)

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
	taskHandler func() []error // function to handle the API request and downloads
	active      bool
	finished    bool
	mu          sync.Mutex
	errSlice    []error

	// for frontend
	inputs          []Input
	mainProgressBar *ProgressBar
	dlProgressBars  *[]*progress.DownloadProgressBar
}

type dlInfo struct {
	website        string
	inputs         []Input
	mainProgBar    *ProgressBar
	dlProgressBars *[]*progress.DownloadProgressBar
	taskHandler    func() []error
}

func (a *App) addNewDownloadQueue(ctx context.Context, cancelFunc context.CancelFunc, dlInfo *dlInfo) *DownloadQueue {
	id := count
	count++

	dlQueue := &DownloadQueue{
		id:              id,
		ctx:             ctx,
		cancel:          cancelFunc,
		website:         dlInfo.website,
		taskHandler:     dlInfo.taskHandler,
		active:          false,
		finished:        false,
		mainProgressBar: dlInfo.mainProgBar,
		dlProgressBars:  dlInfo.dlProgressBars,
		mu:              sync.Mutex{},
		inputs:          dlInfo.inputs,
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
		if checkIfWorkerIsBusy(website) {
			continue
		}

		addWorker(website)
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
