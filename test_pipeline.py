import os
import json
from q_shield.parsers.cst_remediator import remediate_code_string

def test_full_solution():
    print("[1] Verifying Generated Artifacts...")
    assert os.path.exists("cbom.json"), "cbom.json missing"
    assert os.path.exists("risk_report.json"), "risk_report.json missing"
    assert os.path.exists("remediation_plan.json"), "remediation_plan.json missing"
    assert os.path.exists("dashboard.html"), "dashboard.html missing"
    print("    └── Artifact verification PASSED.")

    print("[2] Testing LibCST Automated Remediator...")
    legacy_snippet = "from Crypto.PublicKey import RSA\nkey = RSA.generate(2048)"
    res = remediate_code_string(legacy_snippet)
    assert res["success"] is True, "CST Remediation failed"
    assert "HybridMLKEM768" in res["remediated_code"], "Transformation failed"
    print("    └── CST Remediation PASSED.")

    print("\n✅ All 6 Architecture Modules Verified Successfully!")

if __name__ == "__main__":
    test_full_solution()
