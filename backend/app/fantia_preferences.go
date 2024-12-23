package app

import (
	"fmt"

	"github.com/KJHJason/Cultured-Downloader-Logic/cdlerrors"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) SetFantiaPreferences(p *FantiaPreferences) error {
	if p == nil {
		return fmt.Errorf(
			"error %d: fantia preferences is nil in SetFantiaPreferences()",
			cdlerrors.DEV_ERROR,
		)
	}

	if err := a.appData.SetBool(constants.FANTIA_ORGANISE_IMAGES_KEY, p.OrganisePostImages); err != nil {
		return err
	}
	return nil
}
