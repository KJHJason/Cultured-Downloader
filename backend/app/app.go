package app

import (
	"container/list"
	"context"

	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/notifier"
)

// App struct
type App struct {
	ctx            context.Context
	appData        *appdata.AppData
	lang           string
	downloadQueues list.List // doubly linked list of DownloadQueue
	gdriveClient   *gdrive.GDrive
	notifier       notifier.Notifier
	mvCacheDbTask  func() error // to be executed on shutdown
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}
