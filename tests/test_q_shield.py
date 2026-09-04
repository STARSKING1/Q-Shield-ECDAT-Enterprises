import pytest
from q_shield.engine.mosca import evaluate_mosca_risk
from q_shield.parsers.cst_remediator import remediate_code
from q_shield.serializers.cbom_generator import build_cyclonedx_cbom

def test_mosca_risk_evaluation():
    # Test Critical Risk
    res = evaluate_mosca_risk(x=10, y=5, z=8, primitive="RSA-2048")
    assert res["urgency"] == "CRITICAL"
    assert res["qvi_score"] > 0

    # Test Safe Risk (quantum-resistant primitive)
    res_safe = evaluate_mosca_risk(x=10, y=5, z=8, primitive="AES-256")
    assert res_safe["urgency"] == "SAFE"
    assert res_safe["qvi_score"] == 0.0

def test_cst_remediator():
    code = "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"
    refactored, count = remediate_code(code)
    
    # Expect 2 AST nodes matched (Import node + Call node)
    assert count == 2
    assert "mlkem" in refactored.lower() or "generate" in refactored

def test_cbom_generator():
    cbom = build_cyclonedx_cbom(
        scan_id="test-123",
        primitive="RSA-2048",
        qvi_score=87.5,
        urgency="CRITICAL",
        transformations_count=2
    )
    
    assert cbom["bomFormat"] == "CycloneDX"
    assert cbom["specVersion"] == "1.6"
    assert "test-123" in cbom["serialNumber"]
