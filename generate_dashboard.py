import json
import os

def generate_html_dashboard():
    cbom = json.load(open("cbom.json")) if os.path.exists("cbom.json") else {"components": []}
    risk = json.load(open("risk_report.json")) if os.path.exists("risk_report.json") else {}
    remediation = json.load(open("remediation_plan.json")) if os.path.exists("remediation_plan.json") else {}

    components_rows = ""
    for c in cbom.get("components", []):
        components_rows += f"""
        <tr>
            <td><code>{c.get('file', 'N/A')}:{c.get('line', '-')}</code></td>
            <td><span class="badge badge-warning">{c.get('name', 'Unknown')}</span></td>
            <td>{c.get('key_size') or 'N/A'} bit</td>
            <td>{c.get('type', 'Cryptographic Asset')}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Shield ECDAT Enterprise Dashboard</title>
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-card: #121824;
            --border-color: #1e293b;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-cyan: #00f2fe;
            --accent-danger: #ef4444;
            --accent-warning: #f59e0b;
            --accent-success: #10b981;
        }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 2rem;
        }}
        .header {{
            display: flex; justify-content: space-between; align-items: center;
            padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
        }}
        .title h1 {{ margin: 0; font-size: 1.8rem; color: var(--accent-cyan); display: flex; align-items: center; gap: 0.5rem; }}
        .title p {{ margin: 0.3rem 0 0 0; color: var(--text-muted); font-size: 0.9rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
        .card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .card-header {{ font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }}
        .card-value {{ font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem; }}
        .danger-text {{ color: var(--accent-danger); }}
        .warning-text {{ color: var(--accent-warning); }}
        .success-text {{ color: var(--accent-success); }}
        table {{ width: 100%; border-collapse: collapse; background: var(--bg-card); border-radius: 12px; overflow: hidden; border: 1px solid var(--border-color); }}
        th, td {{ padding: 1rem; text-align: left; border-bottom: 1px solid var(--border-color); font-size: 0.9rem; }}
        th {{ background-color: #1a2332; color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }}
        code {{ background: #1e293b; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; color: var(--accent-cyan); }}
        .badge {{ padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-warning); border: 1px solid var(--accent-warning); }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">
            <h1>🛡️ Q-Shield ECDAT Enterprise Dashboard</h1>
            <p>Real-Time Post-Quantum Cryptography Readiness & Mosca Risk Assessment</p>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-header">Detected Classical Assets</div>
            <div class="card-value warning-text">{len(cbom.get('components', []))}</div>
            <p style="margin:0; font-size:0.8rem; color:var(--text-muted);">Scanned via Module 1 AST Analyzer</p>
        </div>
        <div class="card">
            <div class="card-header">Mosca Quantum Threat State</div>
            <div class="card-value danger-text">{risk.get('risk_status', 'IN_IMMEDIATE_DANGER')}</div>
            <p style="margin:0; font-size:0.8rem; color:var(--text-muted);">Formula: x + y > z (10 + 3 > 7)</p>
        </div>
        <div class="card">
            <div class="card-header">Target Migration Target</div>
            <div class="card-value success-text">NIST FIPS 203/204</div>
            <p style="margin:0; font-size:0.8rem; color:var(--text-muted);">ML-KEM & ML-DSA Hybrid Scheme</p>
        </div>
    </div>

    <div class="card" style="padding:0;">
        <div style="padding:1.5rem 1.5rem 1rem 1.5rem; border-bottom:1px solid var(--border-color);">
            <h3 style="margin:0; font-size:1.1rem;">Discovered Cryptographic Assets (CBOM v1.6)</h3>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Location / Line</th>
                    <th>Algorithm</th>
                    <th>Key Size</th>
                    <th>Asset Type</th>
                </tr>
            </thead>
            <tbody>
                {components_rows if components_rows else "<tr><td colspan='4' style='text-align:center;'>No legacy cryptographic primitives flagged in current codebase.</td></tr>"}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

    with open("dashboard.html", "w") as f:
        f.write(html_content)
    print("[+] UI/UX Executive Dashboard compiled into dashboard.html successfully.")

if __name__ == "__main__":
    generate_html_dashboard()
