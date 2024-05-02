package app

import (
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

// Note: rmb to edit language.ts as well
const (
	EN = "en"
	JA = "ja"
)

func getLangKey(lang string) string {
	switch lang {
	case JA:
		return JA
	default:
		return EN
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
