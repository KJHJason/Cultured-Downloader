package app

import (
	"fmt"
	"strings"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
)

type FrontendDownloadQueue struct {
	Id                int                  `json:"Id"`
	Website           string               `json:"Website"`
	Msg               string               `json:"Msg"`
	SuccessMsg        string               `json:"SuccessMsg"`
	ErrMsg            string               `json:"ErrMsg"`
	ErrSlice          []string             `json:"ErrSlice"`
	HasError          bool                 `json:"HasError"`
	Inputs            []Input              `json:"Inputs"`
	ProgressBar       ProgressBar          `json:"ProgressBar"`
	NestedProgressBar []*NestedProgressBar `json:"NestedProgressBar"`
	Finished          bool                 `json:"Finished"`
}

type FrontendDownloadDetails struct {
	Msg           string  `json:"Msg"`
	SuccessMsg    string  `json:"SuccessMsg"`
	ErrMsg        string  `json:"ErrMsg"`
	Finished      bool    `json:"Finished"`
	HasError      bool    `json:"HasError"`
	FileSize      string  `json:"FileSize"`
	Filename      string  `json:"Filename"`
	DownloadSpeed float64 `json:"DownloadSpeed"`
	DownloadETA   float64 `json:"DownloadETA"`
	Percentage    int     `json:"Percentage"`
}

func formatFrontendDlDetails(dlProgressBars []*progress.DownloadProgressBar) []*FrontendDownloadDetails {
	dlDetailsLen := len(dlProgressBars)
	if dlDetailsLen == 0 {
		return []*FrontendDownloadDetails{}
	}

	lastIdx := dlDetailsLen - 1
	inProgPtr := 0
	donePtr := lastIdx
	dlDetails := make([]*FrontendDownloadDetails, dlDetailsLen)

	// Reverse the order of the download progress bars so that the
	// latest download progress bar that are still downloading is at the top.
	// However, the order of the finished download progress bars is not reversed yet.
	for i := lastIdx; i >= 0; i-- {
		dlProg := dlProgressBars[i]
		dlDetail := &FrontendDownloadDetails{
			Msg:           dlProg.GetMsg(),
			SuccessMsg:    dlProg.GetSuccessMsg(),
			ErrMsg:        dlProg.GetErrMsg(),
			Finished:      dlProg.IsFinished(),
			HasError:      dlProg.HasError(),
			Filename:      dlProg.GetFilename(),
			FileSize:      iofuncs.FormatFileSize(dlProg.GetTotalBytes()),
			DownloadSpeed: dlProg.GetDownloadSpeed(),
			DownloadETA:   dlProg.GetDownloadETA(),
			Percentage:    dlProg.GetPercentage(),
		}
		if dlProg.IsFinished() {
			dlDetails[donePtr] = dlDetail
			donePtr--
		} else {
			dlDetails[inProgPtr] = dlDetail
			inProgPtr++
		}
	}

	// Reverse the sub-slice of already finished download progress bars within
	// dlDetails so that the recently finished download progress bar is at the top
	for i, j := donePtr+1, lastIdx; i <= j; i, j = i+1, j-1 {
		dlDetails[i], dlDetails[j] = dlDetails[j], dlDetails[i]
	}
	return dlDetails
}

func (a *App) GetFrontendDownloadDetails(id int) []*FrontendDownloadDetails {
	_, dlQueue := a.getQueueEl(id)
	if dlQueue == nil {
		return make([]*FrontendDownloadDetails, 0)
	}

	return formatFrontendDlDetails(*dlQueue.dlProgressBars)
}

func (a *App) GetDownloadQueues() []FrontendDownloadQueue {
	var queues []FrontendDownloadQueue
	for e := a.downloadQueues.Back(); e != nil; e = e.Prev() {
		val := e.Value

		msg := val.mainProgressBar.GetBaseMsg()
		if !val.mainProgressBar.GetIsSpinner() && strings.Contains(msg, "%d") {
			msg = fmt.Sprintf(msg, val.mainProgressBar.count)
		}

		errSlice := val.GetErrSlice()
		errStringSlice := make([]string, len(errSlice))
		for idx, err := range errSlice {
			errStringSlice[idx] = err.Error()
		}

		hasError := false
		nestedProgBars := val.mainProgressBar.nestedProgBars
		for _, nestedProgBar := range nestedProgBars {
			if nestedProgBar.HasError {
				hasError = true
				break
			}
		}

		queues = append(queues, FrontendDownloadQueue{
			Id:                val.id,
			Website:           val.website,
			Msg:               msg,
			SuccessMsg:        val.mainProgressBar.GetSuccessMsg(),
			ErrMsg:            val.mainProgressBar.GetErrorMsg(),
			ErrSlice:          errStringSlice,
			HasError:          hasError,
			Inputs:            val.inputs,
			ProgressBar:       *val.mainProgressBar,
			NestedProgressBar: val.mainProgressBar.nestedProgBars,
			Finished:          val.finished,
		})
	}
	return queues
}
