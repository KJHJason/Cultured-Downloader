package crypto

import (
	"bytes"

	"golang.org/x/crypto/argon2"
)

const (
	timeCost	= 4
	memoryCost	= 64 * 1024
	parallelism	= 4
	HashSaltLen = 64
	HashKeyLen  = 64 // 128-bit salt according to NIST SP 800-132
	kdfKeyLen   = 32
)

func HashPassword(password string) []byte {
	salt := GenerateNonce(HashSaltLen)
	hash := argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, HashKeyLen)
	return append(salt, hash...) // prepend salt to hash
}

// GetKey returns a 32-bytes key derived from the password and salt using Argon2id
func GetKey(password string, salt []byte) []byte {
	return argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, kdfKeyLen)
}

func VerifyPassword(password string, hash []byte) bool {
	salt := hash[:HashSaltLen]
	hash = hash[HashSaltLen:]
	return bytes.Equal(hash, argon2.IDKey([]byte(password), salt, timeCost, memoryCost, parallelism, uint32(len(hash))))
}