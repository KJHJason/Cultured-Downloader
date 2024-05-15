package app

import (
	"errors"
	"fmt"
	goruntime "runtime"

	"github.com/KJHJason/Cultured-Downloader-Logic/configs"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

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

func (a *App) SetFfmpegPath(ffmpegPath string) error {
	if ffmpegPath == "" || ffmpegPath == "ffmpeg" {
		return a.appData.Unset(constants.FFMPEG_KEY)
	}

	if err := configs.ValidateFfmpegPathLogic(a.ctx, ffmpegPath); err != nil {
		return err
	}

	return a.appData.SetString(constants.FFMPEG_KEY, ffmpegPath)
}

func (a *App) SelectFfmpegPath() error {
	var filters []runtime.FileFilter
	if goruntime.GOOS == "windows" {
		filters = []runtime.FileFilter{
			{
				DisplayName: "Executable Files (*.exe)",
				Pattern:     "*.exe",
			},
		}
	} else {
		filters = []runtime.FileFilter{
			{
				DisplayName: "All Files",
				Pattern:     "*",
			},
		}
	}

	ffmpegPath, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
		Title:   "Select FFmpeg executable",
		Filters: filters,
	})
	if err != nil {
		return err
	}
	if ffmpegPath == "" {
		return errors.New("no file selected")
	}

	// open dialog to confirm to avoid accidental execution of an incorrect file
	options := []string{"Yes", "No"}
	messageFmt := "Are you sure you want to set this file, %q, as the FFmpeg executable? Cultured Downloader will EXECUTE this file to verify the FFmpeg binary!"
	confirm, err := runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
		Type:          runtime.QuestionDialog,
		Title:         "Confirm FFmpeg executable",
		Message:       fmt.Sprintf(messageFmt, ffmpegPath),
		Buttons:       options,
		DefaultButton: options[0],
		CancelButton:  options[1],
	})
	if err != nil {
		logger.LogError(err, false, logger.ERROR)
		return err
	}
	if confirm != options[0] {
		return errors.New("no file selected")
	}

	if err := configs.ValidateFfmpegPathLogic(a.ctx, ffmpegPath); err != nil {
		return err
	}
	return a.SetFfmpegPath(ffmpegPath)
}

func (a *App) GetFfmpegPath() string {
	path := a.appData.GetStringWithFallback(constants.FFMPEG_KEY, "ffmpeg")
	if err := configs.ValidateFfmpegPathLogic(a.ctx, path); err != nil {
		if path != "ffmpeg" {
			a.appData.Unset(constants.FFMPEG_KEY)
		}
		return ""
	}
	return path
}

type UserAgentResponse struct {
	UserAgent string
	IsDefault bool
}

func (a *App) GetUserAgent() UserAgentResponse {
	userAgent := a.appData.GetStringWithFallback(constants.USER_AGENT_KEY, httpfuncs.DEFAULT_USER_AGENT)
	isDefault := userAgent == httpfuncs.DEFAULT_USER_AGENT
	return UserAgentResponse{
		UserAgent: userAgent,
		IsDefault: isDefault,
	}
}

func (a *App) SetUserAgent(userAgent string) error {
	if userAgent == "" {
		return errors.New("user agent cannot be empty")
	}

	return a.appData.SetString(constants.USER_AGENT_KEY, userAgent)
}
