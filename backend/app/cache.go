package app

import (
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/KJHJason/Cultured-Downloader-Logic/cache"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func (a *App) changeCacheDbLocationLogic(newLocation string) error {
	if newLocation == "" {
		return nil
	}

	if !iofuncs.DirPathExists(newLocation) {
		return errors.New("directory path does not exist")
	}

	f, err := os.Open(newLocation)
	if err != nil {
		return fmt.Errorf("error opening directory: %w", err)
	}
	defer f.Close()

	// https://stackoverflow.com/a/30708914/16377492
	_, err = f.Readdirnames(1)
	if !errors.Is(err, io.EOF) {
		return errors.New("directory is not empty")
	}

	oldPath := a.appData.GetStringWithFallback(constants.CACHE_DB_PATH_KEY, cache.DEFAULT_PATH)
	a.mvCacheDbTask = func() error {
		return cache.MoveDb(oldPath, newLocation)
	}

	err = a.appData.SetString(constants.CACHE_DB_PATH_KEY, newLocation)
	if err != nil {
		return fmt.Errorf("error saving new cache db location: %w", err)
	}
	return nil
}

func (a *App) ChangeCacheDbLocation(newLocation string) error {
	return a.changeCacheDbLocationLogic(newLocation)
}

func (a *App) SelectNewCacheDbLocation() error {
	newLocation, err := runtime.OpenDirectoryDialog(a.ctx, runtime.OpenDialogOptions{
		Title: "Select new cache database location",
	})
	if err != nil {
		return err
	}
	if newLocation == "" {
		return errors.New("no directory selected")
	}
	return a.changeCacheDbLocationLogic(newLocation)
}

func (a *App) GetCacheDbLocation() string {
	return a.appData.GetStringWithFallback(constants.CACHE_DB_PATH_KEY, cache.DEFAULT_PATH)
}

func (a *App) DeleteCacheKey(cacheKey string) error {
	return cache.Delete(cacheKey)
}

type filter struct {
	Fantia      bool
	Pixiv       bool
	PixivFanbox bool
	Kemono      bool
}

func (a *App) GetPostCache(filter filter) []*cache.PostCache {
	if filter.Fantia && filter.Pixiv && filter.PixivFanbox && filter.Kemono {
		return cache.GetAllCacheForAllPlatforms(a.ctx)
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
	return cache.GetAllCacheForPlatform(a.ctx, filters...)
}

func (a *App) DeleteAllPostCache() error {
	return cache.DeletePostCacheForAllPlatforms(a.ctx)
}

type CacheKey struct {
	Key      string // key is a formatted string without the suffix
	Val      string
	CacheKey string
}

func getCacheLogic(ctx context.Context, fetchCacheFunc func(context.Context) []*cache.CacheKeyValue) []CacheKey {
	cacheKeys := fetchCacheFunc(ctx)
	cacheKeysToReturn := make([]CacheKey, len(cacheKeys))
	for idx, c := range cacheKeys {
		cacheKey := c.GetKey()

		var fmtKey string
		split := strings.Split(cacheKey, cache.SUFFIX)
		splitLen := len(split)
		if splitLen < 2 {
			fmtKey = cacheKey // shouldn't happen but just in case
		} else {
			fmtKey = strings.Join(split[:splitLen-1], cache.SUFFIX)
		}

		cacheKeysToReturn[idx] = CacheKey{
			Key:      fmtKey,
			Val:      c.GetVal(),
			CacheKey: cacheKey,
		}
	}
	return cacheKeysToReturn
}

func (a *App) GetAllGdriveCache() []CacheKey {
	return getCacheLogic(a.ctx, cache.GetAllGdriveCache)
}

func (a *App) DeleteAllGdriveCache() error {
	return cache.DeleteAllGdriveCache(a.ctx)
}

func (a *App) GetAllUgoiraCache() []CacheKey {
	return getCacheLogic(a.ctx, cache.GetAllUgoiraCache)
}

func (a *App) DeleteAllUgoiraCache() error {
	return cache.DeleteAllUgoiraCache(a.ctx)
}

func (a *App) GetAllKemonoCreatorCache() []CacheKey {
	return getCacheLogic(a.ctx, cache.GetAllKemonoCreatorCache)
}

func (a *App) DeleteAllKemonoCreatorCache() error {
	return cache.DeleteAllKemonoCreatorCache(a.ctx)
}
