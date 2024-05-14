package app

import (
	"context"
	"encoding/json"
	"errors"
	"sync"

	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"golang.org/x/oauth2"
)

var (
	gdriveOauthMu         sync.Mutex
	finishedGDriveOauth   bool
	gdriveOauthCancelFunc context.CancelFunc
	gdriveOauthErr        error
	gdriveOauthConfig     *oauth2.Config
)

func updateGdriveOauthErr(err error) {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()
	gdriveOauthErr = err
}

func (a *App) gdriveOauthFlow(ctx context.Context) {
	defer func () {
		gdriveOauthMu.Lock()
		gdriveOauthCancelFunc()
		finishedGDriveOauth = true
		gdriveOauthConfig = nil
		gdriveOauthMu.Unlock()
	}()

	var err error
	var gdriveOauthToken *oauth2.Token
	gdriveOauthToken, err = gdrive.StartOAuthListener(ctx, gdriveOauthConfig)
	if err != nil {
		updateGdriveOauthErr(err)
		return 
	}

	oauthTokenJson, err := json.MarshalIndent(gdriveOauthToken, "", "    ")
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}

	clientSecretJson, err := json.MarshalIndent(gdriveOauthConfig, "", "    ")
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}

	err = a.appData.SetSecureBytes(constants.GDRIVE_OAUTH_TOKEN_KEY, oauthTokenJson)
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}
	
	err = a.appData.SetSecureBytes(constants.GDRIVE_CLIENT_SECRET_KEY, clientSecretJson)
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}
}

func (a *App) StartGDriveOauth() error {
	if gdriveOauthConfig == nil {
		return errors.New("no oauth config found")
	}

	var ctx context.Context
	gdriveOauthMu.Lock()
	ctx, gdriveOauthCancelFunc = context.WithCancel(a.ctx)
	gdriveOauthMu.Unlock()

	go a.gdriveOauthFlow(ctx)
	return nil
} 

func (a *App) CancelGDriveOauth() {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()

	gdriveOauthCancelFunc()
	gdriveOauthConfig = nil

	a.appData.Unset(constants.GDRIVE_OAUTH_TOKEN_KEY)
	a.appData.Unset(constants.GDRIVE_CLIENT_SECRET_KEY)
}

func (a *App) ValidateGDriveOauth() error {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()

	if !finishedGDriveOauth {
		return errors.New("oauth not finished")
	}

	if gdriveOauthErr != nil {
		return gdriveOauthErr
	}
	return nil
}
