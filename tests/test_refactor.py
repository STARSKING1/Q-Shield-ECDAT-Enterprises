from q_shield.parsers.refactor import refactor_code

def test_crypto_refactoring():
    source = "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)\n"
    refactored = refactor_code(source)
    assert "ml_kem_keygen" in refactored
