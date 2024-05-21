package app

import (
	"time"

	"github.com/KJHJason/Cultured-Downloader-Logic/database"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *App) DeleteCacheKey(bucket, cacheKey string) error {
	return database.AppDb.Delete(bucket, cacheKey)
}

type Filter struct {
	Fantia      bool `json:"Fantia"`
	Pixiv       bool `json:"Pixiv"`
	PixivFanbox bool `json:"PixivFanbox"`
	Kemono      bool `json:"Kemono"`
}

func (a *App) GetPostCache(filter Filter) []*database.PostCache {
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

type FrontendCacheKeyValue struct {
	Key      string    `json:"Key"`
	Value    string    `json:"Value"`
	DateTime time.Time `json:"DateTime"`
	Bucket   string    `json:"Bucket"`
}

func parseKeyValues(keyValues []*database.KeyValue, hasDatetime bool) []*FrontendCacheKeyValue {
	frontendKeyValues := make([]*FrontendCacheKeyValue, 0, len(keyValues))
	for _, keyValue := range keyValues {
		value := &FrontendCacheKeyValue{
			Key:    keyValue.GetKey(),
			Value:  keyValue.GetVal(),
			Bucket: keyValue.Bucket,
		}
		if hasDatetime {
			value.DateTime = database.ParseBytesToDateTime(keyValue.Val)
		}
		frontendKeyValues = append(frontendKeyValues, value)
	}
	return frontendKeyValues
}

func (a *App) GetAllGdriveCache() []*FrontendCacheKeyValue {
	return parseKeyValues(database.GetAllGdriveCache(), true)
}

func (a *App) DeleteAllGdriveCache() error {
	return database.DeleteAllGdriveCache()
}

func (a *App) GetAllUgoiraCache() []*FrontendCacheKeyValue {
	return parseKeyValues(database.GetAllUgoiraCache(), true)
}

func (a *App) DeleteAllUgoiraCache() error {
	return database.DeleteAllUgoiraCache()
}

func (a *App) GetAllKemonoCreatorCache() []*FrontendCacheKeyValue {
	return parseKeyValues(database.GetAllKemonoCreatorCache(), false)
}

func (a *App) DeleteAllKemonoCreatorCache() error {
	return database.DeleteAllKemonoCreatorCache()
}
