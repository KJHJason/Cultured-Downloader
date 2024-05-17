package appdata

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"

	cdlconst "github.com/KJHJason/Cultured-Downloader-Logic/constants"
	"github.com/KJHJason/Cultured-Downloader-Logic/iofuncs"
	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/crypto"
	"github.com/pkg/errors"
)

const (
	filename   = "data.json"
	jsonIndent = "    "
)

func initialiseSettingsMap() map[string]interface{} {
	return map[string]interface{}{
		// General
		constants.DARK_MODE_KEY:        false,
		constants.USERNAME_KEY:         "Ojisan",
		constants.PROFILE_PIC_PATH_KEY: "",
		constants.DOWNLOAD_KEY:         iofuncs.APP_PATH,
		constants.LANGUAGE_KEY:         cdlconst.EN,

		// Download preferences
		constants.DL_THUMBNAIL_KEY:  true,
		constants.DL_IMAGES_KEY:     true,
		constants.DL_ATTACHMENT_KEY: true,
	}
}

type AppData struct {
	data                     map[string]interface{}
	dataPath                 string
	masterPassword           string // Used as key to encrypt/decrypt the secured data
	masterPasswordSalt       []byte
	hashOfMasterPasswordHash []byte // Mainly to verify if the master password is correct
	mu                       sync.RWMutex
}

func NewAppData() (*AppData, error) {
	appData := AppData{
		data:     make(map[string]interface{}),
		dataPath: filepath.Join(iofuncs.APP_PATH, filename),
		mu:       sync.RWMutex{},
	}
	err := appData.loadFromFile()
	if err != nil {
		logger.MainLogger.Errorf("Error loading data from file: %s", err)
		return nil, err
	}
	appData.masterPasswordSalt = appData.GetBytes(constants.MASTER_PASS_SALT_KEY)
	appData.hashOfMasterPasswordHash = appData.GetBytes(constants.HASH_OF_MASTER_PASS_HASH_KEY)
	return &appData, nil
}

func (a *AppData) SetMasterPasswordInMem(password string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.masterPassword = password
}

func (a *AppData) changeMasterPassword(password string) error {
	a.mu.Lock()
	a.masterPassword = password

	// Get a new salt for the new password
	salt := crypto.GenerateNonce(crypto.HashSaltLen)
	a.masterPasswordSalt = salt

	// Get a new hash for the new password
	hash := crypto.HashStringWithSalt(password, salt)
	a.hashOfMasterPasswordHash = crypto.HashData(hash)
	a.mu.Unlock()

	err := a.SetBytes(constants.MASTER_PASS_SALT_KEY, salt)
	if err != nil {
		return err
	}

	err = a.SetBytes(constants.HASH_OF_MASTER_PASS_HASH_KEY, a.hashOfMasterPasswordHash)
	if err != nil {
		a.Unset(constants.MASTER_PASS_SALT_KEY)
		return err
	}

	return nil
}

func (a *AppData) ResetMasterPassword() error {
	a.mu.Lock()

	// saved temporarily to decrypt the encrypted fields
	savedMasterPassword := a.masterPassword
	savedSalt := a.masterPasswordSalt

	a.masterPassword = ""
	a.masterPasswordSalt = nil
	a.hashOfMasterPasswordHash = nil
	a.mu.Unlock()

	err := a.Unset(
		constants.MASTER_PASS_SALT_KEY,
		constants.HASH_OF_MASTER_PASS_HASH_KEY,
	)
	if err != nil {
		return err
	}
	return a.ResetEncryptedFields(savedMasterPassword, savedSalt)
}

func (a *AppData) GetMasterPassword() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.masterPassword
}

func (a *AppData) GetMasterPasswordHash() (hash, salt []byte) {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.hashOfMasterPasswordHash, a.masterPasswordSalt
}

// Remember to lock the mutex before calling this function
func (a *AppData) saveToFile() error {
	jsonData, err := json.MarshalIndent(a.data, "", jsonIndent)
	if err != nil {
		return err
	}

	os.MkdirAll(iofuncs.APP_PATH, cdlconst.DEFAULT_PERMS)
	err = os.WriteFile(a.dataPath, jsonData, cdlconst.DEFAULT_PERMS)
	if err != nil {
		return err
	}

	logger.MainLogger.Infof("Data saved to %s", a.dataPath)
	return nil
}

func (a *AppData) loadFromFile() error {
	a.mu.Lock()
	defer a.mu.Unlock()

	var data map[string]interface{}
	os.MkdirAll(iofuncs.APP_PATH, cdlconst.DEFAULT_PERMS)

	fileSize, _ := iofuncs.GetFileSize(a.dataPath)
	if !iofuncs.PathExists(a.dataPath) || fileSize == 0 {
		a.data = initialiseSettingsMap()
		err := a.saveToFile()
		return err
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
	logger.MainLogger.Infof("Data loaded from %s", filename)
	a.data = data
	return nil
}

func (a *AppData) get(key string) (interface{}, bool) {
	a.mu.RLock()
	defer a.mu.RUnlock()

	v, exist := a.data[key]
	return v, exist
}

func (a *AppData) unset(keys ...string) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	hasChanged := false
	for _, key := range keys {
		if _, exist := a.data[key]; !exist {
			continue
		}

		if !hasChanged {
			hasChanged = true
		}
		delete(a.data, key)
	}
	return a.saveToFile()
}

func (a *AppData) set(key string, newValue interface{}) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	// If the newValue is of []interface{} type, check if there's a need to save or not by comparing the length and values
	oldValue, exist := a.data[key]
	if exist && checkIfValueIsSame(oldValue, newValue) {
		return nil
	}

	// check if the newValue is of []byte type and if it is, convert it to base64 encoded string
	if bytes, isBytes := newValue.([]byte); isBytes {
		newValue = base64.StdEncoding.EncodeToString(bytes)
	}

	a.data[key] = newValue
	err := a.saveToFile()
	if err != nil {
		logger.MainLogger.Errorf("Error saving data to file with key %q: %v", key, err)
	}
	return err
}

func (a *AppData) encryptionLogic(key, password string, value []byte) error {
	encryptedNewValue, err := a.EncryptWithPassword(value, a.masterPasswordSalt, password)
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

// Securely stores the newValue in the appData
func (a *AppData) setSecureB(key string, newValue []byte) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	// If the newValue is of []interface{} type, check if there's a need to save or not by comparing the length and values
	oldValue, exist := a.data[key]
	if exist && checkIfValueIsSame(oldValue, newValue) {
		return nil
	}

	return a.encryptionLogic(key, a.masterPassword, newValue)
}

// Securely stores the newValue (utf-8 encoded) in the appData
func (a *AppData) setSecureS(key string, newValue string) error {
	return a.setSecureB(key, []byte(newValue))
}

// Encrypt the stored plaintext value with the new master password and save it to the appData
func (a *AppData) ChangeToSecure(key string) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	oldValue, exist := a.data[key]
	if !exist {
		return nil
	}

	if plaintext, isString := oldValue.(string); !isString {
		return fmt.Errorf("value for key %q is not a string", key)
	} else {
		return a.encryptionLogic(key, a.masterPassword, []byte(plaintext))
	}
}

func (a *AppData) changeToPlaintextLogic(key, masterPassword string, salt []byte) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	oldValue, exist := a.data[key]
	if !exist {
		return nil
	}

	encodedEncryptedField, isString := oldValue.(string)
	if !isString {
		return fmt.Errorf("value for key %q is not a string", key)
	}

	decodedBytes, err := base64.StdEncoding.DecodeString(encodedEncryptedField)
	if err != nil {
		return errors.Wrap(err, "error decoding base64 string for data key "+key)
	}

	plaintext, err := a.DecryptWithPassword(decodedBytes, salt, masterPassword)
	if err != nil {
		return err
	}

	a.data[key] = string(plaintext)
	err = a.saveToFile()
	if err != nil {
		logger.MainLogger.Errorf("Error saving data to file for key %q: %v", key, err)
	}
	return err
}

// Decrypt the stored encrypted value with the master password
// and save the decrypted plaintext STRING to the appData
func (a *AppData) ChangeToPlaintext(key string) error {
	return a.changeToPlaintextLogic(key, a.masterPassword, a.masterPasswordSalt)
}

// Main logic for securely retrieving the value from the appData
// Encrypted values are stored as base64 encoded strings. Hence, we need to decode it first before decrypting it.
func (a *AppData) getSecure(key string) ([]byte, bool) {
	a.mu.RLock()
	defer a.mu.RUnlock()

	v, exist := a.data[key]
	if !exist || v == "" {
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

	decryptedVal, err := a.DecryptWithPassword(valBytes, a.masterPasswordSalt, a.masterPassword)
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
