package app

import (
	"github.com/KJHJason/Cultured-Downloader-Logic/database"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) DeleteCacheKey(bucket, cacheKey string) error {
	return database.AppDb.Delete(bucket, cacheKey)
}

type filter struct {
	Fantia      bool
	Pixiv       bool
	PixivFanbox bool
	Kemono      bool
}

func (a *App) GetPostCache(filter filter) []*database.PostCache {
	if filter.Fantia && filter.Pixiv && filter.PixivFanbox && filter.Kemono {
		return database.GetAllCacheForAllPlatforms()
	}

	filters := make([]string, 0, 3)
	if filter.Fantia {
		filters = append(filters, constants.FANTIA)
	}
	if filter.Pixiv {
		filters = append(filters, constants.PIXIV)
	}
	if filter.PixivFanbox {
		filters = append(filters, constants.PIXIV_FANBOX)
	}
	if filter.Kemono {
		filters = append(filters, constants.KEMONO)
	}
	return database.GetAllCacheForPlatform(filters...)
}

func (a *App) DeleteAllPostCache() error {
	return database.DeletePostCacheForAllPlatforms()
}

func (a *App) GetAllGdriveCache() []*database.CacheKeyValue {
	return database.GetAllGdriveCache()
}

func (a *App) DeleteAllGdriveCache() error {
	return database.DeleteAllGdriveCache()
}

func (a *App) GetAllUgoiraCache() []*database.CacheKeyValue {
	return database.GetAllUgoiraCache()
}

func (a *App) DeleteAllUgoiraCache() error {
	return database.DeleteAllUgoiraCache()
}

func (a *App) GetAllKemonoCreatorCache() []*database.KeyValue {
	return database.GetAllKemonoCreatorCache()
}

func (a *App) DeleteAllKemonoCreatorCache() error {
	return database.DeleteAllKemonoCreatorCache()
}
