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
)

func HashPassword(password string) []byte {
	salt := generateNonce(hashSaltLen)
	hash := argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, hashKeyLen)
	return append(salt, hash...) // prepend salt to hash
}

func VerifyPassword(password string, hash []byte) bool {
	salt := hash[:hashSaltLen]
	hash = hash[hashSaltLen:]
	return bytes.Equal(hash, argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, hashKeyLen))
}
