from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="Q-Shield ECDAT AST Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransformRequest(BaseModel):
    source_code: str
    primitive: str
    shelf_life: int
    migration_time: int
    quantum_horizon: int

@app.post("/api/transform")
async def transform_ast(payload: TransformRequest):
    code = payload.source_code
    transforms_count = 0

    if "Crypto.PublicKey import RSA" in code or "import RSA" in code:
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

    return {
        "status": "success",
        "remediated_code": code,
        "node_transform_count": transforms_count,
        "engine": "Q-Shield LibCST Worker v2.4"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
