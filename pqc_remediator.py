import json
import os

PQC_MAPPING = {
    "RSA": {
        "standard": "NIST FIPS 203 (ML-KEM) / FIPS 204 (ML-DSA)",
        "pqc_pure": "ML-KEM-768 (Encryption) / ML-DSA-65 (Signatures)",
        "hybrid_blueprint": "X25519 + ML-KEM-768",
        "key_size_expansion": "+362% (256 bytes -> 1184 bytes public key)",
        "bandwidth_impact": "Moderate increase in handshake payload"
    },
    "ECC": {
        "standard": "NIST FIPS 203 (ML-KEM) / FIPS 204 (ML-DSA)",
        "pqc_pure": "ML-KEM-768 / ML-DSA-65",
        "hybrid_blueprint": "ECDSA P-256 + ML-DSA-65",
        "key_size_expansion": "+1750% (64 bytes -> 1184 bytes public key)",
        "bandwidth_impact": "High relative increase; minimal absolute latency delta"
    },
    "AES": {
        "standard": "NIST SP 800-38 Series",
        "pqc_pure": "AES-256-GCM",
        "hybrid_blueprint": "Direct Upgrade to AES-256-GCM",
        "key_size_expansion": "+100% (16 bytes -> 32 bytes key size)",
        "bandwidth_impact": "Negligible"
    },
    "SHA-1": {
        "standard": "FIPS 180-4 / FIPS 202",
        "pqc_pure": "SHA-256 or SHA3-256 / SLH-DSA (FIPS 205)",
        "hybrid_blueprint": "SHA-256 Dual Hashing",
        "key_size_expansion": "+60% digest length",
        "bandwidth_impact": "Negligible"
    }
}

def generate_remediation_plan():
    if not os.path.exists("risk_report.json"):
        print("[!] risk_report.json not found. Run risk_engine.py first.")
        return

    with open("risk_report.json", "r") as f:
        risk_data = json.load(f)

    remediation_items = []
    
    for finding in risk_data.get("findings", []):
        algo = finding.get("name", finding.get("algorithm", "UNKNOWN")).upper()
        risk_level = finding.get("quantum_risk_level", "LOW")

        if risk_level in ["CRITICAL", "HIGH"]:
            matched_key = next((k for k in PQC_MAPPING if k in algo), "RSA")
            recommendation = PQC_MAPPING[matched_key]

            remediation_items.append({
                "file": finding.get("file", "unknown"),
                "vulnerable_algorithm": algo,
                "risk_level": risk_level,
                "nist_standard": recommendation["standard"],
                "recommended_pqc": recommendation["pqc_pure"],
                "hybrid_blueprint": recommendation["hybrid_blueprint"],
                "key_expansion_overhead": recommendation["key_size_expansion"],
                "bandwidth_impact": recommendation["bandwidth_impact"]
            })

    plan = {
        "project": "Q-Shield ECDAT",
        "module": "Module 4 - PQC & Hybrid Recommendation Engine",
        "total_migrations_required": len(remediation_items),
        "remediation_roadmap": remediation_items
    }

    with open("remediation_plan.json", "w") as f:
        json.dump(plan, f, indent=2)

    print("=== Q-Shield Module 4: PQC Remediation Plan ===")
    print(f"Total High/Critical Assets Requiring Migration: {len(remediation_items)}")
    for item in remediation_items:
        print(f"[-] Asset ({item['vulnerable_algorithm']}) -> Recommended: {item['hybrid_blueprint']}")
    print("Full plan exported to remediation_plan.json")

if __name__ == "__main__":
    generate_remediation_plan()
