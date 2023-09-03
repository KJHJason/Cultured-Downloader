package cryptography

import (
	"bytes"

	"golang.org/x/crypto/argon2"
)

const (
	timeCost	= 4
	memoryCost	= 64 * 1024
	parallelism	= 4
	hashSaltLen = 64
	hashKeyLen  = 64
	kdfKeyLen   = 32
)

func HashPassword(password string) []byte {
	salt := generateNonce(hashSaltLen)
	hash := argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, hashKeyLen)
	return append(salt, hash...) // prepend salt to hash
}

// GetKey returns a 32-bytes key derived from the password and salt
func GetKey(password string, salt []byte) []byte {
	return argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, kdfKeyLen)
}

func VerifyPassword(password string, hash []byte) bool {
	salt := hash[:hashSaltLen]
	hash = hash[hashSaltLen:]
	return bytes.Equal(hash, argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, uint32(len(hash))))
}
