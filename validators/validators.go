package validators

import (
	"fmt"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
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
