package app

import (
	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/language"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func getLangKey(lang string) string {
	switch lang {
	case cdlconst.JP:
		return cdlconst.JP
	default:
		return cdlconst.EN
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

func (a *App) Translate(textKey string, lang string) string {
	if lang == "" {
		lang = a.lang
	}
	return language.Translate(textKey, getLangKey(lang))
}
