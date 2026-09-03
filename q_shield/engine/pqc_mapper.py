import json
import os
from typing import Dict, Any, List

# NIST PQC Standard Specifications (FIPS 203, 204, 205)
NIST_PQC_CATALOG = {
    "RSA": {
        "target_standard": "NIST FIPS 203 (ML-KEM)",
        "recommended_scheme": "ML-KEM-768 (Kyber)",
        "hybrid_wrapper": "X25519 + ML-KEM-768",
        "legacy_key_bytes": 256,       # RSA-2048 Public Key (2048 bits = 256 bytes)
        "pqc_pk_bytes": 1184,          # ML-KEM-768 Public Key
        "pqc_ct_bytes": 1088,          # ML-KEM-768 Ciphertext
        "expansion_ratio_pk": 4.625
    },
    "ECDSA": {
        "target_standard": "NIST FIPS 204 (ML-DSA)",
        "recommended_scheme": "ML-DSA-65 (Dilithium)",
        "hybrid_wrapper": "ECDSA P-256 + ML-DSA-65",
        "legacy_key_bytes": 64,        # ECDSA P-256 PubKey
        "pqc_pk_bytes": 1952,          # ML-DSA-65 Public Key
        "pqc_sig_bytes": 3309,         # ML-DSA-65 Signature
        "expansion_ratio_pk": 30.5
    },
    "AES-128": {
        "target_standard": "NIST SP 800-38 Series / Grover Halving Mitigation",
        "recommended_scheme": "AES-256-GCM",
        "hybrid_wrapper": "AES-256-GCM",
        "legacy_key_bytes": 16,
        "pqc_pk_bytes": 32,
        "expansion_ratio_pk": 2.0
    },
    "SHA1": {
        "target_standard": "FIPS 180-4 / FIPS 205 (SLH-DSA)",
        "recommended_scheme": "SHA-256 Dual Hashing / SLH-DSA-SHA2-128s",
        "hybrid_wrapper": "SHA-256 + SLH-DSA",
        "legacy_key_bytes": 20,
        "pqc_pk_bytes": 32,
        "expansion_ratio_pk": 1.6
    }
}

class PQCMapperEngine:
    def generate_remediation_plan(self, cbom_components: List[Dict[str, Any]]) -> Dict[str, Any]:
        remediations = []
        total_legacy_bytes = 0
        total_pqc_bytes = 0

        for comp in cbom_components:
            name = comp.get("name", "").upper()
            matched_key = None
            
            for key in NIST_PQC_CATALOG:
                if key in name:
                    matched_key = key
                    break

            if matched_key:
                specs = NIST_PQC_CATALOG[matched_key]
                leg_bytes = specs["legacy_key_bytes"]
                pqc_bytes = specs["pqc_pk_bytes"]
                
                total_legacy_bytes += leg_bytes
                total_pqc_bytes += pqc_bytes

                remediations.append({
                    "asset_name": name,
                    "location": comp.get("evidence", {}).get("file", "Unknown"),
                    "line": comp.get("evidence", {}).get("line", 0),
                    "nist_standard": specs["target_standard"],
                    "recommended_scheme": specs["recommended_scheme"],
                    "hybrid_wrapper": specs["hybrid_wrapper"],
                    "key_expansion": {
                        "legacy_pk_bytes": leg_bytes,
                        "pqc_pk_bytes": pqc_bytes,
                        "overhead_multiplier": f"{specs['expansion_ratio_pk']}x"
                    }
                })

        overall_expansion = (total_pqc_bytes / total_legacy_bytes) if total_legacy_bytes > 0 else 1.0

        plan = {
            "title": "NIST FIPS 203/204/205 PQC Remediation & Key Expansion Plan",
            "total_flagged_assets": len(remediations),
            "aggregate_key_memory_overhead": {
                "total_legacy_key_bytes": total_legacy_bytes,
                "total_pqc_key_bytes": total_pqc_bytes,
                "overall_overhead_multiplier": f"{round(overall_expansion, 2)}x"
            },
            "remediations": remediations
        }

        with open("remediation_plan.json", "w") as f:
            json.dump(plan, f, indent=2)

        return plan

def run_pqc_mapping():
    cbom_components = []
    if os.path.exists("cbom.json"):
        try:
            with open("cbom.json", "r") as f:
                cbom_components = json.load(f).get("components", [])
        except Exception:
            pass

    engine = PQCMapperEngine()
    return engine.generate_remediation_plan(cbom_components)

if __name__ == "__main__":
    plan = run_pqc_mapping()
    print(f"[+] PQC Mapping Complete. Remediated {plan['total_flagged_assets']} assets.")
    print(f"[+] Aggregate Key Memory Overhead: {plan['aggregate_key_memory_overhead']['overall_overhead_multiplier']}")
