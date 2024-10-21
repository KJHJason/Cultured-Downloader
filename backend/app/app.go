package app

import (
	"context"
	"time"

	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader-Logic/utils/threadsafe"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/notifier"
)

// App struct
type App struct {
	ctx            context.Context
	appData        *appdata.AppData
	lang           string
	downloadQueues threadsafe.DoublyLinkedList[*DownloadQueue] // list.List // doubly linked list of DownloadQueue
	queueTicker    *time.Ticker
	gdriveClient   *gdrive.GDrive
	notifier       notifier.Notifier
}

func NewApp() *App {
	return &App{}
}
