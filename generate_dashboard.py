def generate():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Shield ECDAT Enterprise Control Center</title>
    <style>
        :root {
            --bg: #090d16;
            --card-bg: rgba(18, 26, 43, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --accent: #00f2fe;
            --danger: #ff4b5c;
            --text: #f0f4f8;
            --text-dim: #94a3b8;
        }
        body { background-color: var(--bg); color: var(--text); font-family: sans-serif; padding: 2rem; margin: 0; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 2rem; }
        .title { font-size: 1.8rem; font-weight: 700; color: #fff; }
        .badge { background: linear-gradient(135deg, #00c6ff, #0072ff); color: #fff; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .card { background: var(--card-bg); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
        .metric-title { font-size: 0.9rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { font-size: 2.2rem; font-weight: 800; margin: 0.5rem 0; color: var(--accent); }
        .danger { color: var(--danger); }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.8rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }
        th { color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase; }
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
            <div id="qvi-score" class="metric-value danger">Loading...</div>
            <p style="margin:0; color: var(--text-dim);">Urgency Status: <strong id="urgency-status">--</strong></p>
        </div>
        <div class="card">
            <div class="metric-title">Mosca's Inequality Assessment</div>
            <div id="mosca-inequality" class="metric-value">Loading...</div>
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
            <tbody id="cbom-table-body">
                <tr><td colspan="4">Loading dynamic telemetry...</td></tr>
            </tbody>
        </table>
    </div>

    <script>
        const API_KEY = "qshield_secret_key_2026";
        const HEADERS = { "X-API-Key": API_KEY };

        async function fetchDashboardData() {
            try {
                // 1. Fetch Risk Data
                const riskRes = await fetch('/api/v1/risk', { headers: HEADERS });
                if (riskRes.ok) {
                    const risk = await riskRes.json();
                    document.getElementById('qvi-score').innerText = `${risk.qvi_score || 0.0} / 100`;
                    document.getElementById('urgency-status').innerText = risk.urgency || 'UNKNOWN';
                    document.getElementById('mosca-inequality').innerText = risk.mosca_inequality || 'N/A';
                }

                // 2. Fetch CBOM Inventory
                const cbomRes = await fetch('/api/v1/cbom', { headers: HEADERS });
                if (cbomRes.ok) {
                    const cbom = await cbomRes.json();
                    const tbody = document.getElementById('cbom-table-body');
                    if (cbom.components && cbom.components.length > 0) {
                        tbody.innerHTML = cbom.components.map(item => `
                            <tr>
                                <td>${item.primitive || 'Unknown'}</td>
                                <td>${item.vulnerability || "Shor's Algorithm"}</td>
                                <td>${item.target_standard || 'NIST PQC'}</td>
                                <td><span style="color: var(--accent);">${item.action || 'Remediate'}</span></td>
                            </tr>
                        `).join('');
                    } else {
                        tbody.innerHTML = `<tr><td colspan="4">No cryptographic assets found in cbom.json.</td></tr>`;
                    }
                }
            } catch (err) {
                console.error("Failed to update dashboard telemetry:", err);
            }
        }

        // Fetch on load and poll every 5 seconds
        fetchDashboardData();
        setInterval(fetchDashboardData, 5000);
    </script>
</body>
</html>"""
    with open("dashboard.html", "w") as f:
        f.write(html)
    print("[+] Live API-backed dashboard.html generated.")

if __name__ == "__main__":
    generate()
