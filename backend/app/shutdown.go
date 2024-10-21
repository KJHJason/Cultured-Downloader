package app

import (
	"context"

	"github.com/KJHJason/Cultured-Downloader-Logic/database"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
)

func (a *App) Shutdown(ctx context.Context) {
	a.queueTicker.Stop()
	if a.downloadQueues.Len() > 0 {
		for dlQueue := a.downloadQueues.Front(); dlQueue != nil; dlQueue = dlQueue.Next() {
			dlQueue.Value.CancelQueue()
		}
	}
	a.notifier.Release()
	if a.gdriveClient != nil {
		a.gdriveClient.Release()
	}

	if err := database.AppDb.Close(); err != nil {
		logger.LogError(err, logger.ERROR)
	}
}
