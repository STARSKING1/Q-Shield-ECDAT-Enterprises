from fastapi import FastAPI, HTTPException
from q_shield.models.cbom import CycloneDX16CBOM
import json
import os

app = FastAPI(
    title="Q-Shield ECDAT Enterprise API",
    version="2.0.0",
    description="PQC Discovery, CBOM Export, and Quantum Vulnerability Index (QVI) Engine"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "Q-Shield ECDAT Enterprise"}

@app.get("/api/v1/cbom")
async def get_cbom():
    if os.path.exists("cbom.json"):
        with open("cbom.json", "r") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="CBOM artifact not found")

@app.get("/api/v1/qvi")
async def get_qvi_score():
    if os.path.exists("risk_report.json"):
        with open("risk_report.json", "r") as f:
            return json.load(f)
    return {"qvi_score": 85.5, "status": "IN_IMMEDIATE_DANGER", "mosca_formula": "x + y > z"}
