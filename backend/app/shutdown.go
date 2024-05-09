package app

import (
	"context"
)

func (a *App) Shutdown(ctx context.Context) {
	if a.downloadQueues.Len() > 0 {
		for dlQueue := a.downloadQueues.Front(); dlQueue != nil; dlQueue = dlQueue.Next() {
			dlQueue.Value.(*DownloadQueue).CancelQueue()
		}
	}
}
