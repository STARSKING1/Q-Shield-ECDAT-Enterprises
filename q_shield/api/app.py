import os
import json
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from q_shield.db.session import get_db, init_db
from q_shield.db.models import ScanSession, RiskSnapshot, CBOMAsset

# Ensure database tables exist on startup
init_db()

API_KEY = os.getenv("QSHIELD_API_KEY", "qshield_secret_key_2026")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI(title="Q-Shield ECDAT Enterprise API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
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
    return {
        "status": "healthy", 
        "standards": [
            "NIST FIPS 203 (ML-KEM)", 
            "NIST FIPS 204 (ML-DSA)", 
            "NIST FIPS 205 (SLH-DSA)"
        ],
        "database": "connected"
    }

@app.get("/")
def get_dashboard():
    if os.path.exists("dashboard.html"):
        return FileResponse("dashboard.html")
    return JSONResponse({"message": "Dashboard not generated yet."})

@app.get("/api/v1/risk", dependencies=[Depends(verify_api_key)])
def get_risk(db: Session = Depends(get_db)):
    # Fetch latest risk snapshot from database
    latest_snapshot = db.query(RiskSnapshot).order_by(RiskSnapshot.id.desc()).first()
    if latest_snapshot:
        return {
            "qvi_score": latest_snapshot.qvi_score,
            "urgency": latest_snapshot.urgency,
            "mosca_inequality": f"{latest_snapshot.mosca_x} + {latest_snapshot.mosca_y} > {latest_snapshot.mosca_z}",
            "scan_id": latest_snapshot.scan_id
        }
    
    # Fallback to local JSON snapshot if database record is missing
    if os.path.exists("risk_report.json"):
        with open("risk_report.json") as f:
            return json.load(f)
            
    return {"qvi_score": 0.0, "urgency": "UNSCANNED"}

@app.get("/api/v1/cbom", dependencies=[Depends(verify_api_key)])
def get_cbom(db: Session = Depends(get_db)):
    # Fetch components from database
    assets = db.query(CBOMAsset).all()
    if assets:
        components = []
        for a in assets:
            components.append({
                "name": a.asset_name,
                "type": a.asset_type,
                "discovered_primitive": a.discovered_primitive,
                "pqc_target_standard": a.pqc_target_standard,
                "severity": a.severity,
                "source_location": a.source_location
            })
        return {"components": components}

    # Fallback to local JSON file
    if os.path.exists("cbom.json"):
        with open("cbom.json") as f:
            return json.load(f)
            
    return {"components": []}

@app.post("/api/v1/scan", dependencies=[Depends(verify_api_key)])
def trigger_scan(target_project: str, db: Session = Depends(get_db)):
    new_scan = ScanSession(target_project=target_project, status="PENDING")
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    return {"scan_id": new_scan.id, "target_project": target_project, "status": new_scan.status}
