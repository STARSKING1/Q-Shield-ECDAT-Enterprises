from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import json
import os

app = FastAPI(
    title="Q-Shield ECDAT API Server",
    description="Enterprise Post-Quantum Crypto Agility & Risk Assessment Engine",
    version="2.0.0"
)

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    if os.path.exists("dashboard.html"):
        with open("dashboard.html", "r") as f:
            return f.read()
    return "<h1>Dashboard not generated yet. Run python main.py first.</h1>"

@app.get("/api/v1/cbom")
def get_cbom():
    if os.path.exists("cbom.json"):
        with open("cbom.json", "r") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="cbom.json not found.")

@app.get("/api/v1/risk")
def get_risk_report():
    if os.path.exists("risk_report.json"):
        with open("risk_report.json", "r") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="risk_report.json not found.")

@app.get("/api/v1/remediation")
def get_remediation_plan():
    if os.path.exists("remediation_plan.json"):
        with open("remediation_plan.json", "r") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="remediation_plan.json not found.")
