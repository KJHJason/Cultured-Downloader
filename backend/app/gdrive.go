package app

import (
	"errors"
	"os"

	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

const GDriveMaxDownloaders = 2

func (a *App) GetGdriveClient() *gdrive.GDrive {
	if a.gdriveClient != nil {
		return a.gdriveClient
	}

	gdriveKey := a.appData.GetSecuredString(constants.GDRIVE_API_KEY_KEY)
	if gdriveKey != "" {
		gdriveClient, err := gdrive.GetNewGDrive(
			a.ctx,
			gdriveKey,
			a.appData.GetString(constants.USER_AGENT_KEY),
			nil,
			GDriveMaxDownloaders,
		)
		if err != nil {
			logger.MainLogger.Errorf("Error creating GDrive client: %v", err)
			return nil
		} else {
			a.gdriveClient = gdriveClient
			return a.gdriveClient
		}
	}

	credJson := a.appData.GetSecuredBytes(constants.GDRIVE_SERVICE_ACC_KEY)
	if len(credJson) == 0 {
		logger.MainLogger.Infof("No GDrive API key or service account credentials found.")
		return nil
	}

	gdriveClient, err := gdrive.GetNewGDrive(
		a.ctx,
		"",
		a.appData.GetString(constants.USER_AGENT_KEY),
		credJson,
		GDriveMaxDownloaders,
	)
	if err != nil {
		logger.MainLogger.Errorf("Error creating GDrive client: %v", err)
		return nil
	}

	a.gdriveClient = gdriveClient
	return a.gdriveClient
}

func (a *App) SetGDriveAPIKey(apiKey string) error {
	if apiKey == "" {
		return a.appData.Unset(constants.GDRIVE_API_KEY_KEY)
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, httpfuncs.DEFAULT_USER_AGENT)
	_, err := gdrive.GetNewGDrive(a.ctx, apiKey, userAgent, nil, 1)
	if err != nil {
		return err
	}

	return a.appData.SetSecureString(constants.GDRIVE_API_KEY_KEY, apiKey)
}

func (a *App) GetGDriveAPIKey() string {
	return a.appData.GetSecuredString(constants.GDRIVE_API_KEY_KEY)
}

func (a *App) SelectGDriveServiceAccount() error {
	file, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
		Title: "Select Google Drive service account credentials file",
		Filters: []runtime.FileFilter{
			{
				DisplayName: "JSON Files (*.json)",
				Pattern:     "*.json",
			},
		},
	})

	if err != nil {
		return err
	}
	if file == "" {
		return errors.New("no file selected")
	}

	jsonBytes, err := os.ReadFile(file)
	if err != nil {
		return err
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, httpfuncs.DEFAULT_USER_AGENT)
	_, err = gdrive.GetNewGDrive(a.ctx, "", userAgent, jsonBytes, 1)
	if err != nil {
		return err
	}
	return a.appData.SetSecureBytes(constants.GDRIVE_SERVICE_ACC_KEY, jsonBytes)
}

func (a *App) UnsetGDriveServiceAccount() error {
	return a.appData.Unset(constants.GDRIVE_SERVICE_ACC_KEY)
}

func (a *App) GetGDriveServiceAccount() string {
	jsonBytes := a.appData.GetSecuredBytes(constants.GDRIVE_SERVICE_ACC_KEY)

	return string(jsonBytes)
}
