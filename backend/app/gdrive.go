package app

import (
	"errors"
	"fmt"
	"os"

	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) GetGdriveClient() *gdrive.GDrive {
	if a.gdriveClient != nil {
		return a.gdriveClient
	}

	gdriveApiKey := a.appData.GetSecuredString(constants.GDRIVE_API_KEY_KEY)
	srvCredJson := a.appData.GetSecuredBytes(constants.GDRIVE_SERVICE_ACC_KEY)
	clientSecretJson := a.appData.GetSecuredBytes(constants.GDRIVE_CLIENT_SECRET_KEY)
	userOauthTokenJson := a.appData.GetSecuredBytes(constants.GDRIVE_OAUTH_TOKEN_KEY)
	if gdriveApiKey == "" && len(srvCredJson) == 0 && len(clientSecretJson) == 0 && len(userOauthTokenJson) == 0 {
		logger.MainLogger.Error("No GDrive API key, service account credentials, or user oauth credentials found")
		return nil
	}

	gdriveClient, err := gdrive.GetNewGDrive(
		a.ctx,
		&gdrive.CredsInputs{
			ApiKey:             gdriveApiKey,
			SrvAccJson:         srvCredJson,
			ClientSecretJson:   clientSecretJson,
			UserOauthTokenJson: userOauthTokenJson,
		},
		gdrive.USE_DEFAULT_MAX_CONCURRENCY,
	)
	if err != nil {
		logger.MainLogger.Errorf("error creating GDrive client: %v", err)
		return nil
	}

	a.gdriveClient = gdriveClient
	return a.gdriveClient
}

func (a *App) SetGDriveAPIKey(apiKey string) error {
	if apiKey == "" {
		a.gdriveClient = nil
		return a.appData.Unset(constants.GDRIVE_API_KEY_KEY)
	}

	credsInput := &gdrive.CredsInputs{
		ApiKey: apiKey,
	}
	gdriveClient, err := gdrive.GetNewGDrive(a.ctx, credsInput, 1)
	if err != nil {
		return err
	}

	a.gdriveClient = gdriveClient
	err = a.appData.SetSecureString(constants.GDRIVE_API_KEY_KEY, apiKey)
	if err != nil {
		return err
	}

	a.appData.Unset(
		constants.GDRIVE_SERVICE_ACC_KEY, 
		constants.GDRIVE_CLIENT_SECRET_KEY, 
		constants.GDRIVE_OAUTH_TOKEN_KEY,
	)
	return nil
}

func (a *App) GetGDriveAPIKey() string {
	return a.appData.GetSecuredString(constants.GDRIVE_API_KEY_KEY)
}

func (a *App) SelectGDriveServiceAccount() error {
	file, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
		Title: "Select Service Account/Client Secret Credentials File",
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

	if gdriveOauthConfig, err = gdrive.ParseConfigFromClientJson(jsonBytes); err == nil {
		gdriveOauthErr = nil
		oauthUrl := gdrive.GetOAuthUrl(gdriveOauthConfig)
		return fmt.Errorf("authentication needed, %s", oauthUrl)
	} 

	credsInput := &gdrive.CredsInputs{
		SrvAccJson: jsonBytes,
	}
	gdriveClient, err := gdrive.GetNewGDrive(a.ctx, credsInput, 1)
	if err != nil {
		return err
	}

	a.gdriveClient = gdriveClient
	err = a.appData.SetSecureBytes(constants.GDRIVE_SERVICE_ACC_KEY, jsonBytes)
	if err != nil {
		return err
	}

	a.appData.Unset(
		constants.GDRIVE_API_KEY_KEY, 
		constants.GDRIVE_CLIENT_SECRET_KEY, 
		constants.GDRIVE_OAUTH_TOKEN_KEY,
	)
	return nil
}

func (a *App) UnsetGDriveJson() error {
	a.gdriveClient = nil
	return a.appData.Unset(
		constants.GDRIVE_CLIENT_SECRET_KEY, 
		constants.GDRIVE_OAUTH_TOKEN_KEY, 
		constants.GDRIVE_API_KEY_KEY,
	)
}

func (a *App) GetGDriveServiceAccount() string {
	jsonBytes := a.appData.GetSecuredBytes(constants.GDRIVE_SERVICE_ACC_KEY)
	if len(jsonBytes) == 0 {
		return ""
	}
	return string(jsonBytes)
}

type GetGDriveOauthResponse struct {
	ClientJson string
	TokenJson  string
}

func (a *App) GetGDriveClientAndOauthToken() GetGDriveOauthResponse {
	clientJsonBytes := a.appData.GetSecuredBytes(constants.GDRIVE_CLIENT_SECRET_KEY)
	if len(clientJsonBytes) == 0 {
		a.appData.Unset(constants.GDRIVE_OAUTH_TOKEN_KEY)
		return GetGDriveOauthResponse{}
	}

	tokenJsonBytes := a.appData.GetSecuredBytes(constants.GDRIVE_OAUTH_TOKEN_KEY)
	if len(tokenJsonBytes) == 0 {
		a.appData.Unset(constants.GDRIVE_CLIENT_SECRET_KEY)
		return GetGDriveOauthResponse{}
	}
	return GetGDriveOauthResponse{
		ClientJson: string(clientJsonBytes),
		TokenJson:  string(tokenJsonBytes),
	}
}
