package app

import (
	"container/list"
	"context"
	"fmt"
	"os"
	"path/filepath"

	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx            context.Context
	appData        *appdata.AppData
	downloadQueues list.List // doubly linked list of DownloadQueue
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

func (a *App) GetUsername() string {
	return a.appData.GetString(constants.UsernameKey)
}

// Greet returns a greeting for the given name
// func (a *App) Greet(name string) string {
// 	if err := a.appData.SetString("name", name); err != nil {
// 		runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
// 			Type:    runtime.ErrorDialog,
// 			Title:   "Error saving name!",
// 			Message: "Please refer to the logs or report this issue on GitHub.",
// 		})
// 	}
// 	return fmt.Sprintf("Hello %s, Your name has been saved!", name)
// }

func (app *App) GetDarkMode() bool {
	return app.appData.GetBool(constants.DarkModeKey)
}

func (app *App) SetDarkMode(darkMode bool) {
	app.appData.SetBool(constants.DarkModeKey, darkMode)
}

func (app *App) SetUsername(username string) {
	app.appData.SetString(constants.UsernameKey, username)
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
	if err != nil {
		return pic, err
	}

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
				DisplayName: "Images (*.png;*.jpg,*.jpeg,*.gif;*.webp)",
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

	oldProfilePicPath := app.appData.GetString(constants.ProfilePicPathKey)
	oldProfilePicPath = filepath.Join(constants.UserConfigDir, oldProfilePicPath)
	if oldProfilePicPath != "" {
		// If there is an old profile pic, delete it
		os.Remove(oldProfilePicPath)
	}

	picPathToSave := filepath.Join(constants.UserConfigDir, fileName)
	app.appData.SetString(constants.ProfilePicPathKey, fileName)
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
	profilePicPath := app.appData.GetString(constants.ProfilePicPathKey)
	if profilePicPath == "" {
		return false
	}

	profilePicPath = filepath.Join(constants.UserConfigDir, profilePicPath)
	_, err := os.Stat(profilePicPath)

	hasProfilePic := err == nil
	if profilePicPath != "" && !hasProfilePic {
		// If the path is set but the file does not exist, unset the path
		app.appData.Unset(constants.ProfilePicPathKey)
	}
	return err == nil
}

func (app *App) GetProfilePic() (ProfilePic, error) {
	profilePicPath := app.appData.GetString(constants.ProfilePicPathKey)
	profilePicPath = filepath.Join(constants.UserConfigDir, profilePicPath)
	return NewProfilePic(profilePicPath)
}

func (app *App) DeleteProfilePic() error {
	filePath := app.appData.GetString(constants.ProfilePicPathKey)
	filePath = filepath.Join(constants.UserConfigDir, filePath)
	if filePath == "" {
		return nil
	}
	return os.Remove(filePath)
}
