package appdata

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sync"

	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

const (
	filename = "data.json"
	jsonIndent = "    "
)

type AppData struct {
	data     map[string]interface{}
	dataPath string
	mu       sync.RWMutex
}

var (
	Data           *AppData
	InitialLoadErr error
)

func init() {
	Data, InitialLoadErr = NewAppData()
}

func NewAppData() (*AppData, error) {
	appData := AppData{
		data:     make(map[string]interface{}),
		dataPath: filepath.Join(constants.UserConfigDir, filename),
		mu:       sync.RWMutex{},
	}
	err := appData.loadFromFile()
	if err != nil {
		logger.MainLogger.Error("Error loading data from file:", err)
		return nil, err
	}
	return &appData, nil
}

// Remember to lock the mutex before calling this function
func (a *AppData) saveToFile() error {
	jsonData, err := json.MarshalIndent(a.data, "", jsonIndent)
	if err != nil {
		return err
	}

	os.MkdirAll(constants.UserConfigDir, constants.DefaultPerm)
	err = os.WriteFile(a.dataPath, jsonData, constants.DefaultPerm)
	if err != nil {
		return err
	}

	logger.MainLogger.Info("Data saved to", a.dataPath)
	return nil
}

func (a *AppData) loadFromFile() error {
	a.mu.Lock()
	defer a.mu.Unlock()

	var data map[string]interface{}
	os.MkdirAll(constants.UserConfigDir, constants.DefaultPerm)

	fileSize, _ := iofuncs.GetFileSize(a.dataPath)
	if !iofuncs.PathExists(a.dataPath) ||  fileSize == 0 {
		return nil
	}

	fileData, err := os.ReadFile(a.dataPath)
	if err != nil {
		return err
	}

	err = json.Unmarshal(fileData, &data)
	if err != nil {
		return err
	}

	convertDataMapInterface(data)
	logger.MainLogger.Info("Data loaded from", filename)
	a.data = data
	return nil
}

func (a *AppData) get(key string) (interface{}, bool) {
	a.mu.RLock()
	defer a.mu.RUnlock()

	v, exist := a.data[key]
	return v, exist
}

func (a *AppData) set(key string, newValue interface{}) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	// If the newValue is of []interface{} type, check if there's a need to save or not by comparing the length and values
	oldValue, exist := a.data[key]
	if exist && checkIfValueIsSame(oldValue, newValue) {
		return nil
	}

	a.data[key] = newValue
	err := a.saveToFile()
	if err != nil {
		logger.MainLogger.Errorf("Error saving data to file: %v", err)
	}
	return err
}
