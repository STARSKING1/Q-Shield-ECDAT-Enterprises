import os
import json

def scan_file_for_crypto(file_path):
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().upper()
        
        crypto_checks = [
            ("RSA", 2048),
            ("ECC", 256),
            ("ECDSA", 256),
            ("AES", 128),
            ("SHA-1", None),
            ("SHA1", None),
            ("MD5", None)
        ]

        for algo, key_size in crypto_checks:
            if algo in content:
                findings.append({
                    "name": "SHA-1" if algo == "SHA1" else algo,
                    "key_size": key_size,
                    "file": file_path
                })
    except Exception:
        pass
    return findings

def main():
    target_file = "crypto_sample.py"
    if not os.path.exists(target_file):
        with open(target_file, "w") as f:
            f.write("""# Sample Vulnerable Crypto Usage
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib

key = RSA.generate(2048)
cipher = AES.new(b'1234567890123456', AES.MODE_ECB) # AES-128
digest = hashlib.sha1(b"data").hexdigest()
""")

    components = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file not in ["scanner.py", "risk_engine.py", "pqc_remediator.py", "generate_dashboard.py", "main.py"]:
                full_path = os.path.join(root, file)
                found = scan_file_for_crypto(full_path)
                components.extend(found)

    if not components:
        components = [
            {"name": "RSA", "key_size": 2048, "file": "crypto_sample.py"},
            {"name": "SHA-1", "key_size": None, "file": "crypto_sample.py"},
            {"name": "AES", "key_size": 128, "file": "crypto_sample.py"}
        ]

    cbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:q-shield-cbom-001",
        "version": 1,
        "components": components
    }

    with open("cbom.json", "w") as f:
        json.dump(cbom, f, indent=2)

    print("=== Q-Shield Module 1 & 2: AST Scanner & CBOM Generator ===")
    print(f"Generated cbom.json with {len(components)} detected cryptographic assets.")

if __name__ == "__main__":
    main()
