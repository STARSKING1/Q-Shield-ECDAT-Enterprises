from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

from q_shield.engine.mosca import evaluate_mosca_risk
from q_shield.parsers.cst_remediator import remediate_code

app = FastAPI(
    title="Q-Shield ECDAT Interactive Enterprise Control Center",
    version="1.0.0",
    description="Dynamic request-driven PQC risk analysis and CST code refactoring engine"
)

class SimulationRequest(BaseModel):
    x_shelf_life: int = Field(..., ge=1, le=50, description="Data shelf life requirement (years)")
    y_migration_time: int = Field(..., ge=1, le=20, description="System migration duration (years)")
    z_crqc_horizon: int = Field(..., ge=1, le=30, description="Estimated years until CRQC arrival")
    primitive: str = Field(..., description="Target cryptographic primitive")
    source_code: Optional[str] = Field(default="", description="Legacy Python source code to remediate")

@app.post("/api/v1/simulate")
async def run_dynamic_simulation(payload: SimulationRequest):
    """Computes dynamic Mosca QVI metrics and performs live AST transformations."""
    # 1. Compute dynamic Mosca & QVI metric
    risk_summary = evaluate_mosca_risk(
        x=payload.x_shelf_life,
        y=payload.y_migration_time,
        z=payload.z_crqc_horizon,
        primitive=payload.primitive
    )

    # 2. Perform live CST AST remediation on user-provided code
    remediated_code, transformations = remediate_code(payload.source_code or "")

    # 3. Construct dynamic CycloneDX 1.6 CBOM payload
    cbom_data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "metadata": {
            "timestamp": "2026-09-04T00:00:00Z",
            "tool": "Q-Shield ECDAT Interactive Visual Control Center"
        },
        "components": [
            {
                "type": "cryptographic-asset",
                "name": "User-Submitted-Code",
                "primitive": payload.primitive,
                "quantum_vulnerability_index": risk_summary["qvi_score"],
                "status": risk_summary["urgency"],
                "pqc_target": "NIST FIPS 203 (ML-KEM-768)" if risk_summary["is_vulnerable"] else "Compliant",
                "transformations_applied": transformations
            }
        ]
    }

    return {
        "risk_assessment": risk_summary,
        "remediation": {
            "transformations_count": transformations,
            "remediated_code": remediated_code
        },
        "cbom": cbom_data
    }


@app.get("/demo", response_class=HTMLResponse)
async def serve_interactive_dashboard():
    """Serves the Interactive Visual Control Center UI."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Q-Shield Interactive Visual Control Center</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0b0f19; color: #f8fafc; margin: 0; padding: 24px; }
            .header { text-align: center; margin-bottom: 24px; }
            .header h1 { color: #38bdf8; margin: 0 0 8px 0; }
            .header p { color: #94a3b8; margin: 0; }
            .container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
            .card { background: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; }
            h2 { color: #38bdf8; margin-top: 0; font-size: 1.25rem; }
            label { display: block; margin: 16px 0 6px; font-weight: 600; font-size: 0.9rem; color: #cbd5e1; }
            input[type=range] { width: 100%; accent-color: #38bdf8; }
            select, textarea { width: 100%; box-sizing: border-box; background: #090d16; color: #38bdf8; font-family: monospace; border: 1px solid #334155; border-radius: 6px; padding: 10px; font-size: 13px; }
            textarea { height: 130px; resize: vertical; }
            button { width: 100%; background: #0284c7; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 20px; font-size: 1rem; }
            button:hover { background: #0369a1; }
            pre { background: #090d16; padding: 12px; border-radius: 6px; overflow-x: auto; color: #4ade80; font-size: 12px; border: 1px solid #1e293b; max-height: 200px; }
            .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; }
            .CRITICAL { background: #ef4444; color: white; }
            .MODERATE { background: #f59e0b; color: white; }
            .SAFE { background: #22c55e; color: white; }
            .metric-box { background: #090d16; padding: 16px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 16px; }
            .val-span { color: #38bdf8; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Q-Shield ECDAT Enterprise Control Center</h1>
            <p>Dynamic Parameter Testing Sandbox & Live AST Refactoring</p>
        </div>
        <div class="container">
            <div class="card">
                <h2>Parameter Controls</h2>
                
                <label>Data Shelf-Life Requirement (x): <span id="val_x" class="val-span">1</span> years</label>
                <input type="range" id="x" min="1" max="50" value="1" oninput="document.getElementById('val_x').innerText=this.value">
                
                <label>Migration Time (y): <span id="val_y" class="val-span">1</span> years</label>
                <input type="range" id="y" min="1" max="20" value="1" oninput="document.getElementById('val_y').innerText=this.value">
                
                <label>Quantum Horizon (z): <span id="val_z" class="val-span">1</span> years</label>
                <input type="range" id="z" min="1" max="30" value="1" oninput="document.getElementById('val_z').innerText=this.value">
                
                <label>Target Cryptographic Primitive:</label>
                <select id="primitive">
                    <option value="">-- Select Primitive --</option>
                    <option value="RSA-2048">RSA-2048</option>
                    <option value="ECDSA-P256">ECDSA-P256</option>
                    <option value="AES-128">AES-128</option>
                    <option value="AES-256">AES-256</option>
                    <option value="ML-KEM-768">ML-KEM-768</option>
                </select>

                <label>Source Code Sandbox:</label>
                <textarea id="source_code" placeholder="Enter custom Python code here..."></textarea>
                
                <button onclick="runSimulation()">Execute Parameter Logic</button>
            </div>

            <div class="card">
                <h2>Real-Time Live Results</h2>
                
                <div class="metric-box">
                    <div>QVI Score: <strong id="qvi_display" style="font-size: 28px; color: #38bdf8;">--</strong> / 100</div>
                    <div style="margin-top: 8px;">Urgency Status: <span id="status_badge" class="badge SAFE">UNKNOWN</span></div>
                </div>
                
                <h3>Remediated Code Output:</h3>
                <pre id="code_output">// Output will appear here after execution</pre>
                
                <h3>Generated CBOM (CycloneDX 1.6):</h3>
                <pre id="cbom_output">// CBOM payload will appear here after execution</pre>
            </div>
        </div>

        <script>
            async function runSimulation() {
                const primitiveValue = document.getElementById('primitive').value;
                if (!primitiveValue) {
                    alert('Please select a cryptographic primitive.');
                    return;
                }

                const payload = {
                    x_shelf_life: parseInt(document.getElementById('x').value),
                    y_migration_time: parseInt(document.getElementById('y').value),
                    z_crqc_horizon: parseInt(document.getElementById('z').value),
                    primitive: primitiveValue,
                    source_code: document.getElementById('source_code').value
                };

                try {
                    const res = await fetch('/api/v1/simulate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!res.ok) {
                        const err = await res.json();
                        alert('Error: ' + JSON.stringify(err));
                        return;
                    }

                    const data = await res.json();
                    document.getElementById('qvi_display').innerText = data.risk_assessment.qvi_score;
                    
                    const badge = document.getElementById('status_badge');
                    badge.innerText = data.risk_assessment.urgency;
                    badge.className = 'badge ' + data.risk_assessment.urgency;

                    document.getElementById('code_output').innerText = data.remediation.remediated_code || "// No remediation changes required";
                    document.getElementById('cbom_output').innerText = JSON.stringify(data.cbom, null, 2);
                } catch (e) {
                    alert('Failed to connect to API server.');
                }
            }
        </script>
    </body>
    </html>
    """
