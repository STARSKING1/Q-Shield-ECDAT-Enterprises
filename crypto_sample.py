# Sample Vulnerable Crypto Usage
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib

key = RSA.generate(2048)
cipher = AES.new(b'1234567890123456', AES.MODE_ECB) # AES-128
digest = hashlib.sha1(b"data").hexdigest()
