package app

import (
	"context"
	"container/list"

	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
)

var count = 0

type DownloadQueue struct {
	id			int
	ctx			context.Context
	cancel		context.CancelFunc
	toDownload	[]*httpfuncs.RequestArgs
}

func (app *App) NewDownloadQueue(ctx context.Context, reqs []*httpfuncs.RequestArgs) {
	id := count
	ctx, cancel := context.WithCancel(ctx)
	for _, req := range reqs {
		req.Context = ctx
	}

	count++
	dlQueue := &DownloadQueue{
		id:			id,
		ctx:        ctx,
		toDownload: reqs,
		cancel:     cancel,
	}
	app.downloadQueues.PushBack(dlQueue)
}

func (q *DownloadQueue) CancelQueue() {
	q.cancel()
}

func (a *App) CancelQueue(id int) {
	if a.downloadQueues.Len() == 0 {
		return
	}

	// check if id is valid since we are using a counter based id system
	firstEl := a.downloadQueues.Front()
	lastEl := a.downloadQueues.Back()
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
			a.downloadQueues.Remove(dlQueue)
			return
		}

		if direction == 1 {
			dlQueue = dlQueue.Next()
		} else {
			dlQueue = dlQueue.Prev()
		}
	}
}
