from fastapi.testclient import TestClient
from q_shield.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "engine": "active"}

def test_refactor_endpoint():
    payload = {"code": "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"}
    response = client.post("/refactor", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ml_kem_keygen" in data["refactored"]

def test_cbom_report_endpoint():
    payload = {"path": "vulnerable_sample.py", "shelf_life": 10, "migration_time": 3, "quantum_horizon": 7}
    response = client.post("/report/cbom", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["bomFormat"] == "CycloneDX"
    assert "components" in data

def test_sarif_report_endpoint():
    payload = {"path": "vulnerable_sample.py", "shelf_life": 10, "migration_time": 3, "quantum_horizon": 7}
    response = client.post("/report/sarif", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "2.1.0"
    assert "runs" in data
