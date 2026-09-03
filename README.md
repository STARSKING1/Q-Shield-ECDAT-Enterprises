 # 🛡️ Q-Shield ECDAT

Enterprise Cryptographic Discovery & Assessment Toolkit for PQC migration and Mosca risk calculation.

## 📐 Modules
1. **Module 1 (AST Scanner):** Scans codebase for classical crypto (RSA, ECC, AES, SHA-1).
2. **Module 2 (CBOM Generator):** Exports CycloneDX v1.6 `cbom.json`.
3. **Module 3 (Mosca Engine):** Evaluates risk windows ($x + y > z$) in `risk_report.json`.
4. **Module 4 (PQC Remediator):** Maps legacy primitives to NIST FIPS 203/204/205.
5. **Module 5 (Dashboard):** Compiles interactive HTML report (`dashboard.html`).

## 🚀 Quickstart
```bash
python3 main.py
python3 -m http.server 8081
