from flask import Flask, render_template_string, request, jsonify
from q_shield.engine.mosca import evaluate_mosca_risk
from q_shield.parsers.cst_remediator import remediate_code
from q_shield.serializers.cbom_generator import build_cyclonedx_cbom

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Q-Shield ECDAT Console</title>
    <style>
        body { font-family: monospace; background: #0f172a; color: #f8fafc; padding: 20px; }
        .container { display: flex; gap: 20px; }
        .box { background: #1e293b; padding: 15px; border-radius: 8px; flex: 1; }
        pre { background: #090d16; padding: 10px; border-radius: 5px; overflow-x: auto; color: #38bdf8; }
        label { display: block; margin-top: 10px; }
        input, select, textarea { width: 100%; background: #334155; color: white; border: none; padding: 8px; border-radius: 4px; }
        button { margin-top: 15px; background: #0284c7; color: white; padding: 10px; border: none; width: 100%; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🛡️ Q-Shield ECDAT Control Console</h1>
    <div class="container">
        <div class="box">
            <h3>Parameters</h3>
            <form id="pqcForm">
                <label>Shelf Life (x years):</label>
                <input type="number" id="x" value="10">
                <label>Migration Time (y years):</label>
                <input type="number" id="y" value="5">
                <label>Quantum Horizon (z years):</label>
                <input type="number" id="z" value="8">
                <label>Primitive:</label>
                <select id="primitive">
                    <option value="RSA-2048">RSA-2048</option>
                    <option value="RSA-1024">RSA-1024</option>
                    <option value="ECDSA-P256">ECDSA-P256</option>
                    <option value="AES-256">AES-256</option>
                </select>
                <label>Source Code:</label>
                <textarea id="source_code" rows="5">from Crypto.PublicKey import RSA&#10;key = RSA.generate(2048)</textarea>
                <button type="button" onclick="runSimulation()">Evaluate & Refactor</button>
            </form>
        </div>
        <div class="box">
            <h3>Output Dashboard</h3>
            <pre id="output">Adjust parameters and click Evaluate...</pre>
        </div>
    </div>

    <script>
        async function runSimulation() {
            const data = {
                x: parseInt(document.getElementById('x').value),
                y: parseInt(document.getElementById('y').value),
                z: parseInt(document.getElementById('z').value),
                primitive: document.getElementById('primitive').value,
                source_code: document.getElementById('source_code').value
            };
            const res = await fetch('/api/run', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            document.getElementById('output').innerText = JSON.stringify(result, null, 2);
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/run", methods=["POST"])
def run_api():
    data = request.json
    risk = evaluate_mosca_risk(data["x"], data["y"], data["z"], data["primitive"])
    remediated_code, count = remediate_code(data["source_code"])
    cbom = build_cyclonedx_cbom("web-01", data["primitive"], risk["qvi_score"], risk["urgency"], count)

    return jsonify({
        "risk_assessment": risk,
        "refactored_code": remediated_code,
        "transformations_applied": count,
        "cbom_payload": cbom
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
