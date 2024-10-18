package app

import (
	"context"
	"sync"

	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader-Logic/utils/threadsafe"
)

type Input struct {
	Input string `json:"Input"`
	Url   string `json:"Url"`
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
	a.downloadQueues.Append(dlQueue)
	return dlQueue
}

func (a *App) getTraversalDirection(id int) (direction threadsafe.TraversalDirection, ok bool) {
	queueLen := a.downloadQueues.Len()
	if queueLen == 0 {
		return -1, false
	}
	onlyOneQueue := queueLen == 1

	// Retrieve the first and last queue
	firstEl := a.downloadQueues.Front()
	var lastEl *threadsafe.DoublyLinkedListNode[*DownloadQueue]
	if onlyOneQueue {
		lastEl = firstEl // since the head and tail will point to the same node
	} else {
		lastEl = a.downloadQueues.Back()
	}

	firstQueue, lastQueue := firstEl.Value, lastEl.Value
	// check if id is valid since we are using a counter based id system
	if id < firstQueue.id || id > lastQueue.id {
		return -1, false
	}

	if onlyOneQueue { // since the head and tail points to the same node...
		// Just traverse from head.
		return threadsafe.TraverseFromHead, true
	}

	// Decide which direction is the best to iterate through the list
	// by comparing the distance between the first and last element of the list
	if id-firstQueue.id < lastQueue.id-id {
		// dlQueue = firstEl
		return threadsafe.TraverseFromHead, true
	} else {
		// dlQueue = lastEl
		return threadsafe.TraverseFromTail, true
	}
}

func (a *App) getQueueEl(id int) (*threadsafe.DoublyLinkedListNode[*DownloadQueue], *DownloadQueue) {
	traversalDirection, ok := a.getTraversalDirection(id)
	if !ok {
		return nil, nil
	}
	traverseFromHead := traversalDirection == threadsafe.TraverseFromHead

	var dlQueue *threadsafe.DoublyLinkedListNode[*DownloadQueue]
	if traverseFromHead {
		dlQueue = a.downloadQueues.Front()
	} else {
		dlQueue = a.downloadQueues.Back()
	}

	for dlQueue != nil {
		el := dlQueue.Value
		if el.id == id {
			return dlQueue, el
		}

		if traverseFromHead {
			dlQueue = dlQueue.Next()
		} else {
			dlQueue = dlQueue.Prev()
		}
	}
	return nil, nil
}

func (a *App) DeleteQueue(id int) {
	traversalDirection, ok := a.getTraversalDirection(id)
	if !ok {
		return
	}

	a.downloadQueues.RemoveViaFn(traversalDirection, func(curValue *DownloadQueue) bool {
		if curValue.id != id {
			return false
		}
		curValue.CancelQueue()
		return true
	})
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
		dq := e.Value
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
