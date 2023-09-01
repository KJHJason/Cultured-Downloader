package main

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"io"

	"fyne.io/fyne/v2"
	"golang.org/x/crypto/pbkdf2"
	"golang.org/x/crypto/chacha20poly1305"
	"github.com/shirou/gopsutil/v3/host"
)

const (
	// see https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf
	// for the reasonings behind the values used here
	saltLength = 16 // (in bytes)
	iterations = 1000 // higher values increase security but also slow down key derivation
	keyLength  = 32 // (in bytes)

	// Preferences key
	masterKeySalt = "masterkey-salt"
)

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

// Uses PBKDF2 to derive a 256-bit key from the password
func deriveKey(password string) []byte {
	var salt []byte
	var err error
	app := fyne.CurrentApp()
	if app.Preferences().String(masterKeySalt) == "" {
		salt = generateNonce(saltLength) // Generate a random 128-bit salt according to NIST SP 800-132
		app.Preferences().SetString(masterKeySalt, hex.EncodeToString(generateNonce(saltLength)))
	} else {
		salt, err = hex.DecodeString(app.Preferences().String(masterKeySalt))
		if err != nil {
			// Shouldn't happen unless the user has tampered with the preferences file,
			// in which case we should just panic after resetting the salt
			app.Preferences().SetString(masterKeySalt, hex.EncodeToString(generateNonce(saltLength)))
			panic(err)
		}
	}

	// Derive the key using PBKDF2 with HMAC-SHA256
	return pbkdf2.Key([]byte(password), salt, iterations, keyLength, sha256.New)
}

func encrypt(plaintext []byte, key []byte) ([]byte, error) {
	// Nonce (unique for each encryption)
	nonce := generateNonce(chacha20poly1305.NonceSize)

	// Create a ChaCha20-Poly1305 AEAD cipher
	aead, err := chacha20poly1305.New(key)
	if err != nil {
		return nil, err
	}

	// Encrypt the plaintext
	ciphertext := aead.Seal(nil, nonce, plaintext, tag)

	// Return the ciphertext with the nonce prepended for decryption later
	return append(nonce, ciphertext...), nil
}

func encryptWithPassword(plaintext []byte, password string) ([]byte, error) {
	key := deriveKey(password)
	return encrypt(plaintext, key)
}

func decrypt(ciphertext []byte, key []byte) ([]byte, error) {
	// Create a ChaCha20-Poly1305 AEAD cipher
	aead, err := chacha20poly1305.New(key)
	if err != nil {
		return nil, err
	}

	// Split nonce and ciphertext
	nonce := ciphertext[:chacha20poly1305.NonceSize]
	ciphertext = ciphertext[chacha20poly1305.NonceSize:]

	// Decrypt the ciphertext
	plaintext, err := aead.Open(nil, nonce, ciphertext, tag)
	if err != nil {
		return nil, err
	}

	return plaintext, nil
}

func decryptWithPassword(ciphertext []byte, password string) ([]byte, error) {
	key := deriveKey(password)
	return decrypt(ciphertext, key)
}
