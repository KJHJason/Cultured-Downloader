package cryptography

import (
	"crypto/rand"
	"encoding/base64"
	"io"
	"sync"

	"github.com/shirou/gopsutil/v3/host"
	"golang.org/x/crypto/chacha20poly1305"
	"github.com/KJHJason/Cultured-Downloader/backend/appdata"
)

const (
	// Preferences key
	masterKeySalt = "masterkey-salt"
)

// reset the salt for the key derivation function
func ResetMasterKeySalt(appData *appdata.AppData) {
	appData.SetString(masterKeySalt, "")
}

var tag []byte
func init() {
	// use the user's desktop name as the tag
	hostId, err := host.HostID()
	if err != nil {
		hostId = "cultured.downloader"
	}
	tag = []byte(hostId)
}

func generateNonce(n uint8) []byte {
	nonce := make([]byte, n)
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		// Shouldn't happen
		panic("Error generating nonce: " + err.Error())
	}
	return nonce
}

var dkMutex sync.Mutex

// Uses Argon2id to derive a 256-bit key from the password
func deriveKey(appData *appdata.AppData, password string) ([]byte, error) {
	dkMutex.Lock()
	defer dkMutex.Unlock()

	var salt []byte
	var err error
	if appData.GetString(masterKeySalt) == "" {
		salt = generateNonce(hashKeyLen) // Generate a random 128-bit salt according to NIST SP 800-132
		appData.SetString(masterKeySalt, base64.StdEncoding.EncodeToString(salt))
	} else {
		salt, err = base64.StdEncoding.DecodeString(appData.GetString(masterKeySalt))
		if err != nil || len(salt) != hashKeyLen {
			// Shouldn't happen unless the user has tampered with the preferences file,
			// in which case we should just panic after resetting the salt and the encrypted fields
			appData.SetString(masterKeySalt, base64.StdEncoding.EncodeToString(generateNonce(hashKeyLen)))
			ResetEncryptedFields(appData)
			return nil, err
		}
	}

	// Derive the key using Argon2id
	return GetKey(password, salt), nil
}

func encrypt(plaintext []byte, key []byte) ([]byte, error) {
	// Nonce (unique for each encryption)
	nonce := generateNonce(chacha20poly1305.NonceSizeX)

	// Create a XChaCha20-Poly1305 AEAD cipher
	aead, err := chacha20poly1305.NewX(key)
	if err != nil {
		return nil, err
	}

	// Encrypt the plaintext
	ciphertext := aead.Seal(nil, nonce, plaintext, tag)

	// Return the ciphertext with the nonce prepended for decryption later
	return append(nonce, ciphertext...), nil
}

func EncryptWithPassword(appData *appdata.AppData, plaintext []byte, password string) ([]byte, error) {
	key, err := deriveKey(appData, password)
	if err != nil {
		return nil, err
	}
	return encrypt(plaintext, key)
}

func decrypt(ciphertext []byte, key []byte) ([]byte, error) {
	// Create a XChaCha20-Poly1305 AEAD cipher
	aead, err := chacha20poly1305.NewX(key)
	if err != nil {
		return nil, err
	}

	// Split nonce and ciphertext
	nonce := ciphertext[:chacha20poly1305.NonceSizeX]
	ciphertext = ciphertext[chacha20poly1305.NonceSizeX:]

	// Decrypt the ciphertext
	plaintext, err := aead.Open(nil, nonce, ciphertext, tag)
	if err != nil {
		return nil, err
	}

	return plaintext, nil
}

func DecryptWithPassword(appData *appdata.AppData, ciphertext []byte, password string) ([]byte, error) {
	key, err := deriveKey(appData, password)
	if err != nil {
		return nil, err
	}
	return decrypt(ciphertext, key)
}
