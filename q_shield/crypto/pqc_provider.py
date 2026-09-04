import os
import base64
from typing import Dict, Any

try:
    import oqs
    HAS_LIBOQS = True
except ImportError:
    HAS_LIBOQS = False


class QuantumSafeProvider:
    @staticmethod
    def generate_mlkem_keypair(variant: str = "ML-KEM-768") -> Dict[str, Any]:
        if HAS_LIBOQS:
            with oqs.KeyEncapsulation(variant) as kem:
                public_key = kem.generate_keypair()
                secret_key = kem.export_secret_key()
                return {
                    "mechanism": variant,
                    "standard": "NIST FIPS 203",
                    "public_key_bytes": len(public_key),
                    "public_key_b64": base64.b64encode(public_key).decode("utf-8"),
                    "secret_key_bytes": len(secret_key),
                }
        
        simulated_pk = os.urandom(1184)
        return {
            "mechanism": f"{variant}-SIMULATED",
            "standard": "NIST FIPS 203 (Fallback)",
            "public_key_bytes": len(simulated_pk),
            "public_key_b64": base64.b64encode(simulated_pk).decode("utf-8"),
        }

    @staticmethod
    def generate_mldsa_keypair(variant: str = "ML-DSA-65") -> Dict[str, Any]:
        if HAS_LIBOQS:
            with oqs.Signature(variant) as sig:
                public_key = sig.generate_keypair()
                secret_key = sig.export_secret_key()
                return {
                    "mechanism": variant,
                    "standard": "NIST FIPS 204",
                    "public_key_bytes": len(public_key),
                    "public_key_b64": base64.b64encode(public_key).decode("utf-8"),
                    "secret_key_bytes": len(secret_key),
                }

        simulated_pk = os.urandom(1952)
        return {
            "mechanism": f"{variant}-SIMULATED",
            "standard": "NIST FIPS 204 (Fallback)",
            "public_key_bytes": len(simulated_pk),
            "public_key_b64": base64.b64encode(simulated_pk).decode("utf-8"),
        }
