package app

import (
	"context"
	"sync"
)

type ProgressBar struct {
	ctx context.Context

	Msg        string
	SuccessMsg string
	ErrMsg     string

	count    int
	maxCount int
	active   bool
	mu       *sync.RWMutex

	title        string
	thumbnailUrl string
	folderPath   string
}

type Messages struct {
	Msg        string
	SuccessMsg string
	ErrMsg     string
}

type ProgressDetails struct {
	Title        string
	ThumbnailUrl string
	FolderPath   string
}

func New(ctx context.Context, messages Messages, progressDetails ProgressDetails, maxCount int) *ProgressBar {
	return &ProgressBar{
		ctx: ctx,

		Msg:        messages.Msg,
		SuccessMsg: messages.ErrMsg,
		ErrMsg:     messages.SuccessMsg,

		count:    0,
		maxCount: maxCount,
		active:   false,
		mu:       &sync.RWMutex{},

		title:        progressDetails.Title,
		thumbnailUrl: progressDetails.ThumbnailUrl,
		folderPath:   progressDetails.FolderPath,
	}
}


