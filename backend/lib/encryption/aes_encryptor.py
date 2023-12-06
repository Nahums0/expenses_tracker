from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def get_cipher(iv=None):
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        raise ValueError("Environment variable 'ENCRYPTION_KEY' not found")

    # Ensure the key is in bytes
    key = key.encode() if isinstance(key, str) else key
    if iv is None:
        cipher = AES.new(key, AES.MODE_CBC)
    else:
        # Ensure the IV is in bytes
        iv = iv.encode() if isinstance(iv, str) else iv
        cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher

def encrypt(data):
    if not data:
        raise ValueError("No data provided for encryption")

    data = data.encode() if isinstance(data, str) else data
    try:
        cipher = get_cipher()
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = cipher.iv
        return iv + ct_bytes
    except Exception as e:
        raise Exception(f"Encryption error: {e}")

def decrypt(encrypted_data):
    encrypted_data = encrypted_data.encode() if isinstance(encrypted_data, str) else encrypted_data

    if not encrypted_data or len(encrypted_data) < 16:
        raise ValueError("Invalid encrypted data")

    try:
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        cipher = get_cipher(iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    except ValueError as e:
        raise ValueError(f"Decryption error: {e}")
