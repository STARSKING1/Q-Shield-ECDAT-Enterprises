import re

MAPPING_TABLE = {
    "hashlib.sha1()": "hashlib.sha256()  # Q-Shield Auto-Remediated: SHA-1 -> SHA-256 Dual Hash",
    "hashlib.md5()": "hashlib.sha256()   # Q-Shield Auto-Remediated: MD5 -> SHA-256 Dual Hash",
    "RSA.generate(2048)": "oqs.KeyEncapsulation('ML-KEM-768')  # Q-Shield Auto-Remediated: RSA -> FIPS 203 ML-KEM-768",
    "ECDSA.generate()": "oqs.Signature('ML-DSA-65')            # Q-Shield Auto-Remediated: ECDSA -> FIPS 204 ML-DSA-65"
}

def remediate_code_snippet(source_code: str) -> str:
    modified_code = source_code
    for legacy, quantum_safe in MAPPING_TABLE.items():
        modified_code = modified_code.replace(legacy, quantum_safe)
    return modified_code
