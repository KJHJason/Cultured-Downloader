package appdata

import (
	"encoding/base64"
	"errors"

	"github.com/KJHJason/Cultured-Downloader/backend/constants"
	"github.com/KJHJason/Cultured-Downloader/backend/crypto"
)

// IMPORTANT: Update this when adding new encrypted fields
var encryptedFields = []string{
	constants.GDRIVE_API_KEY_KEY,
	constants.GDRIVE_SERVICE_ACC_KEY,

	constants.FANTIA_COOKIE_JSON_KEY,
	constants.FANTIA_COOKIE_TXT_KEY,
	constants.FANTIA_COOKIE_VALUE_KEY,

	constants.PIXIV_FANBOX_COOKIE_JSON_KEY,
	constants.PIXIV_FANBOX_COOKIE_TXT_KEY,
	constants.PIXIV_FANBOX_COOKIE_VALUE_KEY,

	constants.PIXIV_COOKIE_JSON_KEY,
	constants.PIXIV_COOKIE_TXT_KEY,
	constants.PIXIV_COOKIE_VALUE_KEY,
	constants.PIXIV_MOBILE_REFRESH_TOKEN_KEY,

	constants.KEMONO_COOKIE_JSON_KEY,
	constants.KEMONO_COOKIE_TXT_KEY,
	constants.KEMONO_COOKIE_VALUE_KEY,
}

func (a *AppData) ResetEncryptedFields() error {
	return a.Unset(encryptedFields...)
}

func (a *AppData) EncryptWithPassword(plaintext, salt []byte, password string) ([]byte, error) {
	key, err := crypto.DeriveKey(password, salt)
	if err != nil {
		return nil, err
	}
	return crypto.Encrypt(plaintext, key)
}

func (a *AppData) DecryptWithPassword(ciphertext, salt []byte, password string) ([]byte, error) {
	key, err := crypto.DeriveKey(password, salt)
	if err != nil {
		return nil, err
	}
	return crypto.Decrypt(ciphertext, key)
}

func (a *AppData) reEncryptEncryptedField(encodedCiphertext string, oldMasterPassword string, oldMasterPasswordSalt []byte) (string, error) {
	decodedCipherText, err := base64.StdEncoding.DecodeString(encodedCiphertext)
	if err != nil {
		return "", err
	}

	// decrypt the ciphertext using the old master password
	plaintext, err := a.DecryptWithPassword(decodedCipherText, oldMasterPasswordSalt, oldMasterPassword)
	if err != nil {
		return "", err
	}

	// encrypt the plaintext using the new master password
	ciphertext, err := a.EncryptWithPassword(plaintext, a.masterPasswordSalt, a.masterPassword)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func (a *AppData) VerifyMasterPassword(password string) bool {
	hashOfMasterPasswordHash, masterPasswordSalt := a.GetMasterPasswordHash()
	hashedPassword := crypto.HashStringWithSalt(password, masterPasswordSalt)
	if !crypto.VerifyBytes(hashedPassword, hashOfMasterPasswordHash) {
		return false
	}
	if a.masterPassword == "" {
		a.SetMasterPasswordInMem(password)
	}
	return true
}

func (a *AppData) ChangeMasterPassword(oldMasterPassword, newMasterPassword string) error {
	if newMasterPassword == "" {
		return errors.New("new master password cannot be empty")
	}

	if oldMasterPassword == newMasterPassword {
		return nil // no need to re-encrypt
	}

	if oldMasterPassword == "" {
		// Note: not changing master password
		err := a.changeMasterPassword(newMasterPassword)
		if err != nil {
			return err
		}

		return a.EncryptPlainFields(newMasterPassword)
	} else if !a.VerifyMasterPassword(oldMasterPassword) {
		return errors.New("old master password is incorrect")
	}

	// User has an old master password, changing it below
	oldMasterPasswordSalt := a.masterPasswordSalt
	err := a.changeMasterPassword(newMasterPassword)
	if err != nil {
		return err
	}

	for _, key := range encryptedFields {
		encodedEncryptedField := a.GetString(key)
		if encodedEncryptedField != "" {
			reEncryptedField, err := a.reEncryptEncryptedField(
				encodedEncryptedField,
				oldMasterPassword,
				oldMasterPasswordSalt,
			)
			if err != nil {
				return err
			} else {
				a.SetString(key, reEncryptedField)
			}
		}
	}
	return nil
}

func (a *AppData) EncryptPlainFields(masterPassword string) error {
	for _, key := range encryptedFields {
		if err := a.ChangeToSecure(key); err != nil {
			return err
		}
	}
	return nil
}

func (a *AppData) DecryptEncryptedFields(masterPassword string) error {
	for _, key := range encryptedFields {
		if err := a.ChangeToPlaintext(key); err != nil {
			return err
		}
	}
	return nil
}
