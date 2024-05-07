package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func getLangKey(lang string) string {
	switch lang {
	case constants.JA:
		return constants.JA
	default:
		return constants.EN
	}
}

func (a *App) SetLanguage(lang string) string {
	a.lang = getLangKey(lang)
	a.appData.SetString(constants.LANGUAGE_KEY, a.lang)
	return a.lang
}

func (a *App) GetLanguage() string {
	return getLangKey(a.lang)
}
