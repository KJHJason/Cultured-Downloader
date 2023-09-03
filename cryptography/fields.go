package cryptography

import (
	"encoding/base64"
	"errors"

	"fyne.io/fyne/v2"
	"github.com/KJHJason/Cultured-Downloader/constants"
)
var encryptedFields = [...]string{
	constants.GdriveApiKeyKey,
	constants.GdriveServiceAccKey,

	constants.FantiaCookieValueKey,
}

func ResetEncryptedFields(app fyne.App) {
	if app == nil {
		app = fyne.CurrentApp()
	}

	app.Preferences().SetString(masterKeySalt, "") // reset the salt for the key derivation function
	for _, key := range encryptedFields {
		app.Preferences().SetString(key, "")
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

func ReEncryptEncryptedFields(app fyne.App, oldMasterPassword, newMasterPassword string) error {
	if newMasterPassword == "" {
		return errors.New("new master password cannot be empty")
	}

	if oldMasterPassword == "" || oldMasterPassword == newMasterPassword {
		return nil // no need to re-encrypt
	}

	for _, key := range encryptedFields {
		encodedEncryptedField := app.Preferences().String(key)
		if encodedEncryptedField != "" {
			if reEncryptedField, err := reEncryptEncryptedField(encodedEncryptedField, oldMasterPassword, newMasterPassword); err != nil {
				return err
			} else {
				app.Preferences().SetString(key, reEncryptedField)
			}
		}
	}
	return nil
}

func EncryptPlainField(app fyne.App, key string, plaintext []byte, masterPassword string) error {
	ciphertext, err := EncryptWithPassword(plaintext, masterPassword)
	if err != nil {
		return err
	}

	app.Preferences().SetString(key, base64.StdEncoding.EncodeToString(ciphertext))
	return nil
}

func EncryptPlainFields(app fyne.App, masterPassword string) error {
	for _, key := range encryptedFields {
		plaintext := app.Preferences().String(key)
		if plaintext == "" {
			continue
		}
		if err := EncryptPlainField(app, key, []byte(plaintext), masterPassword); err != nil {
			return err
		}
	}
	return nil
}

func DecryptEncryptedField(app fyne.App, key string, masterPassword string, encode bool) (string, error) {
	encodedEncryptedField := app.Preferences().String(key)
	if encodedEncryptedField == "" {
		return "", nil
	}

	decodedCipherText, err := base64.StdEncoding.DecodeString(encodedEncryptedField)
	if err != nil {
		return "", err
	}

	// decrypt the ciphertext using the master password
	plaintext, err := DecryptWithPassword(decodedCipherText, masterPassword)
	if err != nil {
		return "", err
	}

	if encode {
		return base64.StdEncoding.EncodeToString(plaintext), nil
	}
	return string(plaintext), nil
}

func DecryptEncryptedFields(app fyne.App, masterPassword string) error {
	for _, key := range encryptedFields {
		if decryptedField, err := DecryptEncryptedField(app, key, masterPassword, false); err != nil {
			return err
		} else {
			app.Preferences().SetString(key, decryptedField)
		}
	}
	return nil
}
