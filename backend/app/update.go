package app

import (
	"errors"

	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

type ProgramInfo struct {
	ProgramVer string
	BackendVer string
}

func (a *App) GetProgramInfo() ProgramInfo {
	return ProgramInfo{
		ProgramVer: constants.PROGRAM_VER,
		BackendVer: cdlconst.VERSION,
	}
}

func (a *App) CheckForUpdates() (bool, error) {
	outdated, err := httpfuncs.CheckVer("KJHJason/Cultured-Downloader", constants.PROGRAM_VER, false, nil)
	if err == nil {
		return outdated, nil
	}

	if errors.Is(err, httpfuncs.ErrProcessLatestVer) {
		return false, nil
	}
	if errors.Is(err, httpfuncs.ErrProcessVer) {
		return false, nil
	}
	return false, err
}
