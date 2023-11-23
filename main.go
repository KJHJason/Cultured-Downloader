package main

import (
	"embed"
	"net/http"
    "os"
    "strings"
	"fmt"
	"path/filepath"

	"github.com/KJHJason/Cultured-Downloader/backend/constants"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

type FileLoader struct {
    http.Handler
}

func NewFileLoader() *FileLoader {
    return &FileLoader{}
}

func (h *FileLoader) ServeHTTP(res http.ResponseWriter, req *http.Request) {
    var err error
    requestedFilename := strings.TrimPrefix(req.URL.Path, "/")
    println("Requesting file:", requestedFilename)

	localFilePath := filepath.Join(
		constants.UserConfigDir, 
		constants.LocalUserAssetDirName,
		requestedFilename,
	)
	os.MkdirAll(filepath.Dir(localFilePath), constants.DefaultPerm)
    fileData, err := os.ReadFile(localFilePath)
    if err != nil {
        res.WriteHeader(http.StatusBadRequest)
        res.Write([]byte(fmt.Sprintf("Could not load file %s", requestedFilename)))
    }

    res.Write(fileData)
}

func main() {
	// Create an instance of the app structure
	app := NewApp()

	// Create application with options
	err := wails.Run(&options.App{
		Title:  "cultureddownloader",
		Width:  1024,
		Height: 768,
		AssetServer: &assetserver.Options{
			Assets: assets,
			Handler: NewFileLoader(),
		},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
		},
	})

	if err != nil {
		println("Error:", err.Error())
	}
}
