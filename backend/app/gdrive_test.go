package app

import (
	"context"
	"os"
	"testing"

	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/progress"
	"github.com/joho/godotenv"
)

func InitTestGDrive(t *testing.T) (*gdrive.GDrive, context.CancelFunc, *configs.Config, *progress.ProgressBarInfo) {
	err := godotenv.Load("../../.env")
	if err != nil {
		t.Fatal("Error loading .env file")
	}

	apiKey := os.Getenv("GDRIVE_API_KEY")
	if apiKey == "" {
		t.Fatal("GDRIVE_API_KEY is empty")
	}

	ctx, cancel := context.WithCancel(context.Background())
	gdriveClient, err := gdrive.GetNewGDrive(ctx, apiKey, httpfuncs.DEFAULT_USER_AGENT, nil, 2)
	if err != nil {
		t.Fatalf("Error creating GDrive client: %v", err)
	}

	config := &configs.Config{
		DownloadPath:   "./",
		FfmpegPath:     "",
		OverwriteFiles: false,
		LogUrls: 	    false,
		UserAgent:      httpfuncs.DEFAULT_USER_AGENT,
	}
	prog := &progress.ProgressBarInfo{
		MainProgressBar: NewProgressBar(ctx),
		DownloadProgressBars: nil,
	}
	return gdriveClient, cancel, config, prog
}

func TestGDriveFileDownload(t *testing.T) {
	gdriveClient, cancel, config, progInfo := InitTestGDrive(t)
	defer cancel()

	url := "https://drive.google.com/file/d/1xnDYjiH866KOlAGnZ3mDJuqpPq3mRF1F/view?usp=sharing"
	dirPath := "test-dir"
	defer os.RemoveAll(dirPath)

	toDlInfo := &httpfuncs.ToDownload{
		Url:      url,
		FilePath: dirPath,
	}

	errSlice := gdriveClient.DownloadGdriveUrls(
		[]*httpfuncs.ToDownload{toDlInfo},
		config,
		progInfo,
	)
	if len(errSlice) > 0 {
		t.Logf("Errors downloading file in %s", dirPath)
		for _, err := range errSlice {
			t.Error(err)
		}
		t.Fail()
	} else {
		t.Logf("Downloaded file in %s", dirPath)
	}
}

func TestGDriveFolderDownload(t *testing.T) {
	gdriveClient, cancel, config, progInfo := InitTestGDrive(t)
	defer cancel()

	url := "https://drive.google.com/drive/folders/1zhP5ZzpxFX654-KSNP8d4nA2-zqLa-qq?usp=sharing"
	dirPath := "test-dir"
	defer os.RemoveAll(dirPath)

	toDlInfo := &httpfuncs.ToDownload{
		Url:      url,
		FilePath: dirPath,
	}

	errSlice := gdriveClient.DownloadGdriveUrls(
		[]*httpfuncs.ToDownload{toDlInfo},
		config,
		progInfo,
	)
	if len(errSlice) > 0 {
		t.Logf("Errors downloading folder at %s", dirPath)
		for _, err := range errSlice {
			t.Error(err)
		}
		t.Fail()
	} else {
		t.Logf("Downloaded folder at %s", dirPath)
	}
}
