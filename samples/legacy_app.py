import hmac
from Crypto.Cipher import AES
from Crypto.Hash import SHA1

def insecure_hash_and_cipher(key: bytes, data: bytes):
    # Using weak/legacy primitives
    hasher = SHA1.new(data)
    cipher = AES.new(key, AES.MODE_ECB)
    return hasher.digest(), cipher.encrypt(data)
