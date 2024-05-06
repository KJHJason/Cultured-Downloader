package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"

	"errors"
	"net/http"
	"os"
	"path/filepath"

	"github.com/KJHJason/Cultured-Downloader-Logic/api"
	cdlconsts "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/parsers"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (app *App) GetPreferences() appdata.Preferences {
	return app.appData.GetPreferences()
}

func (app *App) SetPreferences(platform string, preferences appdata.Preferences) error {
	return app.appData.SetPreferences(platform, preferences)
}

func (a *App) SelectDlDirPath() error {
	dirPath, err := runtime.OpenDirectoryDialog(a.ctx, runtime.OpenDialogOptions{
		Title: "Select download directory",
	})
	if err != nil {
		return err
	}
	if dirPath == "" {
		return errors.New("no directory selected")
	}
	return a.appData.SetString(constants.DOWNLOAD_KEY, dirPath)
}

func (a *App) SetDlDirPath(dirPath string) error {
	if dirPath == "" {
		return errors.New("directory path cannot be empty")
	}

	if !iofuncs.DirPathExists(dirPath) {
		return errors.New("directory does not exist")
	}

	return a.appData.SetString(constants.DOWNLOAD_KEY, dirPath)
}

func (a *App) GetUserAgent() string {
	return a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, cdlconsts.USER_AGENT)
}

func (a *App) SetUserAgent(userAgent string) error {
	if userAgent == "" {
		return errors.New("user agent cannot be empty")
	}

	return a.appData.SetString(constants.USER_AGENT_KEY, userAgent)
}

func verifyWebsiteString(website string) error {
	switch website {
	case cdlconsts.FANTIA, cdlconsts.PIXIV_FANBOX, cdlconsts.PIXIV, cdlconsts.KEMONO:
		return nil
	default:
		return errors.New("invalid website")
	}
}

func getCookieDataKeys(website string) (valKey string, txtKey string, jsonKey string, err error) {
	switch website {
	case cdlconsts.FANTIA:
		return constants.FANTIA_COOKIE_VALUE_KEY, constants.FANTIA_COOKIE_TXT_KEY, constants.FANTIA_COOKIE_JSON_KEY, nil
	case cdlconsts.PIXIV_FANBOX:
		return constants.PIXIV_FANBOX_COOKIE_VALUE_KEY, constants.PIXIV_FANBOX_COOKIE_TXT_KEY, constants.PIXIV_FANBOX_COOKIE_JSON_KEY, nil
	case cdlconsts.PIXIV:
		return constants.PIXIV_COOKIE_VALUE_KEY, constants.PIXIV_COOKIE_JSON_KEY, constants.PIXIV_COOKIE_JSON_KEY, nil
	case cdlconsts.KEMONO:
		return constants.KEMONO_COOKIE_VALUE_KEY, constants.KEMONO_COOKIE_TXT_KEY, constants.KEMONO_COOKIE_JSON_KEY, nil
	default:
		return "", "", "", errors.New("invalid website")
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
	if err != nil {
		return err
	}
	if filePath == "" {
		return errors.New("no file selected")
	}

	data, err := os.ReadFile(filePath)
	if err != nil {
		return err
	}

	dataKey, dataTxtKey, dataJsonKey, err := getCookieDataKeys(website)
	if err != nil {
		return err
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

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, cdlconsts.USER_AGENT)
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

	a.appData.Unset(dataKey)
	if isJson {
		a.appData.Unset(dataTxtKey)
	} else {
		a.appData.Unset(dataJsonKey)
	}
	return nil
}

func (a *App) SetSessionValue(website, session string) error {
	dataKey, dataTxtKey, dataJsonKey, err := getCookieDataKeys(website)
	if err != nil {
		return err
	}

	if session == "" {
		return a.appData.Unset(dataKey)
	}

	if err := verifyWebsiteString(website); err != nil {
		return err
	}

	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, cdlconsts.USER_AGENT)
	if _, err := api.VerifyAndGetCookie(website, session, userAgent); err != nil {
		return err
	}

	if err := a.appData.SetSecureString(dataKey, session); err != nil {
		return err
	}

	a.appData.Unset(dataTxtKey)
	a.appData.Unset(dataJsonKey)
	return nil
}

func (a *App) ResetSession(website string) error {
	dataKey, dataTxtKey, dataJsonKey, err := getCookieDataKeys(website)
	if err != nil {
		return err
	}

	err = a.appData.Unset(dataKey)
	if err != nil {
		return err
	}

	err = a.appData.Unset(dataTxtKey)
	if err != nil {
		return err
	}

	err = a.appData.Unset(dataJsonKey)
	if err != nil {
		return err
	}

	return nil
}

func getSessionValFromCookies(website string, cookies []*http.Cookie) (string, error) {
	baseCookie := api.GetCookie("placeholder-value", website)
	for _, cookie := range cookies {
		if cookie.Name == baseCookie.Name {
			return cookie.Value, nil
		}
	}
	return "", errors.New("cookie not found")
}

func (a *App) GetSessionValue(website string) (string, error) {
	if err := verifyWebsiteString(website); err != nil {
		return "", err
	}

	dataKey, dataTxtKey, dataJsonKey, err := getCookieDataKeys(website)
	if err != nil {
		return "", err
	}

	if val := a.appData.GetSecuredString(dataKey); val != "" {
		return val, nil
	}

	cookieInfoArgs := parsers.NewCookieInfoArgsByWebsite(website)
	if val := a.appData.GetSecuredString(dataTxtKey); val != "" {
		cookies, parseErr := parsers.ParseTxtCookie(val, cookieInfoArgs)
		sessionVal, notFoundErr := getSessionValFromCookies(website, cookies)
		if parseErr != nil || notFoundErr != nil { // if session cookie is invalid, remove the stored session value
			a.appData.Unset(dataTxtKey)
			return "", nil
		}
		return sessionVal, nil
	}

	if val := a.appData.GetSecuredBytes(dataJsonKey); val != nil {
		cookies, parseErr := parsers.ParseJsonCookie(val, cookieInfoArgs)
		sessionVal, notFoundErr := getSessionValFromCookies(website, cookies)
		if parseErr != nil || notFoundErr != nil { // if session cookie is invalid, remove the stored session value
			a.appData.Unset(dataJsonKey)
			return "", nil
		}
		return sessionVal, nil
	}
	return "", nil
}
