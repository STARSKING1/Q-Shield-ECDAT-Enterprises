import rsa

def generate_rsa_keys():
    (pubKey, privKey) = rsa.newkeys(1024)
    return pubKey, privKey
