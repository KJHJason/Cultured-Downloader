package notifier

import (
	"context"
	_ "embed"
	"os"
	"path/filepath"

	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/gen2brain/beeep"
)

var (
	//go:embed icon.png
	iconImg []byte
)

type Notifier struct {
	cancel   context.CancelFunc
	title    string
	filePath string
}

func NewNotifier(ctx context.Context, title string) Notifier {
	folderDir := os.TempDir()
	tempFile := filepath.Join(folderDir, "cultured-downloader-icon.png")
	os.Mkdir(folderDir, os.ModePerm)

	filePath := ""
	if err := os.WriteFile(tempFile, iconImg, 0644); err == nil {
		filePath = tempFile
	}

	childCtx, cancel := context.WithCancel(ctx)
	go func() {
		for range childCtx.Done() {
			logger.MainLogger.Debug("Removing temp icon file")
			if filePath != "" {
				os.RemoveAll(folderDir)
			}
		}
	}()
	return Notifier{
		cancel:   cancel,
		title:    title,
		filePath: filePath,
	}
}

func (n Notifier) Alert(msg string) {
	beeep.Notify(n.title, msg, n.filePath)
}

func (n Notifier) Release() {
	n.cancel()
}
