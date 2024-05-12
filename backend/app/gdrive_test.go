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

func getConfigAndProgInfo(ctx context.Context) (*configs.Config, *progress.ProgressBarInfo) {
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
	return config, prog
}

func initTestGDrive(t *testing.T) (*gdrive.GDrive, context.CancelFunc, *configs.Config, *progress.ProgressBarInfo) {
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
	gdriveClient, cancel, config, progInfo := initTestGDrive(t)
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
	gdriveClient, cancel, config, progInfo := initTestGDrive(t)
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

func TestGDriveServiceAcc(t *testing.T) {
	gdriveJsonPath := "../../test-gdrive-service-acc.json"
	if _, err := os.Stat(gdriveJsonPath); os.IsNotExist(err) {
		t.Fatalf("gdrive-service-acc.json not found at %s", gdriveJsonPath)
	} 

	credJson, err := os.ReadFile(gdriveJsonPath)
	if err != nil {
		t.Fatalf("Error reading gdrive-service-acc.json: %v", err)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	gdriveClient, err := gdrive.GetNewGDrive(ctx, "", httpfuncs.DEFAULT_USER_AGENT, credJson, 2)
	if err != nil {
		t.Fatalf("Error setting service account: %v", err)
	}

	url := "https://drive.google.com/file/d/1ZjhOns-rZeSWS0EQPMziqsZINxWge468/view?usp=sharing"
	dirPath := "test-dir"
	defer os.RemoveAll(dirPath)

	toDlInfo := &httpfuncs.ToDownload{
		Url:      url,
		FilePath: dirPath,
	}

	config, progInfo := getConfigAndProgInfo(ctx)
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
