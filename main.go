package main

import (
	"embed"
	"path/filepath"

	cdlogic "github.com/KJHJason/Cultured-Downloader-Logic"
	cdlogger "github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader/backend/app"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/logger"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"github.com/wailsapp/wails/v2/pkg/options/linux"
	"github.com/wailsapp/wails/v2/pkg/options/mac"
	"github.com/wailsapp/wails/v2/pkg/options/windows"
)

//go:embed all:frontend/dist
var assets embed.FS

//go:embed build/appicon.png
var icon []byte

func main() {
	cdlogger.InitLogger()

	// Create an instance of the app structure
	cdApp := app.NewApp()

	// Create application with options
	err := wails.Run(&options.App{
		Title:     "Cultured Downloader",
		Width:     1024,
		Height:    768,
		MinWidth:  380,
		MinHeight: 400,
		// MaxWidth:          1280,
		// MaxHeight:         800,
		DisableResize:     false,
		Fullscreen:        false,
		Frameless:         false,
		StartHidden:       false,
		HideWindowOnClose: false,
		BackgroundColour: &options.RGBA{
			R: 255,
			G: 255,
			B: 255,
			A: 255,
		},
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		Menu:               nil,
		Logger:             cdlogic.GetLogger(),
		LogLevel:           logger.DEBUG,
		LogLevelProduction: logger.INFO,
		OnStartup:          cdApp.Startup,
		OnShutdown:         cdApp.Shutdown,
		WindowStartState:   options.Normal,
		Bind: []interface{}{
			cdApp,
		},
		// Windows platform specific options
		Windows: &windows.Options{
			WebviewIsTransparent:              false,
			WindowIsTranslucent:               false,
			DisableWindowIcon:                 false,
			DisableFramelessWindowDecorations: false,
			WebviewUserDataPath:               filepath.Join(iofuncs.APP_PATH, "webview-data"),
			ZoomFactor:                        1.0,
		},
		// Mac platform specific options
		Mac: &mac.Options{
			TitleBar: &mac.TitleBar{
				TitlebarAppearsTransparent: false,
				HideTitle:                  false,
				HideTitleBar:               false,
				FullSizeContent:            false,
				UseToolbar:                 false,
				HideToolbarSeparator:       true,
			},
			Appearance:           mac.NSAppearanceNameDarkAqua,
			WebviewIsTransparent: false,
			WindowIsTranslucent:  false,
			About: &mac.AboutInfo{
				Title:   "Cultured Downloader",
				Message: "",
				Icon:    icon,
			},
		},
		// Linux platform specific options
		Linux: &linux.Options{
			Icon:                icon,
			ProgramName:         "Cultured Downloader",
			WindowIsTranslucent: false,
		},
	})

	if err != nil {
		cdlogic.GetLogger().Fatal(err.Error())
	}
}
