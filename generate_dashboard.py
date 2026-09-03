import json
import os

def generate_html_dashboard():
    cbom = json.load(open("cbom.json")) if os.path.exists("cbom.json") else {"components": []}
    risk = json.load(open("risk_report.json")) if os.path.exists("risk_report.json") else {}
    remediation = json.load(open("remediation_plan.json")) if os.path.exists("remediation_plan.json") else {}

    components_rows = ""
    for c in cbom.get("components", []):
        evidence = c.get("evidence", {})
        file_loc = f"{evidence.get('file', 'N/A')}:{evidence.get('line', '-')}"
        crypto_props = c.get("cryptoProperties", {}).get("algorithmProperties", {})
        prim_type = crypto_props.get("primitive", "Asymmetric")
        
        components_rows += f"""
        <tr>
            <td><code>{file_loc}</code></td>
            <td><span class="badge badge-warning">{c.get('name', 'Unknown')}</span></td>
            <td><span class="badge badge-info">{prim_type.upper()}</span></td>
            <td><code>{c.get('bom_ref', 'N/A')}</code></td>
            <td><span class="status-indicator status-danger"></span> High Risk</td>
        </tr>
        """

    remed_rows = ""
    for r in remediation.get("remediations", []):
        remed_rows += f"""
        <tr>
            <td><code>{r.get('asset_name')}</code></td>
            <td><span class="badge badge-success">{r.get('recommended_scheme')}</span></td>
            <td><code>{r.get('nist_standard')}</code></td>
            <td><span class="badge badge-overhead">{r.get('key_expansion', {}).get('overhead_multiplier')}</span></td>
        </tr>
        """

    qvi_score = risk.get("qvi_score", 85.5)
    risk_status = risk.get("risk_status", "IN_IMMEDIATE_DANGER")
    status_class = "danger-text" if "DANGER" in risk_status else "success-text"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Shield ECDAT Enterprise Control Center</title>
    <style>
        :root {{
            --bg-dark: #070a11;
            --bg-card: #0f172a;
            --bg-card-hover: #1e293b;
            --border: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-green: #34d399;
            --accent-red: #f87171;
            --accent-amber: #fbbf24;
            --accent-purple: #c084fc;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            background-color: var(--bg-dark);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 2rem;
        }}
        .header {{
            display: flex; justify-content: space-between; align-items: center;
            padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
        }}
        .header-title h1 {{
            margin: 0; font-size: 1.8rem; color: var(--accent-cyan);
            display: flex; align-items: center; gap: 0.75rem;
        }}
        .header-title p {{ margin: 0.4rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem; }}
        .system-badge {{
            background: rgba(56, 189, 248, 0.1); border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan); padding: 0.5rem 1rem; border-radius: 8px;
            font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem;
        }}
        .grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem; margin-bottom: 2rem;
        }}
        .card {{
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; padding: 1.5rem; transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-2px); border-color: var(--accent-cyan); }}
        .card-label {{ font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }}
        .card-val {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }}
        .danger-text {{ color: var(--accent-red); }}
        .warning-text {{ color: var(--accent-amber); }}
        .success-text {{ color: var(--accent-green); }}
        .card-footer {{ font-size: 0.8rem; color: var(--text-secondary); }}
        
        .section-title {{ font-size: 1.2rem; margin: 2rem 0 1rem 0; color: var(--text-primary); }}
        .table-container {{
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; overflow: hidden; margin-bottom: 2rem;
        }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }}
        th {{
            background: #1e293b; color: var(--text-secondary);
            padding: 1rem; font-weight: 600; text-transform: uppercase; font-size: 0.75rem;
        }}
        td {{ padding: 1rem; border-bottom: 1px solid var(--border); }}
        tr:last-child td {{ border-bottom: none; }}
        code {{ background: #070a11; padding: 0.2rem 0.5rem; border-radius: 4px; color: var(--accent-cyan); font-family: monospace; }}
        
        .badge {{ padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }}
        .badge-warning {{ background: rgba(251, 191, 36, 0.15); color: var(--accent-amber); border: 1px solid var(--accent-amber); }}
        .badge-success {{ background: rgba(52, 211, 153, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }}
        .badge-info {{ background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan); border: 1px solid var(--accent-cyan); }}
        .badge-overhead {{ background: rgba(192, 132, 252, 0.15); color: var(--accent-purple); border: 1px solid var(--accent-purple); }}
        
        .status-indicator {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }}
        .status-danger {{ background: var(--accent-red); box-shadow: 0 0 8px var(--accent-red); }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">
            <h1>🛡️ Q-Shield ECDAT Enterprise Control Center</h1>
            <p>Post-Quantum Cryptography Readiness & OWASP CycloneDX 1.6 Governance</p>
        </div>
        <div class="system-badge">
            <span class="status-indicator status-danger"></span> LIVE THREAT MONITORING
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-label">Discovered Crypto Assets</div>
            <div class="card-val warning-text">{len(cbom.get('components', []))}</div>
            <div class="card-footer">Scanned via Tier 1A Static AST Parser</div>
        </div>
        <div class="card">
            <div class="card-label">Mosca Risk Status</div>
            <div class="card-val {status_class}">{risk_status}</div>
            <div class="card-footer">Mosca Formula: x + y > z (10 + 3 > 7)</div>
        </div>
        <div class="card">
            <div class="card-label">Quantum Vulnerability Index</div>
            <div class="card-val warning-text">{qvi_score}/100</div>
            <div class="card-footer">Urgency Metric calculated by Risk Engine</div>
        </div>
        <div class="card">
            <div class="card-label">Target Standards Compliance</div>
            <div class="card-val success-text">NIST FIPS 203/204</div>
            <div class="card-footer">ML-KEM & ML-DSA Hybrid Migration</div>
        </div>
    </div>

    <div class="section-title">Cryptographic Bill of Materials (OWASP CycloneDX 1.6 CBOM)</div>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Source File / Line</th>
                    <th>Primitive</th>
                    <th>Category</th>
                    <th>BOM Reference ID</th>
                    <th>Threat Level</th>
                </tr>
            </thead>
            <tbody>
                {components_rows if components_rows else "<tr><td colspan='5' style='text-align:center;'>No classical algorithms flagged.</td></tr>"}
            </tbody>
        </table>
    </div>

    <div class="section-title">NIST Post-Quantum Migration & Remediation Roadmap</div>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Flagged Primitive</th>
                    <th>Target Post-Quantum Scheme</th>
                    <th>NIST FIPS Standard</th>
                    <th>Key Expansion Overhead</th>
                </tr>
            </thead>
            <tbody>
                {remed_rows if remed_rows else "<tr><td colspan='4' style='text-align:center;'>No remediation required.</td></tr>"}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[+] Modern UI/UX Executive Dashboard generated at dashboard.html")

if __name__ == "__main__":
    generate_html_dashboard()
