package appdata

import (
	"errors"
	"encoding/base64"
	"sync"

	"github.com/KJHJason/Cultured-Downloader/backend/crypto"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

const (
	// Preferences key
	masterKeySalt = "masterkey-salt"
)

// reset the salt for the key derivation function
func ResetMasterKeySalt(appData *AppData) {
	appData.SetString(masterKeySalt, "")
}

var dkMutex sync.Mutex
// Uses Argon2id to derive a 256-bit key from the password
func deriveKey(appData *AppData, password string) ([]byte, error) {
	dkMutex.Lock()
	defer dkMutex.Unlock()

	var salt []byte
	var err error
	if appData.GetString(masterKeySalt) == "" {
		salt = crypto.GenerateNonce(crypto.HashKeyLen)
		appData.SetString(masterKeySalt, base64.StdEncoding.EncodeToString(salt))
	} else {
		salt, err = base64.StdEncoding.DecodeString(appData.GetString(masterKeySalt))
		if err != nil || len(salt) != crypto.HashKeyLen {
			// Shouldn't happen unless the user has tampered with the preferences file,
			// in which case we should just panic after resetting the salt and the encrypted fields
			appData.SetString(masterKeySalt, base64.StdEncoding.EncodeToString(crypto.GenerateNonce(crypto.HashKeyLen)))
			ResetEncryptedFields(appData)
			return nil, err
		}
	}

	// Derive the key using Argon2id
	return crypto.GetKey(password, salt), nil
}

var encryptedFields = [...]string{
	constants.GdriveApiKeyKey,
	constants.GdriveServiceAccKey,

	constants.FantiaCookieValueKey,
}

func ResetEncryptedFields(appData *AppData) {
	appData.SetString(masterKeySalt, "") // reset the salt for the key derivation function
	for _, key := range encryptedFields {
		appData.SetString(key, "")
	}
}

func reEncryptEncryptedField(appData *AppData, encodedCiphertext string, oldMasterPassword, newMasterPassword string) (string, error) {
	decodedCipherText, err := base64.StdEncoding.DecodeString(encodedCiphertext)
	if err != nil {
		return "", err
	}

	// decrypt the ciphertext using the old master password
	plaintext, err := DecryptWithPassword(appData, decodedCipherText, oldMasterPassword)
	if err != nil {
		return "", err
	}

	// encrypt the plaintext using the new master password
	ciphertext, err := EncryptWithPassword(appData, plaintext, newMasterPassword)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func EncryptWithPassword(appData *AppData, plaintext []byte, password string) ([]byte, error) {
	key, err := deriveKey(appData, password)
	if err != nil {
		return nil, err
	}
	return crypto.Encrypt(plaintext, key)
}

func DecryptWithPassword(appData *AppData, ciphertext []byte, password string) ([]byte, error) {
	key, err := deriveKey(appData, password)
	if err != nil {
		return nil, err
	}
	return crypto.Decrypt(ciphertext, key)
}

func ReEncryptEncryptedFields(appData *AppData, oldMasterPassword, newMasterPassword string) error {
	if newMasterPassword == "" {
		return errors.New("new master password cannot be empty")
	}

	if oldMasterPassword == "" || oldMasterPassword == newMasterPassword {
		return nil // no need to re-encrypt
	}

	for _, key := range encryptedFields {
		encodedEncryptedField := appData.GetString(key)
		if encodedEncryptedField != "" {
			reEncryptedField, err := reEncryptEncryptedField(
				appData, 
				encodedEncryptedField, 
				oldMasterPassword, 
				newMasterPassword,
			)
			if err != nil {
				return err
			} else {
				appData.SetString(key, reEncryptedField)
			}
		}
	}
	return nil
}

func EncryptPlainField(appData *AppData, key string, plaintext []byte, masterPassword string) error {
	ciphertext, err := EncryptWithPassword(appData, plaintext, masterPassword)
	if err != nil {
		return err
	}

	appData.SetString(key, base64.StdEncoding.EncodeToString(ciphertext))
	return nil
}

func EncryptPlainFields(appData *AppData, masterPassword string) error {
	for _, key := range encryptedFields {
		plaintext := appData.GetString(key)
		if plaintext == "" {
			continue
		}
		if err := EncryptPlainField(appData, key, []byte(plaintext), masterPassword); err != nil {
			return err
		}
	}
	return nil
}

func DecryptEncryptedFieldBytes(appData *AppData, key string, masterPassword string) ([]byte, error) {
	encodedEncryptedField := appData.GetString(key)
	if encodedEncryptedField == "" {
		return nil, nil
	}

	decodedCipherText, err := base64.StdEncoding.DecodeString(encodedEncryptedField)
	if err != nil {
		return nil, err
	}

	// decrypt the ciphertext using the master password
	plaintext, err := DecryptWithPassword(appData, decodedCipherText, masterPassword)
	if err != nil {
		return nil, err
	}
	return plaintext, nil
}

func DecryptEncryptedField(appData *AppData, key string, masterPassword string, encode bool) (string, error) {
	plaintext, err := DecryptEncryptedFieldBytes(appData, key, masterPassword)
	if err != nil {
		return "", err
	}

	if encode {
		return base64.StdEncoding.EncodeToString(plaintext), nil
	}
	return string(plaintext), nil
}

func DecryptEncryptedFields(appData *AppData, masterPassword string) error {
	for _, key := range encryptedFields {
		if decryptedField, err := DecryptEncryptedField(appData, key, masterPassword, false); err != nil {
			return err
		} else {
			appData.SetString(key, decryptedField)
		}
	}
	return nil
}
