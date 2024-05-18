package app

import (
	"context"

	"github.com/KJHJason/Cultured-Downloader-Logic/cache"
	"github.com/KJHJason/Cultured-Downloader-Logic/language"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) Shutdown(ctx context.Context) {
	a.queueTicker.Stop()
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

	savedCacheLocation := a.appData.GetStringWithFallback(constants.CACHE_DB_PATH_KEY, cache.DEFAULT_PATH)
	if a.mvCacheDbTask != nil && savedCacheLocation != cache.DEFAULT_PATH {
		if err := a.mvCacheDbTask(); err != nil {
			logger.LogError(err, logger.ERROR)
			resetCacheLocErr := a.appData.SetString(constants.CACHE_DB_PATH_KEY, cache.DEFAULT_PATH)
			if resetCacheLocErr != nil {
				logger.LogError(resetCacheLocErr, logger.ERROR)
			}
		}
	}
}
