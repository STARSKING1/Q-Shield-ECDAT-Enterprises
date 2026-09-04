from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_legacy_keys():
    # RSA 2048-bit key generation (Quantum Vulnerable)
    rsa_key = RSA.generate(2048)
    
    # Cryptography library RSA pattern
    hazmat_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return rsa_key, hazmat_key
