package appdata

import (
	"encoding/base64"
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
	data               map[string]interface{}
	dataPath           string
	masterPassword     string // Used as key to encrypt/decrypt the secured data
	masterPasswordHash []byte // Mainly to verify if the master password is correct
	mu                 sync.RWMutex
}

func NewAppData() (*AppData, error) {
	appData := AppData{
		data:      make(map[string]interface{}),
		dataPath:  filepath.Join(constants.UserConfigDir, filename),
		mu:        sync.RWMutex{},
	}
	err := appData.loadFromFile()
	if err != nil {
		logger.MainLogger.Error("Error loading data from file:", err)
		return nil, err
	}
	appData.masterPasswordHash = appData.GetSecuredBytesWithFallback(constants.MasterPasswordHashKey, nil)
	return &appData, nil
}

func (a *AppData) SetMasterPassword(password string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.masterPassword = password
}

func (a *AppData) ChangeMasterPassword(password string, hash []byte) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.masterPassword = password
	a.masterPasswordHash = hash
}

func (a *AppData) GetMasterPassword() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.masterPassword
}

func (a *AppData) GetMasterPasswordHash() []byte {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.masterPasswordHash
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
		logger.MainLogger.Errorf("Error saving data to file with key %q: %v", key, err)
	}
	return err
}

// Securely stores the newValue in the appData
func (a *AppData) setSecureB(key string, newValue []byte) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	// If the newValue is of []interface{} type, check if there's a need to save or not by comparing the length and values
	oldValue, exist := a.data[key]
	if exist && checkIfValueIsSame(oldValue, newValue) {
		return nil
	}

	encryptedNewValue, err := EncryptWithPassword(a, newValue, a.masterPassword)
	if err != nil {
		return err
	}

	a.data[key] = base64.StdEncoding.EncodeToString(encryptedNewValue)
	err = a.saveToFile()
	if err != nil {
		logger.MainLogger.Errorf("Error saving data to file for key %q: %v", key, err)
	}
	return err
}

// Securely stores the newValue (utf-8 encoded) in the appData
func (a *AppData) setSecureS(key string, newValue string) error {
	return a.setSecureB(key, []byte(newValue))
}

// Main logic for securely retrieving the value from the appData
// Encrypted values are stored as base64 encoded strings. Hence, we need to decode it first before decrypting it.
func (a *AppData) getSecure(key string) ([]byte, bool) {
	a.mu.RLock()
	defer a.mu.RUnlock()

	v, exist := a.data[key]
	if !exist {
		return nil, false
	}

	var resetValue = func() {
		a.data[key] = ""
		if err := a.saveToFile(); err != nil {
			logger.MainLogger.Errorf("Error saving data with key %q to file: %v", key, err)
		}
	}

	valBytes, err := base64.StdEncoding.DecodeString(v.(string))
	if err != nil {
		logger.MainLogger.Errorf("Error decoding base64 string for data key %q: %v", key, err)

		// reset the value if it's not a valid base64 string
		resetValue()
		return nil, false
	}

	decryptedVal, err := DecryptWithPassword(a, valBytes, a.masterPassword)
	if err != nil {
		logger.MainLogger.Errorf("Error decrypting value for data %q: %v", key, err)

		// reset the value if it's not a valid base64 string
		resetValue()
		return nil, false
	}

	return decryptedVal, true
}

// Securely retrieves the value from the appData
func (a *AppData) getSecureB(key string) ([]byte, bool) {
	return a.getSecure(key)
}

// Securely retrieves the value from the appData
func (a *AppData) getSecureS(key string) (string, bool) {
	val, exist := a.getSecure(key)
	if !exist {
		return "", false
	}
	return string(val), true
}
