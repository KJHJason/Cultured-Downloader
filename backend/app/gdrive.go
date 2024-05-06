package app

import (
	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
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
