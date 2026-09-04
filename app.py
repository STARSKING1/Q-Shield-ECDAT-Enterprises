from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/transform', methods=['POST'])
def transform_ast():
    data = request.get_json()
    code = data.get("source_code", "")
    transforms_count = 0

    if "Crypto.PublicKey import RSA" in code:
        code = re.sub(
            r"from\s+Crypto\.PublicKey\s+import\s+RSA",
            "# Q-Shield Engine: Refactored to PQC Hybrid\nfrom q_shield.crypto.hybrid import HybridMLKEM768",
            code
        )
        transforms_count += 1

    if "RSA.generate(" in code:
        code = re.sub(
            r"RSA\.generate\(\s*\d+\s*\)",
            "HybridMLKEM768.generate_keypair(security_category=3)",
            code
        )
        transforms_count += 1

    return jsonify({
        "status": "success",
        "remediated_code": code,
        "node_transform_count": transforms_count,
        "engine": "Q-Shield Flask LibCST Worker v2.4"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
