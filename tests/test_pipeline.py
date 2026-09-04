import pytest
from fastapi.testclient import TestClient
from q_shield.engine.mosca import evaluate_mosca_risk
from q_shield.parsers.cst_remediator import remediate_code
from q_shield.api.app import app

client = TestClient(app)

# --- 1. Mosca Theorem & QVI Tests ---

def test_mosca_critical_vulnerability():
    # x=10, y=3 => x+y=13 > z=7 (CRITICAL)
    result = evaluate_mosca_risk(x=10, y=3, z=7, primitive="RSA-2048")
    assert result["is_vulnerable"] is True
    assert result["urgency"] == "CRITICAL"
    assert result["qvi_score"] >= 80.0

def test_mosca_safe_primitive():
    # Symmetric AES-256 with long CRQC horizon
    result = evaluate_mosca_risk(x=2, y=1, z=15, primitive="AES-256")
    assert result["is_vulnerable"] is False
    assert result["urgency"] == "SAFE"
    assert result["qvi_score"] < 30.0

# --- 2. LibCST Code Transformation Tests ---

def test_cst_remediation_rsa_import():
    legacy_code = """# Legacy Crypto Module
from Crypto.PublicKey import RSA

def generate_key():
    key = RSA.generate(2048)
    return key
"""
    new_code, changes = remediate_code(legacy_code)
    assert changes == 1
    assert "from q_shield.pqc import HybridMLKEM768, MLDSA65" in new_code
    assert "# Legacy Crypto Module" in new_code  # Preserves inline comments

def test_cst_remediation_no_op():
    clean_code = "import os\nimport sys\nprint('No cryptography here')"
    new_code, changes = remediate_code(clean_code)
    assert changes == 0
    assert new_code == clean_code

# --- 3. REST API Endpoint Tests ---

def test_api_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "NIST FIPS 203 (ML-KEM)" in data["standards"]

def test_api_risk_unauthorized():
    # Request without X-API-Key header
    response = client.get("/api/v1/risk")
    assert response.status_code == 401

def test_api_risk_authorized():
    headers = {"X-API-Key": "qshield_secret_key_2026"}
    response = client.get("/api/v1/risk", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "qvi_score" in data
    assert "urgency" in data

def test_api_cbom_structure():
    headers = {"X-API-Key": "qshield_secret_key_2026"}
    response = client.get("/api/v1/cbom", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "components" in data
    assert isinstance(data["components"], list)
