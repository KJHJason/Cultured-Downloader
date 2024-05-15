package app

import (
	"fmt"
	"strings"

	cdlConst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

type FrontendDownloadQueue struct {
	Id                int
	Website           string
	Msg               string
	SuccessMsg        string
	ErrMsg            string
	ErrSlice          []string
	HasError          bool
	Inputs            []Input
	ProgressBar       *ProgressBar
	NestedProgressBar []*NestedProgressBar
	DlProgressBars    []*FrontendDownloadDetails
	Finished          bool
}

type FrontendDownloadDetails struct {
	Msg           string
	SuccessMsg    string
	ErrMsg        string
	Finished      bool
	HasError      bool
	FileSize      string
	Filename      string
	DownloadSpeed float64
	DownloadETA   float64
	Percentage    int
}

func formatFileSize(fileSize int64) string {
	if fileSize == -1 {
		return "Unknown"
	} else if fileSize > constants.FILESIZE_TB {
		return fmt.Sprintf("~%d TB", fileSize>>40)
	} else if fileSize > constants.FILESIZE_GB {
		return fmt.Sprintf("~%d GB", fileSize>>30)
	} else if fileSize > constants.FILESIZE_MB {
		return fmt.Sprintf("~%d MB", fileSize>>20)
	} else if fileSize > constants.FILESIZE_KB {
		return fmt.Sprintf("~%d KB", fileSize>>10)
	}
	return fmt.Sprintf("~%d B", fileSize)
}

func formatFrontendDlDetails(dlProgressBars []*progress.DownloadProgressBar) []*FrontendDownloadDetails {
	dlDetailsLen := len(dlProgressBars)
	if dlDetailsLen == 0 {
		return []*FrontendDownloadDetails{}
	}

	idx := 0
	dlDetails := make([]*FrontendDownloadDetails, dlDetailsLen)

	// reverse the order of the download progress bars
	// so that the latest download progress bar is at the top
	for i := dlDetailsLen - 1; i >= 0; i-- {
		dlProg := dlProgressBars[i]

		dlDetails[idx] = &FrontendDownloadDetails{
			Msg:           dlProg.GetMsg(),
			SuccessMsg:    dlProg.GetSuccessMsg(),
			ErrMsg:        dlProg.GetErrMsg(),
			Finished:      dlProg.IsFinished(),
			HasError:      dlProg.HasError(),
			Filename:      dlProg.GetFilename(),
			FileSize:      formatFileSize(dlProg.GetTotalBytes()),
			DownloadSpeed: dlProg.GetDownloadSpeed(),
			DownloadETA:   dlProg.GetDownloadETA(),
			Percentage:    dlProg.GetPercentage(),
		}
		idx++
	}
	return dlDetails
}

func checkNestedProgBarForErrors(dlQueue *DownloadQueue) bool {
	hasError := false
	nestedProgBars := dlQueue.mainProgressBar.nestedProgBars

	lastElIdx := len(nestedProgBars) - 1
	for idx, nestedProgBar := range nestedProgBars {
		if !hasError && nestedProgBar.HasError {
			hasError = true
			if dlQueue.website != constants.FANTIA {
				// for those that doesn't have a captcha solver
				continue
			}

			if nestedProgBar.ErrMsg != cdlConst.ERR_RECAPTCHA_STR {
				continue
			}

			// check the next element if it has an error as the captcha error can be ignored if the next element has no error
			if idx+1 <= lastElIdx && nestedProgBars[idx+1].HasError {
				hasError = true
			}
		}
	}
	return hasError
}

func (a *App) GetDownloadQueues() []FrontendDownloadQueue {
	var queues []FrontendDownloadQueue
	for e := a.downloadQueues.Back(); e != nil; e = e.Prev() {
		val := e.Value.(*DownloadQueue)

		msg := val.mainProgressBar.GetBaseMsg()
		if !val.mainProgressBar.GetIsSpinner() && strings.Contains(msg, "%d") {
			msg = fmt.Sprintf(msg, val.mainProgressBar.count)
		}

		errSlice := val.GetErrSlice()
		errStringSlice := make([]string, len(errSlice))
		for idx, err := range errSlice {
			errStringSlice[idx] = err.Error()
		}

		queues = append(queues, FrontendDownloadQueue{
			Id:                val.id,
			Website:           val.website,
			Msg:               msg,
			SuccessMsg:        val.mainProgressBar.GetSuccessMsg(),
			ErrMsg:            val.mainProgressBar.GetErrorMsg(),
			ErrSlice:          errStringSlice,
			HasError:          checkNestedProgBarForErrors(val),
			Inputs:            val.inputs,
			ProgressBar:       val.mainProgressBar,
			NestedProgressBar: val.mainProgressBar.nestedProgBars,
			DlProgressBars:    formatFrontendDlDetails(*val.dlProgressBars),
			Finished:          val.finished,
		})
	}
	return queues
}
