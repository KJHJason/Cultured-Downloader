package app

import (
	"context"
)

func (app *App) Shutdown(ctx context.Context) {
	if app.downloadQueues.Len() > 0 {
		for dlQueue := app.downloadQueues.Front(); dlQueue != nil; dlQueue = dlQueue.Next() {
			dlQueue.Value.(*DownloadQueue).CancelQueue()
		}
	}
}
