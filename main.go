package main

import (
	"embed"
	"log"

	"github.com/KJHJason/Cultured-Downloader/backend/app"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/logger"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"github.com/wailsapp/wails/v2/pkg/options/mac"
	"github.com/wailsapp/wails/v2/pkg/options/windows"
)

//go:embed all:frontend/dist
var assets embed.FS

//go:embed build/appicon.png
var icon []byte

func main() {
	// Create an instance of the app structure
	cdApp := app.NewApp()

	// Create application with options
	err := wails.Run(&options.App{
		Title:				"Cultured Downloader",
		Width:				1024,
		Height:				768,
		MinWidth:			380,
		MinHeight:			400,
		// MaxWidth:          1280,
		// MaxHeight:         800,
		DisableResize:		false,
		Fullscreen:			false,
		Frameless:			false,
		StartHidden:		false,
		HideWindowOnClose:	false,
		BackgroundColour:	&options.RGBA{
			R: 255, 
			G: 255, 
			B: 255, 
			A: 255,
		},
		AssetServer:		&assetserver.Options{
			Assets: assets,
		},
		Menu:				nil,
		Logger:				nil,
		LogLevel:			logger.DEBUG,
		OnStartup:			cdApp.Startup,
		OnShutdown:			cdApp.Shutdown,
		// OnDomReady:        app.domReady,
		// OnBeforeClose:     app.beforeClose,
		// OnShutdown:        app.shutdown,
		WindowStartState:	options.Normal,
		Bind: []interface{}{
			cdApp,
		},
		// Windows platform specific options
		Windows: &windows.Options{
			WebviewIsTransparent:	false,
			WindowIsTranslucent:	false,
			DisableWindowIcon:		false,
			// DisableFramelessWindowDecorations: false,
			WebviewUserDataPath: "",
			ZoomFactor: 1.0,
		},
		// Mac platform specific options
		Mac: &mac.Options{
			TitleBar: &mac.TitleBar{
				TitlebarAppearsTransparent:	true,
				HideTitle:					false,
				HideTitleBar:				false,
				FullSizeContent:			false,
				UseToolbar:		 			false,
				HideToolbarSeparator:		true,
			},
			Appearance:           mac.NSAppearanceNameDarkAqua,
			WebviewIsTransparent: true,
			WindowIsTranslucent:  true,
			About: &mac.AboutInfo{
				Title:		"Cultured Downloader",
				Message:	"",
				Icon:		icon,
			},
		},
	})

	if err != nil {
		log.Fatal(err)
	}
}
