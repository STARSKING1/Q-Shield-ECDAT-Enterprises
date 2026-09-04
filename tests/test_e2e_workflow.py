import pytest
from fastapi.testclient import TestClient
from q_shield.api.main import app

client = TestClient(app)

def test_full_q_shield_lifecycle():
    # 1. Verify health
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    # 2. Execute cryptographic scan
    scan_payload = {
        "path": "vulnerable_sample.py",
        "shelf_life": 10,
        "migration_time": 3,
        "quantum_horizon": 7
    }
    scan_res = client.post("/scan", json=scan_payload)
    assert scan_res.status_code == 200
    scan_data = scan_res.json()
    assert "qvi_score" in scan_data
    assert scan_data["qvi_score"] == 60.0

    # 3. Generate CycloneDX CBOM report
    cbom_res = client.post("/report/cbom", json=scan_payload)
    assert cbom_res.status_code == 200
    cbom_data = cbom_res.json()
    assert cbom_data["bomFormat"] == "CycloneDX"

    # 4. Generate SARIF report
    sarif_res = client.post("/report/sarif", json=scan_payload)
    assert sarif_res.status_code == 200
    sarif_data = sarif_res.json()
    assert sarif_data["version"] == "2.1.0"

    # 5. Execute AST Refactoring
    refactor_payload = {"code": "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"}
    ref_res = client.post("/refactor", json=refactor_payload)
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    assert "ml_kem_keygen" in ref_data["refactored"]
