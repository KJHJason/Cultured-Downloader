package validators

import (
	"fmt"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/gdrive"
)

func Filepath(s string) error {
	if s == "" {
		return nil
	}

	if !iofuncs.PathExists(s) {
		return fmt.Errorf("filepath does not exist")
	}
	return nil
}

func EmptyStr(s string) error {
	if s == "" {
		return fmt.Errorf("cannot be empty")
	}
	return nil
}

func GdriveApiKey(key string) error {
	if key == "" {
		return nil
	}

	if !gdrive.API_KEY_REGEX.MatchString(key) {
		return fmt.Errorf("invalid API key")
	}
	return nil
}
