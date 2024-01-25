package cryptography

import (
	"encoding/base64"
	"errors"

	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
)
var encryptedFields = [...]string{
	constants.GdriveApiKeyKey,
	constants.GdriveServiceAccKey,

	constants.FantiaCookieValueKey,
}

func ResetEncryptedFields(appData *appdata.AppData) {
	appData.SetString(masterKeySalt, "") // reset the salt for the key derivation function
	for _, key := range encryptedFields {
		appData.SetString(key, "")
	}
}

func reEncryptEncryptedField(encodedCiphertext string, oldMasterPassword, newMasterPassword string) (string, error) {
	decodedCipherText, err := base64.StdEncoding.DecodeString(encodedCiphertext)
	if err != nil {
		return "", err
	}

	// decrypt the ciphertext using the old master password
	plaintext, err := DecryptWithPassword(decodedCipherText, oldMasterPassword)
	if err != nil {
		return "", err
	}

	// encrypt the plaintext using the new master password
	ciphertext, err := EncryptWithPassword(plaintext, newMasterPassword)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func ReEncryptEncryptedFields(appData *appdata.AppData, oldMasterPassword, newMasterPassword string) error {
	if newMasterPassword == "" {
		return errors.New("new master password cannot be empty")
	}

	if oldMasterPassword == "" || oldMasterPassword == newMasterPassword {
		return nil // no need to re-encrypt
	}

	for _, key := range encryptedFields {
		encodedEncryptedField := appData.GetString(key)
		if encodedEncryptedField != "" {
			if reEncryptedField, err := reEncryptEncryptedField(encodedEncryptedField, oldMasterPassword, newMasterPassword); err != nil {
				return err
			} else {
				appData.SetString(key, reEncryptedField)
			}
		}
	}
	return nil
}

func EncryptPlainField(appData *appdata.AppData, key string, plaintext []byte, masterPassword string) error {
	ciphertext, err := EncryptWithPassword(plaintext, masterPassword)
	if err != nil {
		return err
	}

	appData.SetString(key, base64.StdEncoding.EncodeToString(ciphertext))
	return nil
}

func EncryptPlainFields(appData *appdata.AppData, masterPassword string) error {
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

func DecryptEncryptedFieldBytes(appData *appdata.AppData, key string, masterPassword string) ([]byte, error) {
	encodedEncryptedField := appData.GetString(key)
	if encodedEncryptedField == "" {
		return nil, nil
	}

	decodedCipherText, err := base64.StdEncoding.DecodeString(encodedEncryptedField)
	if err != nil {
		return nil, err
	}

	// decrypt the ciphertext using the master password
	plaintext, err := DecryptWithPassword(decodedCipherText, masterPassword)
	if err != nil {
		return nil, err
	}
	return plaintext, nil
}

func DecryptEncryptedField(appData *appdata.AppData, key string, masterPassword string, encode bool) (string, error) {
	plaintext, err := DecryptEncryptedFieldBytes(appData, key, masterPassword)
	if err != nil {
		return "", err
	}

	if encode {
		return base64.StdEncoding.EncodeToString(plaintext), nil
	}
	return string(plaintext), nil
}

func DecryptEncryptedFields(appData *appdata.AppData, masterPassword string) error {
	for _, key := range encryptedFields {
		if decryptedField, err := DecryptEncryptedField(appData, key, masterPassword, false); err != nil {
			return err
		} else {
			appData.SetString(key, decryptedField)
		}
	}
	return nil
}
