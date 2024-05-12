package app

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) GetUsername() string {
	return a.appData.GetString(constants.USERNAME_KEY)
}

func (a *App) SetUsername(username string) {
	a.appData.SetString(constants.USERNAME_KEY, username)
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

func (a *App) SelectProfilePic() (ProfilePic, error) {
	selection, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
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

func (a *App) UploadProfilePic(picPath string) error {
	fileName := filepath.Base(picPath)
	data, err := os.ReadFile(picPath)
	if err != nil {
		return err
	}

	oldProfilePicPath := a.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	oldProfilePicPath = filepath.Join(iofuncs.APP_PATH, oldProfilePicPath)
	if oldProfilePicPath != "" {
		// If there is an old profile pic, delete it
		os.Remove(oldProfilePicPath)
	}

	picPathToSave := filepath.Join(iofuncs.APP_PATH, fileName)
	a.appData.SetString(constants.PROFILE_PIC_PATH_KEY, fileName)
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

func (a *App) HasProfilePic() bool {
	profilePicPath := a.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	if profilePicPath == "" {
		return false
	}

	profilePicPath = filepath.Join(iofuncs.APP_PATH, profilePicPath)
	_, err := os.Stat(profilePicPath)

	hasProfilePic := err == nil
	if profilePicPath != "" && !hasProfilePic {
		// If the path is set but the file does not exist, unset the path
		a.appData.Unset(constants.PROFILE_PIC_PATH_KEY)
	}
	return err == nil
}

func (a *App) GetProfilePic() (ProfilePic, error) {
	profilePicPath := a.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	profilePicPath = filepath.Join(iofuncs.APP_PATH, profilePicPath)
	return NewProfilePic(profilePicPath)
}

func (a *App) DeleteProfilePic() error {
	filePath := a.appData.GetString(constants.PROFILE_PIC_PATH_KEY)
	filePath = filepath.Join(iofuncs.APP_PATH, filePath)
	if filePath == "" {
		return nil
	}
	return os.Remove(filePath)
}
