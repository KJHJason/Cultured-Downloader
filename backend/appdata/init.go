package appdata

import (
	"os"
	"path/filepath"
)

var (
	UserConfigDir string
	UserConfigDirErr error
)

const (
	DefaultDirPerm = 0755
)

func init() {
	// Try to get the OS specific path to the user config directory
	UserConfigDir, UserConfigDirErr = os.UserConfigDir()
	if UserConfigDirErr == nil {
		// If we got the path, append the app name to it
		UserConfigDir = filepath.Join(UserConfigDir, "cultured.downloader")

		// Create the directory if it doesn't exist
		os.MkdirAll(UserConfigDir, DefaultDirPerm)
	}
}
