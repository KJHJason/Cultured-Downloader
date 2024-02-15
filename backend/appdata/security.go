package appdata

import (
	"errors"
	"encoding/base64"
	"sync"

	"github.com/KJHJason/Cultured-Downloader/backend/crypto"
	"github.com/KJHJason/Cultured-Downloader/backend/constants"
)

var dkMutex sync.Mutex
// Uses Argon2id to derive a 256-bit key from the password
func (a *AppData) deriveKey(password string) ([]byte, error) {
	dkMutex.Lock()
	defer dkMutex.Unlock()

	salt := a.masterPasswordSalt
	if (salt == nil) {
		a.unset(constants.MasterPasswordSaltKey)
		panic("master password salt is nil") // should never happen
	}

	// Derive the key using Argon2id
	return crypto.GetKey(password, salt), nil
}

var encryptedFields = [...]string{
	constants.GdriveApiKeyKey,
	constants.GdriveServiceAccKey,

	constants.FantiaCookieValueKey,
}

func (a *AppData) ResetEncryptedFields() error {
	var err error
	for _, key := range encryptedFields {
		err = a.Unset(key)
		if err != nil {
			return err
		}
	}
	return nil
}

func (a *AppData) EncryptWithPassword(plaintext, salt []byte, password string) ([]byte, error) {
	key, err := a.deriveKey(password)
	if err != nil {
		return nil, err
	}
	return crypto.Encrypt(plaintext, key)
}

func (a *AppData) DecryptWithPassword(ciphertext, salt []byte, password string) ([]byte, error) {
	key, err := a.deriveKey(password)
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
		a.changeMasterPassword(newMasterPassword)
		return a.EncryptPlainFields(newMasterPassword)
	} else if !a.VerifyMasterPassword(oldMasterPassword) {
		return errors.New("old master password is incorrect")
	}

	oldMasterPasswordSalt := a.masterPasswordSalt
	a.changeMasterPassword(newMasterPassword)
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
