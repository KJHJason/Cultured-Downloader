package app

import (
	"context"

	"github.com/KJHJason/Cultured-Downloader-Logic/language"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
)

func (a *App) Shutdown(ctx context.Context) {
	if a.downloadQueues.Len() > 0 {
		for dlQueue := a.downloadQueues.Front(); dlQueue != nil; dlQueue = dlQueue.Next() {
			dlQueue.Value.(*DownloadQueue).CancelQueue()
		}
	}
	a.notifier.Release()
	if a.gdriveClient != nil {
		a.gdriveClient.Release()
	}

	if err := language.CloseDb(); err != nil {
		logger.LogError(err, logger.ERROR)
	}

	if a.mvCacheDbTask != nil {
		if err := a.mvCacheDbTask(); err != nil {
			logger.LogError(err, logger.ERROR)
		}
	}
}
