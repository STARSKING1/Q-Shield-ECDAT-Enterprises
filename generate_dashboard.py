import json
import os

def create_dashboard():
    risk_file = "risk_report.json"
    remediation_file = "remediation_plan.json"

    if not os.path.exists(risk_file) or not os.path.exists(remediation_file):
        print("[!] Error: Ensure risk_report.json and remediation_plan.json exist before generating dashboard.")
        return

    with open(risk_file, "r") as f:
        risk_data = json.load(f)

    with open(remediation_file, "r") as f:
        remediation_data = json.load(f)

    mosca = risk_data.get("mosca_assessment", {})
    summary = risk_data.get("risk_summary", {})
    findings = risk_data.get("findings", [])
    roadmap = remediation_data.get("remediation_roadmap", [])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Shield ECDAT - Executive Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 25px; }}
        .title {{ font-size: 24px; font-weight: bold; color: #38bdf8; }}
        .badge-danger {{ background-color: #ef4444; color: #fff; padding: 6px 12px; border-radius: 6px; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 25px; }}
        .card {{ background-color: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 20px; }}
        .card-title {{ font-size: 14px; color: #94a3b8; text-transform: uppercase; margin-bottom: 10px; }}
        .card-value {{ font-size: 28px; font-weight: bold; }}
        .critical {{ color: #ef4444; }}
        .high {{ color: #f97316; }}
        .low {{ color: #22c55e; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ text-align: left; padding: 12px; border-bottom: 1px solid #334155; }}
        th {{ background-color: #0f172a; color: #94a3b8; }}
        tr:hover {{ background-color: #334155; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">🛡️ Q-Shield ECDAT Enterprise Dashboard</div>
            <div class="badge-danger">STATUS: {mosca.get("status", "UNKNOWN")}</div>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-title">Mosca's Vulnerability Equation</div>
                <div class="card-value">{mosca.get("formula", "N/A")}</div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 5px;">x (10yr) + y (3yr) > z (7yr) trigger met</p>
            </div>
            <div class="card">
                <div class="card-title">Critical Assets</div>
                <div class="card-value critical">{summary.get("CRITICAL", 0)}</div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 5px;">Shor's Algorithm Vulnerabilities</p>
            </div>
            <div class="card">
                <div class="card-title">High Risk Assets</div>
                <div class="card-value high">{summary.get("HIGH", 0)}</div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 5px;">Grover's Degradation / Weak Hashes</p>
            </div>
            <div class="card">
                <div class="card-title">Quantum Safe Assets</div>
                <div class="card-value low">{summary.get("LOW", 0)}</div>
                <p style="font-size: 12px; color: #94a3b8; margin-top: 5px;">AES-256 / SHA-256 Margin</p>
            </div>
        </div>

        <div class="card" style="margin-bottom: 25px;">
            <div class="card-title">NIST Post-Quantum Cryptography Migration Roadmap</div>
            <table>
                <thead>
                    <tr>
                        <th>Target File</th>
                        <th>Vulnerable Classical Primitive</th>
                        <th>Risk</th>
                        <th>Recommended NIST Standard</th>
                        <th>Hybrid Blueprint</th>
                    </tr>
                </thead>
                <tbody>
"""

    for item in roadmap:
        html_content += f"""
                    <tr>
                        <td><code>{item['file']}</code></td>
                        <td><strong>{item['vulnerable_algorithm']}</strong></td>
                        <td><span class="{item['risk_level'].lower()}">{item['risk_level']}</span></td>
                        <td>{item['nist_standard']}</td>
                        <td><code>{item['hybrid_blueprint']}</code></td>
                    </tr>
"""

    html_content += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

    with open("dashboard.html", "w") as f:
        f.write(html_content)

    print("=== Q-Shield Module 5: Dashboard Generated ===")
    print("Exported interactive dashboard to dashboard.html")

if __name__ == "__main__":
    create_dashboard()
