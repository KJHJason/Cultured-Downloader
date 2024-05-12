package app

import (
	"sync"

	cdlConst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

var (
	count = 0

	// no. of workers used for each platform
	workerMu           = sync.RWMutex{}
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

// Returns true if the worker for the website is busy, false otherwise
func checkIfWorkerIsBusy(website string) bool {
	var workersUsed int
	var maxWorkers int

	workerMu.RLock()
	defer workerMu.RUnlock()

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
	return workersUsed+1 > maxWorkers
}

func addWorker(website string) {
	workerMu.Lock()
	defer workerMu.Unlock()

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
}
