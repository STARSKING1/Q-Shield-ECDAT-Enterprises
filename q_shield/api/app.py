from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import json, os

API_KEY = os.getenv("QSHIELD_API_KEY", "qshield_secret_key_2026")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI(title="Q-Shield ECDAT Enterprise API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

async def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key header")
    return key

@app.get("/health")
def health():
    return {"status": "ACTIVE", "standards": ["NIST FIPS 203", "NIST FIPS 204", "NIST FIPS 205"]}

@app.get("/")
def get_dashboard():
    if os.path.exists("dashboard.html"):
        return FileResponse("dashboard.html")
    return JSONResponse({"message": "Dashboard not generated yet. Run generate_dashboard.py"})

@app.get("/api/v1/cbom", dependencies=[Depends(verify_api_key)])
def get_cbom():
    if os.path.exists("cbom.json"):
        with open("cbom.json") as f:
            return json.load(f)
    return {"components": []}

@app.get("/api/v1/risk", dependencies=[Depends(verify_api_key)])
def get_risk():
    if os.path.exists("risk_report.json"):
        with open("risk_report.json") as f:
            return json.load(f)
    return {"qvi_score": 0.0}

@app.get("/api/v1/remediation", dependencies=[Depends(verify_api_key)])
def get_remediation():
    if os.path.exists("remediation_plan.json"):
        with open("remediation_plan.json") as f:
            return json.load(f)
    return {"remediations": []}
