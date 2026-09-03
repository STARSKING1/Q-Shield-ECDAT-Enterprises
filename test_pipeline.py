import os
import json
from fastapi.testclient import TestClient
from q_shield.api.app import app, API_KEY
from q_shield.parsers.cst_remediator import remediate_code_string

client = TestClient(app)

def test_full_solution():
    print("[1/3] Verifying Generated Pipeline Artifacts...")
    assert os.path.exists("cbom.json"), "cbom.json missing"
    assert os.path.exists("risk_report.json"), "risk_report.json missing"
    assert os.path.exists("remediation_plan.json"), "remediation_plan.json missing"
    assert os.path.exists("dashboard.html"), "dashboard.html missing"
    print("      └── Artifact Integrity PASSED.")

    print("[2/3] Testing LibCST Automated Remediator Engine...")
    legacy_snippet = "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"
    res = remediate_code_string(legacy_snippet)
    assert res["success"] is True, "CST Remediation failed"
    assert "HybridMLKEM768" in res["remediated_code"], "Transformation failed"
    print("      └── LibCST Auto-Remediation PASSED.")

    print("[3/3] Testing Secured FastAPI REST Endpoints...")
    # Health check (unauthenticated)
    h = client.get("/health")
    assert h.status_code == 200, "Health check failed"
    assert h.json()["security_enabled"] is True

    # Test unauthorized access (should return 401)
    unauth = client.get("/api/v1/cbom")
    assert unauth.status_code == 401, "Security bypass detected on /api/v1/cbom"

    # Test authorized access with API key
    auth = client.get("/api/v1/cbom", headers={"X-API-Key": API_KEY})
    assert auth.status_code == 200, "Authorized API request failed"
    print("      └── REST API Authentication & Security PASSED.")

    print("\n✅ Q-Shield ECDAT 100% Production Verification Successful!")

if __name__ == "__main__":
    test_full_solution()
