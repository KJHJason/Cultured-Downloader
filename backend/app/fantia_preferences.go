package app

import (
	"fmt"

	cdlerrors "github.com/KJHJason/Cultured-Downloader-Logic/errors"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) SetFantiaPreferences(p *preferences) error {
	if p == nil {
		return fmt.Errorf(
			"error %d: preferences is nil in SetFantiaPreferences()",
			cdlerrors.DEV_ERROR,
		)
	}

	if err := a.appData.SetBool(constants.FANTIA_ORGANISE_IMAGES_KEY, p.OrganisePostImages); err != nil {
		return err
	}
	return nil
}
