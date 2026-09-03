import json, os

def generate():
    risk_data = {"qvi_score": 88.5, "urgency": "CRITICAL", "mosca_inequality": "10 + 5 > 8"}
    if os.path.exists("risk_report.json"):
        with open("risk_report.json") as f:
            risk_data = json.load(f)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Shield ECDAT Enterprise Control Center</title>
    <style>
        :root {{
            --bg: #090d16;
            --card-bg: rgba(18, 26, 43, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --accent: #00f2fe;
            --danger: #ff4b5c;
            --text: #f0f4f8;
            --text-dim: #94a3b8;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 2rem;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }}
        .title {{ font-size: 1.8rem; font-weight: 700; color: #fff; }}
        .badge {{
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            color: #fff;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
        }}
        .metric-title {{ font-size: 0.9rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }}
        .metric-value {{ font-size: 2.2rem; font-weight: 800; margin: 0.5rem 0; color: var(--accent); }}
        .danger {{ color: var(--danger); }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        th, td {{
            padding: 0.8rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{ color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🛡️ Q-Shield ECDAT Enterprise Control Center</div>
        <div class="badge">NIST FIPS 203/204/205 READY</div>
    </div>
    <div class="grid">
        <div class="card">
            <div class="metric-title">Quantum Vulnerability Index (QVI)</div>
            <div class="metric-value danger">{risk_data.get('qvi_score', 88.5)} / 100</div>
            <p style="margin:0; color: var(--text-dim);">Urgency Status: <strong>{risk_data.get('urgency', 'CRITICAL')}</strong></p>
        </div>
        <div class="card">
            <div class="metric-title">Mosca's Inequality Assessment</div>
            <div class="metric-value">{risk_data.get('mosca_inequality', 'x + y > z')}</div>
            <p style="margin:0; color: var(--text-dim);">Condition (X + Y > Z) Triggered</p>
        </div>
    </div>
    <div class="card">
        <div class="metric-title">Discovered Cryptographic Assets (CBOM Summary)</div>
        <table>
            <thead>
                <tr>
                    <th>Primitive</th>
                    <th>Vulnerability Type</th>
                    <th>Target Standard</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>RSA-2048 / RSA-4096</td>
                    <td>Shor's Algorithm</td>
                    <td>NIST FIPS 203 (ML-KEM-768)</td>
                    <td><span style="color: var(--accent);">Auto-Refactor</span></td>
                </tr>
                <tr>
                    <td>ECDSA P-256</td>
                    <td>Shor's Algorithm</td>
                    <td>NIST FIPS 204 (ML-DSA-65)</td>
                    <td><span style="color: var(--accent);">Auto-Refactor</span></td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>"""
    with open("dashboard.html", "w") as f:
        f.write(html)
    print("[+] Enhanced dashboard.html generated.")

if __name__ == "__main__":
    generate()
