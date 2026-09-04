import time
from celery import Celery
from q_shield.engine.mosca import evaluate_mosca_risk
from q_shield.parsers.cst_remediator import remediate_code
from q_shield.db.session import SessionLocal
from q_shield.db.models import ScanSession, CBOMAsset, RiskSnapshot

REDIS_URL = "redis://localhost:6379/0"
celery_app = Celery("q_shield_tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(name="execute_deep_ast_scan")
def execute_deep_ast_scan(scan_id: int, file_paths: list[str]):
    """Asynchronously parses python files, updates CBOM, and computes risk metrics."""
    db: SessionLocal = SessionLocal()
    try:
        scan = db.query(ScanSession).filter(ScanSession.id == scan_id).first()
        if not scan:
            return {"status": "FAILED", "reason": "Scan ID not found"}

        scan.status = "IN_PROGRESS"
        db.commit()

        vulnerable_count = 0
        for path in file_paths:
            try:
                with open(path, "r") as f:
                    content = f.read()
                _, changes = remediate_code(content)
                if changes > 0:
                    vulnerable_count += 1
                    asset = CBOMAsset(
                        scan_id=scan.id,
                        asset_name=path,
                        asset_type="Source Code",
                        discovered_primitive="RSA-2048 / Legacy Crypto",
                        pqc_target_standard="ML-KEM-768 (FIPS 203)",
                        severity="CRITICAL",
                        source_location=path
                    )
                    db.add(asset)
            except Exception:
                continue

        # Compute risk snapshot
        risk_result = evaluate_mosca_risk(x=10, y=3, z=7, primitive="RSA-2048" if vulnerable_count > 0 else "AES-256")
        snapshot = RiskSnapshot(
            scan_id=scan.id,
            qvi_score=risk_result["qvi_score"],
            urgency=risk_result["urgency"],
            mosca_x=10, mosca_y=3, mosca_z=7
        )
        db.add(snapshot)

        scan.status = "COMPLETED"
        db.commit()
        return {"status": "SUCCESS", "vulnerabilities_found": vulnerable_count}

    except Exception as exc:
        db.rollback()
        if scan:
            scan.status = "FAILED"
            db.commit()
        raise exc
    finally:
        db.close()
