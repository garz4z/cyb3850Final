# crypto_service.py
from __future__ import annotations
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


class CryptoService:
    def __init__(self, iterations: int = 200_000, key_len: int = 32):
        """
        iterations: PBKDF2 iteration count
        key_len: length of derived key in bytes (32 = 256-bit AES)
        """
        self.iterations = iterations
        self.key_len = key_len

    def derive_key(self, master_password: str, salt: bytes, iterations: int | None = None) -> bytes:
        """Derive a key from a master password and salt using PBKDF2-HMAC-SHA256."""
        if iterations is None:
            iterations = self.iterations
        key = PBKDF2(master_password, salt, dkLen=self.key_len, count=iterations)
        return key

    def encrypt(self, plaintext: str, key: bytes) -> tuple[bytes, bytes, bytes]:
        """Encrypt plaintext with AES-256-GCM. Returns (nonce, ciphertext, tag)."""
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
        return cipher.nonce, ciphertext, tag

    def decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes) -> str:
        """Decrypt AES-256-GCM (nonce, ciphertext, tag). Returns plaintext string."""
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")
