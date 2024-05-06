package appdata

import (
	"encoding/base64"

	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

func (a *AppData) GetBool(key string) bool {
	return a.GetBoolWithFallback(key, false)
}

func (a *AppData) GetBoolSlice(key string) []bool {
	return a.GetBoolSliceWithFallback(key, []bool{})
}

func (a *AppData) GetBoolWithFallback(key string, fallback bool) bool {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	b, isBool := v.(bool)
	if !isBool {
		return fallback
	}
	return b
}

func (a *AppData) GetBoolSliceWithFallback(key string, fallback []bool) []bool {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	b, isBoolSlice := v.([]bool)
	if !isBoolSlice {
		return fallback
	}
	return b
}

func (a *AppData) GetFloat(key string) float64 {
	return a.GetFloatWithFallback(key, 0.0)
}

func (a *AppData) GetFloatSlice(key string) []float64 {
	return a.GetFloatSliceWithFallback(key, []float64{})
}

func (a *AppData) GetFloatWithFallback(key string, fallback float64) float64 {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	f, isFloat64 := v.(float64)
	if !isFloat64 {
		return fallback
	}
	return f
}

func (a *AppData) GetFloatSliceWithFallback(key string, fallback []float64) []float64 {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	floats, ok := v.([]float64)
	if ok {
		return floats
	}

	ints, ok := v.([]int)
	if ok {
		floats = make([]float64, len(ints))
		for i, v := range ints {
			floats[i] = float64(v)
		}
		return floats
	}
	return fallback
}

func (a *AppData) GetInt(key string) int {
	return a.GetIntWithFallback(key, 0)
}

func (a *AppData) GetIntSlice(key string) []int {
	return a.GetIntSliceWithFallback(key, []int{})
}

func (a *AppData) GetIntWithFallback(key string, fallback int) int {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	i, isInt := v.(int)
	if !isInt {
		return fallback
	}
	return i
}

func (a *AppData) GetIntSliceWithFallback(key string, fallback []int) []int {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	ints, ok := v.([]int)
	if ok {
		return ints
	}

	// int can be deserialised as floats
	floats, ok := v.([]float64)
	if ok {
		ints = make([]int, len(floats))
		for idx, v := range floats {
			ints[idx] = int(v)
		}
		return ints
	}
	return fallback
}

func (a *AppData) GetString(key string) string {
	return a.GetStringWithFallback(key, "")
}

func (a *AppData) GetStringSlice(key string) []string {
	return a.GetStringSliceWithFallback(key, []string{})
}

func (a *AppData) GetStringWithFallback(key string, fallback string) string {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	s, isString := v.(string)
	if !isString {
		return fallback
	}
	return s
}

func (a *AppData) GetStringSliceWithFallback(key string, fallback []string) []string {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	s, isStringSlice := v.([]string)
	if !isStringSlice {
		return fallback
	}
	return s
}

func (a *AppData) GetBytes(key string) []byte {
	return a.GetBytesWithFallback(key, []byte{})
}

func (a *AppData) GetBytesWithFallback(key string, fallback []byte) []byte {
	v, exist := a.get(key)
	if !exist {
		return fallback
	}

	s, isString := v.(string) // should be base64 encoded
	if !isString {
		return fallback
	}

	b, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		logger.MainLogger.Errorf("Error decoding base64 string for data key %q: %v", key, err)
		return fallback
	}
	return b
}

func (a *AppData) GetSecuredString(key string) string {
	return a.GetSecuredStringWithFallback(key, "")
}

func (a *AppData) GetSecuredBytes(key string) []byte {
	return a.GetSecuredBytesWithFallback(key, []byte{})
}

func (a *AppData) GetSecuredStringWithFallback(key string, fallback string) string {
	if a.GetString(constants.HASH_OF_MASTER_PASS_HASH_KEY) == "" {
		return a.GetStringWithFallback(key, fallback) // not encrypted
	}

	v, exist := a.getSecureS(key)
	if !exist {
		return fallback
	}
	return v
}

func (a *AppData) GetSecuredBytesWithFallback(key string, fallback []byte) []byte {
	if a.GetString(constants.HASH_OF_MASTER_PASS_HASH_KEY) == "" {
		return a.GetBytesWithFallback(key, fallback) // not encrypted
	}

	v, exist := a.getSecureB(key)
	if !exist {
		return fallback
	}
	return v
}
