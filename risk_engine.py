import json
import os

def evaluate_quantum_risk(algorithm, key_size=None):
    algo_upper = str(algorithm).upper()
    
    # Asymmetric Cryptography (Shor's Algorithm)
    if any(k in algo_upper for k in ["RSA", "ECC", "ECDSA", "ECDH", "DH"]):
        return "CRITICAL", "Vulnerable to Shor's Algorithm"
    
    # Legacy Hashes
    if any(k in algo_upper for k in ["SHA1", "SHA-1", "MD5"]):
        return "HIGH", "Legacy hash function with high collision/quantum vulnerability"
    
    # Symmetric Cryptography (Grover's Algorithm)
    if "AES" in algo_upper:
        if key_size and int(key_size) < 256:
            return "HIGH", f"AES-{key_size} suffers bit-security halving under Grover's algorithm"
        return "LOW", "AES-256 provides sufficient quantum security margin"
        
    if any(k in algo_upper for k in ["SHA256", "SHA-256", "SHA3"]):
        return "LOW", "Quantum-resistant collision margin"
        
    return "MEDIUM", "Unclassified algorithm"

def mosca_theorem_eval(x=10, y=3, z=7):
    # x: Data Shelf-life (years), y: Migration Time (years), z: Time to CRQC (years)
    in_danger = (x + y) > z
    return {
        "x_shelf_life_years": x,
        "y_migration_time_years": y,
        "z_crqc_arrival_years": z,
        "status": "IN_IMMEDIATE_DANGER" if in_danger else "SAFE",
        "formula": f"{x} + {y} = {x+y} > {z}"
    }

def main():
    if not os.path.exists("cbom.json"):
        print("[!] cbom.json not found. Generating dummy cbom.json for testing...")
        dummy_cbom = {
            "components": [
                {"name": "RSA", "key_size": 2048, "file": "test_crypto.py"},
                {"name": "SHA-1", "file": "test_crypto.py"},
                {"name": "AES", "key_size": 128, "file": "test_crypto.py"}
            ]
        }
        with open("cbom.json", "w") as f:
            json.dump(dummy_cbom, f, indent=2)

    with open("cbom.json", "r") as f:
        cbom_data = json.load(f)

    findings = cbom_data.get("components", cbom_data.get("findings", []))
    enriched_findings = []

    for item in findings:
        algo = item.get("name", item.get("algorithm", "UNKNOWN"))
        key_size = item.get("key_size", None)
        
        risk_level, rationale = evaluate_quantum_risk(algo, key_size)
        
        enriched_item = dict(item)
        enriched_item["quantum_risk_level"] = risk_level
        enriched_item["risk_rationale"] = rationale
        enriched_findings.append(enriched_item)

    report = {
        "project": "Q-Shield ECDAT",
        "module": "Module 3 - Quantum Risk Assessment & Mosca Engine",
        "mosca_assessment": mosca_theorem_eval(x=10, y=3, z=7),
        "risk_summary": {
            "CRITICAL": sum(1 for e in enriched_findings if e["quantum_risk_level"] == "CRITICAL"),
            "HIGH": sum(1 for e in enriched_findings if e["quantum_risk_level"] == "HIGH"),
            "MEDIUM": sum(1 for e in enriched_findings if e["quantum_risk_level"] == "MEDIUM"),
            "LOW": sum(1 for e in enriched_findings if e["quantum_risk_level"] == "LOW"),
        },
        "findings": enriched_findings
    }

    with open("risk_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("=== Q-Shield Module 3: Quantum Risk Assessment Report ===")
    print(f"Mosca Status: {report['mosca_assessment']['status']} ({report['mosca_assessment']['formula']})")
    print(f"Risk Counts: {json.dumps(report['risk_summary'])}")
    print("Full report saved to risk_report.json")

if __name__ == "__main__":
    main()
