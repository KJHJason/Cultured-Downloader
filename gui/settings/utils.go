package settings

import (
	"fmt"
	"os"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
)

func readPath(path string) ([]byte, error) {
	if !iofuncs.PathExists(path) {
		return nil, fmt.Errorf("filepath does not exist")
	}

	fileBytes, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return fileBytes, nil
}
