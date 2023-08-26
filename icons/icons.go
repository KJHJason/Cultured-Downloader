package icons

import (
	"fyne.io/fyne/v2"
	_ "embed"
)

var (
	CulturedDownloaderIcon fyne.Resource

	//go:embed fantia-logo.png
	fantiaIconBytes []byte
	FantiaIcon *fyne.StaticResource	

	//go:embed pixiv-fanbox-logo.png
	pixivFanboxIconBytes []byte
	PixivFanboxIcon *fyne.StaticResource

	//go:embed pixiv-logo.png
	pixivIconBytes []byte
	PixivIcon *fyne.StaticResource

	//go:embed kemono-logo.png
	kemonoIconBytes []byte
	KemonoIcon *fyne.StaticResource
)

func init() {
	// have to load from path due to "image: unknown format" error when using embed
	var err error
	CulturedDownloaderIcon, err = fyne.LoadResourceFromPath("./icons/cultured-downloader-logo.png")
	if err != nil {
		// should never happen unless the file is missing
		panic(err)
	}

	FantiaIcon = fyne.NewStaticResource("fantia-logo.png", fantiaIconBytes)
	PixivFanboxIcon = fyne.NewStaticResource("pixiv-fanbox-logo.png", pixivFanboxIconBytes)
	PixivIcon = fyne.NewStaticResource("pixiv-logo.png", pixivIconBytes)
	KemonoIcon = fyne.NewStaticResource("kemono-logo.png", kemonoIconBytes)
}
