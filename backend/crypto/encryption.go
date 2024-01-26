package crypto

import (
	"crypto/rand"
	"fmt"
	"io"

	"github.com/shirou/gopsutil/v3/host"
	"golang.org/x/crypto/chacha20poly1305"
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

func GenerateNonce(n uint8) []byte {
	nonce := make([]byte, n)
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		// Shouldn't happen
		panic("Error generating nonce: " + err.Error())
	}
	return nonce
}

var ErrInvalidSaltLen = fmt.Errorf("invalid salt length must be %d bytes", HashKeyLen)

// Generate a random 128-bit salt according to NIST SP 800-132
// Uses Argon2id to derive a 256-bit key from the password
func DeriveKey(salt []byte, password string) ([]byte, error) {
	if len(salt) != HashKeyLen {
		return nil, ErrInvalidSaltLen
	}
	// Derive the key using Argon2id
	return GetKey(password, salt), nil
}

func Encrypt(plaintext []byte, key []byte) ([]byte, error) {
	// Nonce (unique for each encryption)
	nonce := GenerateNonce(chacha20poly1305.NonceSizeX)

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

func Decrypt(ciphertext []byte, key []byte) ([]byte, error) {
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
