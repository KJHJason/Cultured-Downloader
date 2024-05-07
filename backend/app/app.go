package app

import (
	"container/list"
	"context"
	"fmt"
	"os"
	"errors"
	"path/filepath"

	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
	"github.com/KJHJason/Cultured-Downloader-Logic/httpfuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx            context.Context
	appData        *appdata.AppData
	lang           string
	downloadQueues list.List // doubly linked list of DownloadQueue
	gdriveClient   *gdrive.GDrive
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

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

func (a *App) GetUsername() string {
	return a.appData.GetString(constants.USERNAME_KEY)
}

func (app *App) GetDarkMode() bool {
	return app.appData.GetBool(constants.DARK_MODE_KEY)
}

func (app *App) SetDarkMode(darkMode bool) {
	app.appData.SetBool(constants.DARK_MODE_KEY, darkMode)
}

func (app *App) SetUsername(username string) {
	app.appData.SetString(constants.USERNAME_KEY, username)
}

type ProfilePic struct {
	Path     string
	Type     string
	Filename string
	Data     []byte
}

func NewProfilePic(path string) (ProfilePic, error) {
	var err error
	var pic ProfilePic

	if path == "" {
		return pic, nil
	}

	if _, err = os.Stat(path); err != nil {
		return pic, fmt.Errorf("file does not exist")
	}

	data, err := os.ReadFile(path)
	if err != nil {
		return pic, err
	}

	// https://www.freeformatter.com/mime-types-list.html#mime-types-list
	pic.Type = filepath.Ext(path)[1:] // remove the dot
	if pic.Type == "jpg" {
		pic.Type = "jpeg"
	}

	pic.Path = path
	pic.Data = data
	pic.Filename = filepath.Base(path)
	return pic, nil
}

func (app *App) SelectProfilePic() (ProfilePic, error) {
	selection, err := runtime.OpenFileDialog(app.ctx, runtime.OpenDialogOptions{
		Title: "Select File",
		Filters: []runtime.FileFilter{
			{
				DisplayName: "Images (*.png,*.jpg,*.jpeg,*.gif,*.webp)",
				Pattern:     "*.png;*.jpg;*.jpeg;*.gif;*.webp",
			},
		},
	})

	if err != nil {
		return ProfilePic{}, err
	}
	return NewProfilePic(selection)
}

func (app *App) UploadProfilePic(picPath string) error {
	fileName := filepath.Base(picPath)
	data, err := os.ReadFile(picPath)
	if err != nil {
		return err
	}

	oldProfilePicPath := app.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	oldProfilePicPath = filepath.Join(iofuncs.APP_PATH, oldProfilePicPath)
	if oldProfilePicPath != "" {
		// If there is an old profile pic, delete it
		os.Remove(oldProfilePicPath)
	}

	picPathToSave := filepath.Join(iofuncs.APP_PATH, fileName)
	app.appData.SetString(constants.PROFILE_PIC_PATH_KEY, fileName)
	file, err := os.OpenFile(picPathToSave, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.Write(data)
	if err != nil {
		return err
	}
	return nil
}

func (app *App) HasProfilePic() bool {
	profilePicPath := app.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	if profilePicPath == "" {
		return false
	}

	profilePicPath = filepath.Join(iofuncs.APP_PATH, profilePicPath)
	_, err := os.Stat(profilePicPath)

	hasProfilePic := err == nil
	if profilePicPath != "" && !hasProfilePic {
		// If the path is set but the file does not exist, unset the path
		app.appData.Unset(constants.PROFILE_PIC_PATH_KEY)
	}
	return err == nil
}

func (app *App) GetProfilePic() (ProfilePic, error) {
	profilePicPath := app.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	profilePicPath = filepath.Join(iofuncs.APP_PATH, profilePicPath)
	return NewProfilePic(profilePicPath)
}

func (app *App) DeleteProfilePic() error {
	filePath := app.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	filePath = filepath.Join(iofuncs.APP_PATH, filePath)
	if filePath == "" {
		return nil
	}
	return os.Remove(filePath)
}
