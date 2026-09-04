import json
import os
from datetime import datetime

from q_shield.engine.mosca import evaluate_mosca_risk, MoscaAssessment
from q_shield.parsers.cst_remediator import remediate_code
from q_shield.db.session import init_db, SessionLocal
from q_shield.db.models import ScanSession, RiskSnapshot, CBOMAsset

def run_pipeline():
    print("==================================================")
    print("   Q-Shield ECDAT Enterprise Pipeline Execution   ")
    print("==================================================")

    # 1. Initialize Database Schema
    init_db()
    db = SessionLocal()

    # Create new ScanSession record
    current_scan = ScanSession(
        target_project="Q-Shield ECDAT Core Repository",
        status="IN_PROGRESS"
    )
    db.add(current_scan)
    db.commit()
    db.refresh(current_scan)
    print(f"[*] Created Database Scan Session ID: #{current_scan.id}")

    # 2. Execute Mosca Risk Evaluation
    mosca_engine = MoscaAssessment(x=10.0, y=5.0, z=8.0, primitive="RSA-2048")
    risk_data = mosca_engine.evaluate()
    print(f"[*] Mosca Inequality Metric: {risk_data['mosca_inequality']}")
    print(f"[*] QVI Score: {risk_data['qvi_score']} | Urgency: {risk_data['urgency']}")

    # Save Risk Snapshot to Database
    risk_snapshot = RiskSnapshot(
        scan_id=current_scan.id,
        qvi_score=risk_data['qvi_score'],
        urgency=risk_data['urgency'],
        mosca_x=10,
        mosca_y=5,
        mosca_z=8
    )
    db.add(risk_snapshot)

    # 3. Perform LibCST Remediation Check
    sample_code = """# Legacy Cryptographic Operations
from Crypto.PublicKey import RSA

def init_security():
    key = RSA.generate(2048)
    return key
"""
    remediated_code, transformations = remediate_code(sample_code)
    print(f"[*] LibCST Transformations Applied: {transformations}")

    # 4. Generate CBOM Component and Persist to DB
    if transformations > 0:
        asset = CBOMAsset(
            scan_id=current_scan.id,
            asset_name="q_shield/crypto_legacy.py",
            asset_type="Source Code",
            discovered_primitive="RSA-2048 / PyCryptodome",
            pqc_target_standard="ML-KEM-768 / FIPS 203",
            severity="CRITICAL",
            source_location="q_shield/crypto_legacy.py:line 2",
            raw_metadata={"original_import": "Crypto.PublicKey.RSA"}
        )
        db.add(asset)

        # Generate Legacy cbom.json for backwards compatibility
        cbom_data = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "serialNumber": f"urn:uuid:qshield-scan-{current_scan.id}",
            "components": [
                {
                    "name": asset.asset_name,
                    "type": asset.asset_type,
                    "discovered_primitive": asset.discovered_primitive,
                    "pqc_target_standard": asset.pqc_target_standard,
                    "severity": asset.severity,
                    "source_location": asset.source_location
                }
            ]
        }
        with open("cbom.json", "w") as f:
            json.dump(cbom_data, f, indent=2)

    # Finalize Scan Status in DB
    current_scan.status = "COMPLETED"
    db.commit()
    db.close()
    print("[*] Pipeline execution completed. Scan session persisted to SQLite database.")

if __name__ == "__main__":
    run_pipeline()
