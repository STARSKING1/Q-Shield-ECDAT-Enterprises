import json
import os
from fastapi import FastAPI, HTTPException, Security, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response

# API Key Security Configuration
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("QSHIELD_API_KEY", "qshield_prod_sec_key_2026")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(header_key: str = Depends(api_key_header)):
    if header_key == API_KEY:
        return header_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing X-API-Key header",
    )

app = FastAPI(
    title="Q-Shield ECDAT Enterprise API Core",
    description="Secured Post-Quantum Crypto Agility & Risk Assessment REST Engine",
    version="2.0.0"
)

# CORS Policy - Restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Middleware for Enterprise Security Headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"
    return response

def _safe_read_json(file_path: str):
    # Ensure canonical path safety against directory traversal
    base_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(os.path.join(base_dir, file_path))
    
    if not target_path.startswith(base_dir):
        raise HTTPException(status_code=403, detail="Unauthorized file access attempt")
    
    if not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail=f"Artifact {file_path} not found. Run pipeline first.")
    
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading artifact: {str(e)}")

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "engine": "Q-Shield ECDAT Enterprise Core",
        "pqc_standards": ["FIPS 203", "FIPS 204", "FIPS 205"],
        "security_enabled": True
    }

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def get_dashboard():
    base_dir = os.path.abspath(os.getcwd())
    dashboard_path = os.path.join(base_dir, "dashboard.html")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Q-Shield ECDAT: Dashboard not generated yet. Run 'python main.py' first.</h1>"

@app.get("/api/v1/cbom", tags=["Artifacts"], dependencies=[Depends(verify_api_key)])
async def get_cbom():
    return _safe_read_json("cbom.json")

@app.get("/api/v1/risk", tags=["Artifacts"], dependencies=[Depends(verify_api_key)])
async def get_risk_report():
    return _safe_read_json("risk_report.json")

@app.get("/api/v1/remediation", tags=["Artifacts"], dependencies=[Depends(verify_api_key)])
async def get_remediation_plan():
    return _safe_read_json("remediation_plan.json")
