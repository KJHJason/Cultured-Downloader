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
	gdriveOauthMu         sync.RWMutex
	finishedGDriveOauth   bool
	gdriveOauthCancelFunc context.CancelFunc
	gdriveOauthErr        error
	gdriveOauthConfig     *oauth2.Config
	gdriveOauthJsonBytes  []byte
)

func updateGdriveOauthConfig(config *oauth2.Config) {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()
	gdriveOauthConfig = config
}

func getGdriveOauthConfig() *oauth2.Config {
	gdriveOauthMu.RLock()
	defer gdriveOauthMu.RUnlock()
	return gdriveOauthConfig
}

func updateGdriveOauthJsonBytes(jsonBytes []byte) {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()
	gdriveOauthJsonBytes = jsonBytes
}

func getGdriveOauthJsonBytes() []byte {
	gdriveOauthMu.RLock()
	defer gdriveOauthMu.RUnlock()
	return gdriveOauthJsonBytes
}

func updateGdriveOauthErr(err error) {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()
	gdriveOauthErr = err
}

func (a *App) gdriveOauthFlow(ctx context.Context, port uint16) {
	defer func() {
		gdriveOauthMu.Lock()
		gdriveOauthCancelFunc()
		finishedGDriveOauth = true
		gdriveOauthConfig = nil
		gdriveOauthMu.Unlock()
	}()

	var err error
	var gdriveOauthToken *oauth2.Token
	gdriveOauthToken, err = gdrive.StartOAuthListener(ctx, port, getGdriveOauthConfig())
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}

	oauthTokenJson, err := json.MarshalIndent(gdriveOauthToken, "", "    ")
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}

	err = a.appData.SetSecureBytes(constants.GDRIVE_OAUTH_TOKEN_KEY, oauthTokenJson)
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}

	err = a.appData.SetSecureBytes(constants.GDRIVE_CLIENT_SECRET_KEY, getGdriveOauthJsonBytes())
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}

	err = a.appData.Unset(constants.GDRIVE_SERVICE_ACC_KEY, constants.GDRIVE_API_KEY_KEY)
	if err != nil {
		updateGdriveOauthErr(err)
		return
	}
}

func (a *App) StartGDriveOauth() error {
	if getGdriveOauthConfig() == nil {
		return errors.New("no oauth config found")
	}

	var ctx context.Context
	gdriveOauthMu.Lock()
	finishedGDriveOauth = false
	ctx, gdriveOauthCancelFunc = context.WithCancel(a.ctx)
	gdriveOauthMu.Unlock()

	go a.gdriveOauthFlow(ctx, 8080)
	return nil
}

func (a *App) CancelGDriveOauth() {
	gdriveOauthMu.Lock()
	defer gdriveOauthMu.Unlock()

	gdriveOauthCancelFunc()
	gdriveOauthConfig = nil

	a.appData.Unset(
		constants.GDRIVE_OAUTH_TOKEN_KEY,
		constants.GDRIVE_CLIENT_SECRET_KEY,
	)
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
