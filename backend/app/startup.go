package app

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/database"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader-Logic/startup"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/notifier"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) getDownloadDir() (dirPath string, err error, hadToFallback bool) {
	savedDirPath := a.appData.GetString(constants.DOWNLOAD_KEY)
	if savedDirPath != "" && iofuncs.PathExists(savedDirPath) {
		return savedDirPath, nil, false
	}

	desktopDir, err := os.UserHomeDir()
	if err != nil {
		logger.MainLogger.Errorf("Error getting user home directory: %v", err)
		return "", fmt.Errorf("error getting user home directory: %w\nPlease manually set the download directory in the settings", err), false
	}

	desktopDir = filepath.Join(desktopDir, "Desktop", "Cultured Downloader")
	if err := os.MkdirAll(desktopDir, cdlconst.DEFAULT_PERMS); err != nil {
		panic(err)
	}
	a.appData.SetString(constants.DOWNLOAD_KEY, desktopDir)
	return desktopDir, nil, true
}

func (a *App) initAppDb() {
	database.HandleErr = func(err error, logMsg string) {
		_, dialogErr := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error encountered!",
			Message: logMsg + ": " + err.Error(),
		})
		if dialogErr != nil {
			logger.MainLogger.Errorf("Error encountered while trying to show error dialog: %v", dialogErr)
		}
		logger.MainLogger.Fatalf("%s: %s", logMsg, err)
	}

	if err := database.InitAppDb(); err != nil {
		_, dialogErr := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error initialising cache database!",
			Message: err.Error(),
		})
		if dialogErr != nil {
			logger.MainLogger.Errorf("Error encountered while trying to show error dialog for cache db: %v", dialogErr)
		}
		logger.MainLogger.Fatalf("Error initialising cache db: %v", err)
	}
}

func (a *App) checkPrerequisites() {
	panicHandler := func(msg string) {
		_, dialogErr := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Pre-requisites Check Failed!",
			Message: msg,
		})
		if dialogErr != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show pre-requisites check fail msg: %v",
				dialogErr,
			)
		}
		logger.MainLogger.Fatalf("Pre-requisites check failed: %s", msg)
	}
	infoHandler := func(msg string) {
		// Start another goroutine to show the message dialog so that
		// the frontend can start up properly without crashing the program (nil pointer dereference errors)
		// since the backend has yet to initialise as it is waiting for the user to click the dialog.
		go func() {
			_, dialogErr := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
				Type:    runtime.InfoDialog,
				Title:   "Pre-requisites Check Info",
				Message: msg,
			})
			if dialogErr != nil {
				logger.MainLogger.Errorf(
					"Error encountered while trying to show pre-requisites check info msg: %v",
					dialogErr,
				)
			}
			logger.MainLogger.Infof("Pre-requisites check info: %s", msg)
		}()
	}
	startup.CheckPrerequisites(a.ctx, infoHandler, panicHandler)
}

func (a *App) loadAppData() {
	appData, initialLoadErr := appdata.NewAppData()
	if initialLoadErr != nil {
		_, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error loading data from file!",
			Message: "Please refer to the logs or report this issue on GitHub.",
		})
		if err != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v",
				err, initialLoadErr,
			)
		}
		panic("Error loading data from file!")
	}
	a.appData = appData
}

// retrieve user's download directory
func (a *App) getUserSavedDlDirPath() {
	_, err, hadToFallback := a.getDownloadDir()
	if err != nil {
		_, dialogErr := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
			Type:    runtime.ErrorDialog,
			Title:   "Error getting download directory!",
			Message: err.Error(),
		})
		if dialogErr != nil {
			logger.MainLogger.Errorf(
				"Error encountered while trying to show error dialog: %v\nOriginal error: %v",
				dialogErr, err,
			)
		}
	} else if hadToFallback {
		// try retrieving the old download directory path from config.json (*Cultured-Downloader-CLI)
		oldSavedDlDirPath := iofuncs.DOWNLOAD_PATH
		if oldSavedDlDirPath != "" { // if it's not empty, set it as the download directory path
			if setErr := a.appData.SetString(constants.DOWNLOAD_KEY, oldSavedDlDirPath); setErr != nil {
				logger.MainLogger.Errorf("Error setting old download directory path: %v", setErr)
			}
		}
	}
}

func (a *App) initQueueTicker() {
	a.queueTicker = time.NewTicker(1 * time.Second) // check for new queues every few second
	go func() {
		for {
			select {
			case <-a.ctx.Done():
				a.queueTicker.Stop()
				return
			case <-a.queueTicker.C:
				a.startNewQueues()
			}
		}
	}()
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx
	a.initAppDb()
	a.checkPrerequisites()
	a.loadAppData()
	a.getUserSavedDlDirPath()

	a.gdriveClient = a.getGdriveClient()
	a.notifier = notifier.NewNotifier(a.ctx, constants.PROGRAM_NAME)
	a.lang = a.appData.GetStringWithFallback(constants.LANGUAGE_KEY, cdlconst.EN)
	a.initQueueTicker()
}
