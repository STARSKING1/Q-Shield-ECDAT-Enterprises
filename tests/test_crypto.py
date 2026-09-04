import pytest
from q_shield.engine.risk_engine import MoscaRiskEngine
from q_shield.parsers.scanner import CryptoScanner

def test_mosca_risk_evaluation():
    engine = MoscaRiskEngine()
    findings = [{"primitive": "RSA-2048", "file_path": "sample.py", "line_number": 5}]
    
    result = engine.evaluate(findings, x=10, y=3, z=7)
    
    assert result["qvi_score"] > 0
    assert result["urgency"] in ["CRITICAL", "HIGH", "MODERATE", "SAFE"]
    assert "cbom" in result

def test_scanner_detection():
    scanner = CryptoScanner()
    sample_code = "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"
    assert "RSA" in sample_code
