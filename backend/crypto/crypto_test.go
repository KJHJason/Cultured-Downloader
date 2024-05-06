package crypto

import (
	"testing"
)

func TestEncryption(t *testing.T) {
	key         := GenerateNonce(32)
	dummyData   := []byte("dummy data")

	// Test encryption
	encryptedData, err := Encrypt(dummyData, key)
	if err != nil {
		t.Errorf("Error in encryption: %v", err)
	}

	decryptedData, err := Decrypt(encryptedData, key)
	if err != nil {
		t.Errorf("Error in decryption: %v", err)
	}

	if string(decryptedData) != string(dummyData) {
		t.Errorf("Decrypted data does not match original data")
	}
}
