import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_legacy_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key

def hash_data(data):
    return hashlib.sha1(data).hexdigest()

def encrypt_aes(key, iv, plaintext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()
