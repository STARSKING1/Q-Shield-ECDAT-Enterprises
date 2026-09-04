def generate():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Shield ECDAT Enterprise Control Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #070a11;
            --card-bg: rgba(15, 23, 42, 0.65);
            --card-border: rgba(255, 255, 255, 0.08);
            --card-border-hover: rgba(0, 242, 254, 0.3);
            --accent-cyan: #00f2fe;
            --accent-blue: #0072ff;
            --danger-red: #ff4b5c;
            --warning-amber: #f59e0b;
            --success-green: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dark: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 0% 0%, rgba(0, 242, 254, 0.05) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(0, 114, 255, 0.05) 0px, transparent 50%);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            padding: 2rem 1.5rem;
            line-height: 1.5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header UI */
        .header {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }

        .brand-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: #ffffff;
        }

        .brand-icon {
            font-size: 1.75rem;
            filter: drop-shadow(0 0 8px rgba(0, 242, 254, 0.4));
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0, 242, 254, 0.08);
            border: 1px solid rgba(0, 242, 254, 0.25);
            color: var(--accent-cyan);
            padding: 0.4rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-cyan);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-cyan);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(0, 242, 254, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0); }
        }

        /* Metrics Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.75rem;
            transition: all 0.25s ease;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .card:hover {
            border-color: var(--card-border-hover);
            transform: translateY(-2px);
        }

        .metric-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.75rem;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-main);
        }

        .metric-value.critical { color: var(--danger-red); text-shadow: 0 0 12px rgba(255, 75, 92, 0.3); }
        .metric-value.moderate { color: var(--warning-amber); }
        .metric-value.safe { color: var(--success-green); }

        .metric-sub {
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .metric-sub strong {
            color: var(--text-main);
        }

        /* Table Design */
        .table-card {
            overflow: hidden;
        }

        .table-header-container {
            padding: 1.5rem 1.75rem 1rem 1.75rem;
        }

        .table-wrapper {
            width: 100%;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 1rem 1.75rem;
            border-bottom: 1px solid var(--card-border);
        }

        td {
            padding: 1rem 1.75rem;
            border-bottom: 1px solid var(--card-border);
            color: var(--text-main);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        .code-text {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.06);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            border: 1px solid rgba(0, 242, 254, 0.15);
        }

        .action-tag {
            color: var(--accent-cyan);
            font-weight: 600;
            font-size: 0.8rem;
        }

        .empty-state {
            text-align: center;
            padding: 3rem 1.5rem;
            color: var(--text-dark);
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="brand-title">
                <span class="brand-icon">🛡️</span>
                <span>Q-Shield ECDAT Enterprise</span>
            </div>
            <div class="status-badge">
                <span class="pulse-dot"></span>
                <span>NIST FIPS 203 / 204 / 205 READY</span>
            </div>
        </header>

        <!-- Metric Cards -->
        <section class="grid">
            <div class="card">
                <div class="metric-title">Quantum Vulnerability Index (QVI)</div>
                <div id="qvi-score" class="metric-value">0.0 / 100</div>
                <div class="metric-sub">
                    <span>Urgency Status:</span>
                    <strong id="urgency-status">UNSCANNED</strong>
                </div>
            </div>

            <div class="card">
                <div class="metric-title">Mosca's Inequality Assessment</div>
                <div id="mosca-inequality" class="metric-value code-text" style="display: inline-block; font-size: 1.5rem; margin-top: 0.5rem;">--</div>
                <div class="metric-sub" style="margin-top: 1rem;">
                    <span id="mosca-condition-label">Condition (X + Y > Z): Not Evaluated</span>
                </div>
            </div>
        </section>

        <!-- Discovered Assets Table -->
        <section class="card table-card">
            <div class="table-header-container">
                <div class="metric-title">Discovered Cryptographic Assets (CBOM Summary)</div>
            </div>
            <div class="table-wrapper">
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
                        <tr>
                            <td colspan="4" class="empty-state">No cryptographic scan results available. Run scan to populate.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    </div>

    <script>
        const API_KEY = "qshield_secret_key_2026";
        const HEADERS = { "X-API-Key": API_KEY };

        async function fetchDashboardData() {
            try {
                // 1. Fetch Risk Assessment Telemetry
                const riskRes = await fetch('/api/v1/risk', { headers: HEADERS });
                if (riskRes.ok) {
                    const risk = await riskRes.json();
                    
                    const qviElement = document.getElementById('qvi-score');
                    const qviVal = risk.qvi_score !== undefined ? risk.qvi_score : 0.0;
                    qviElement.innerText = `${qviVal} / 100`;

                    // Apply visual dynamic urgency styling strictly based on payload
                    const urgencyElement = document.getElementById('urgency-status');
                    const urgencyVal = risk.urgency || 'UNSCANNED';
                    urgencyElement.innerText = urgencyVal;

                    qviElement.classList.remove('critical', 'moderate', 'safe');
                    if (urgencyVal === 'CRITICAL') {
                        qviElement.classList.add('critical');
                    } else if (urgencyVal === 'MODERATE') {
                        qviElement.classList.add('moderate');
                    } else if (urgencyVal === 'LOW' || urgencyVal === 'SAFE') {
                        qviElement.classList.add('safe');
                    }

                    // Render Mosca Formula
                    const moscaElement = document.getElementById('mosca-inequality');
                    const moscaCondLabel = document.getElementById('mosca-condition-label');
                    
                    if (risk.mosca_inequality) {
                        moscaElement.innerText = risk.mosca_inequality;
                        const isVulnerable = risk.quantum_vulnerable;
                        moscaCondLabel.innerText = isVulnerable 
                            ? "Condition (X + Y > Z): TRIGGERED (Vulnerable)" 
                            : "Condition (X + Y > Z): NOT TRIGGERED (Secure)";
                    } else {
                        moscaElement.innerText = "--";
                        moscaCondLabel.innerText = "Condition (X + Y > Z): Not Evaluated";
                    }
                }

                // 2. Fetch CBOM Component Inventory
                const cbomRes = await fetch('/api/v1/cbom', { headers: HEADERS });
                if (cbomRes.ok) {
                    const cbom = await cbomRes.json();
                    const tbody = document.getElementById('cbom-table-body');
                    
                    if (cbom.components && cbom.components.length > 0) {
                        tbody.innerHTML = cbom.components.map(item => `
                            <tr>
                                <td><span class="code-text">${item.primitive || 'Unknown'}</span></td>
                                <td>${item.vulnerability || "Shor's Algorithm"}</td>
                                <td>${item.target_standard || 'NIST PQC'}</td>
                                <td><span class="action-tag">${item.action || 'Remediate'}</span></td>
                            </tr>
                        `).join('');
                    } else {
                        tbody.innerHTML = `<tr><td colspan="4" class="empty-state">No cryptographic assets discovered in system memory or code files.</td></tr>`;
                    }
                }
            } catch (err) {
                console.error("Error updating telemetry from backend API:", err);
            }
        }

        // Fetch on initial load and poll live every 5 seconds
        fetchDashboardData();
        setInterval(fetchDashboardData, 5000);
    </script>
</body>
</html>"""
    with open("dashboard.html", "w") as f:
        f.write(html)
    print("[+] Dynamic UI/UX dashboard.html updated successfully.")

if __name__ == "__main__":
    generate()
