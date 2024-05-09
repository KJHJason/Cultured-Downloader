package app

import (
	"errors"
	"strings"

	pixivmobile "github.com/KJHJason/Cultured-Downloader-Logic/api/pixiv/mobile"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func validatePixivTag(tag *string) (valid bool, pageNum string) {
	// split by ";" and get the last element,
	// for the other elements, just join them back with ";"
	splitTag := strings.Split(*tag, ";")
	if len(splitTag) == 0 {
		return len(*tag) > 0, ""
	}

	pageNum = splitTag[len(splitTag)-1]
	*tag = strings.Join(splitTag[:len(splitTag)-1], ";")
	if len(*tag) == 0 {
		return false, ""
	}

	return true, pageNum
}

var codeVerifier string

func (a *App) StartPixivOAuth() string {
	var url string
	url, codeVerifier = pixivmobile.GetOAuthURL()
	return url
}

func (a *App) VerifyPixivOAuthCode(code string) error {
	if codeVerifier == "" {
		return errors.New("code verifier is empty, please start the OAuth process first")
	}

	refreshToken, err := pixivmobile.VerifyOAuthCode(code, codeVerifier, 15)
	if err != nil {
		return err
	}

	return a.appData.SetSecureString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY, refreshToken)
}

func (a *App) SetPixivOAuthRefreshToken(refreshToken string) error {
	if _, _, err := pixivmobile.RefreshAccessToken(a.ctx, 15, refreshToken); err != nil {
		return err
	}
	return a.appData.SetSecureString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY, refreshToken)

}
func (a *App) GetPixivRefreshToken() string {
	return a.appData.GetSecuredString(constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY)
}
