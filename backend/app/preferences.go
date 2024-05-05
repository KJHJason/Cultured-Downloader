package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"

	"errors"
	"net/http"
	"os"
	"path/filepath"

	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/parsers"
	"github.com/KJHJason/Cultured-Downloader-Logic/api"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (app *App) GetPreferences() appdata.Preferences {
	return app.appData.GetPreferences()
}

func (app *App) SetPreferences(platform string, preferences appdata.Preferences) error {
	return app.appData.SetPreferences(platform, preferences)
}

func verifyWebsiteString(website string) error {
	switch website {
	case cdlconsts.FANTIA, cdlconsts.PIXIV_FANBOX, cdlconsts.PIXIV, cdlconsts.KEMONO:
		return nil
	default:
		return errors.New("invalid website")
	}
}

func (a *App) UploadCookieFile(website string) error {
	if err := verifyWebsiteString(website); err != nil {
		return err
	}

	filePath, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
		Title: "Select generated Netscape/Mozilla cookie file for " + api.GetReadableSiteStr(website),
		Filters: []runtime.FileFilter{
			{
				DisplayName: "Text Files (*.txt,*.json)",
				Pattern:     "*.txt;*.json",
			},
		},
	})
	if filePath == "" {
		return nil
	}
	if err != nil {
		return err
	}

	data, err := os.ReadFile(filePath)
	if err != nil {
		return err
	}

	var dataTxtKey, dataJsonKey string
	switch website {
	case cdlconsts.FANTIA:
		dataTxtKey = constants.FantiaCookieTxtKey
		dataJsonKey = constants.FantiaCookieJsonKey
	case cdlconsts.PIXIV_FANBOX:
		dataTxtKey = constants.PixivFanboxCookieTxtKey
		dataJsonKey = constants.PixivFanboxCookieJsonKey
	case cdlconsts.PIXIV:
		dataTxtKey = constants.PixivCookieTxtKey
		dataJsonKey = constants.PixivCookieJsonKey
	case cdlconsts.KEMONO:
		dataTxtKey = constants.KemonoCookieTxtKey
		dataJsonKey = constants.KemonoCookieJsonKey
	default:
		return errors.New("invalid website")
	}

	var cookies []*http.Cookie
	isJson := filepath.Ext(filePath) == ".json"
	cookieInfoArgs := parsers.NewCookieInfoArgsByWebsite(website)
	if isJson {
		cookies, err = parsers.ParseJsonCookie(data, cookieInfoArgs)
	} else {
		decodedData := string(data)
		cookies, err = parsers.ParseTxtCookie(decodedData, cookieInfoArgs)
	}
	if err != nil {
		return err
	}

	userAgent := a.appData.GetStringWithFallback(constants.UserAgentKey, cdlconsts.USER_AGENT)
	err = api.VerifyCookies(website, userAgent, cookies)
	if err != nil {
		return err
	}

	if isJson {
		err = a.appData.SetSecureBytes(dataJsonKey, data)
	} else {
		err = a.appData.SetSecureString(dataTxtKey, string(data))
	}
	if err != nil {
		return err
	}

	return nil
}

func (a *App) SetSessionValue(website, session string) error {
	if session == "" {
		return nil
	}

	if err := verifyWebsiteString(website); err != nil {
		return err
	}

	userAgent := a.appData.GetStringWithFallback(constants.UserAgentKey, cdlconsts.USER_AGENT)
	if _, err := api.VerifyAndGetCookie(website, session, userAgent); err != nil {
		return err
	}

	var dataKey string
	switch website {
	case cdlconsts.FANTIA:
		dataKey = constants.FantiaCookieValueKey
	case cdlconsts.PIXIV_FANBOX:
		dataKey = constants.PixivFanboxCookieValueKey
	case cdlconsts.PIXIV:
		dataKey = constants.PixivCookieValueKey
	case cdlconsts.KEMONO:
		dataKey = constants.KemonoCookieValueKey
	default:
		return errors.New("invalid website")
	}

	if err := a.appData.SetSecureString(dataKey, session); err != nil {
		return err
	}
	return nil
}
