import pytest
from starlette.testclient import TestClient
from q_shield.dashboard_app import app

@pytest.fixture
def client():
    # Set up Flask app in testing mode
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Ensure the web control console UI renders successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Q-Shield ECDAT Control Console" in response.data

def test_run_api_endpoint(client):
    """Validate synchronous state execution across risk, CST, and CBOM engines."""
    payload = {
        "x": 10,
        "y": 5,
        "z": 8,
        "primitive": "RSA-2048",
        "source_code": "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"
    }
    
    response = client.post("/api/run", json=payload)
    assert response.status_code == 200
    
    data = response.get_json()
    assert "risk_assessment" in data
    assert "refactored_code" in data
    assert "cbom_payload" in data
    
    # Verify core engine output bindings
    assert data["risk_assessment"]["urgency"] == "CRITICAL"
    assert data["cbom_payload"]["bomFormat"] == "CycloneDX"
    assert data["transformations_applied"] > 0
