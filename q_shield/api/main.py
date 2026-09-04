from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from q_shield.parsers.scanner import CryptoScanner
from q_shield.engine.risk_engine import MoscaRiskEngine

app = FastAPI(title="Q-Shield ECDAT API", version="1.0.0")

class ScanRequest(BaseModel):
    path: str
    shelf_life: int = 10
    migration_time: int = 3
    quantum_horizon: int = 7

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "active"}

@app.post("/scan")
def run_scan(payload: ScanRequest):
    try:
        scanner = CryptoScanner()
        findings = scanner.scan_path(payload.path)
        
        engine = MoscaRiskEngine()
        result = engine.evaluate(
            findings, 
            x=payload.shelf_life, 
            y=payload.migration_time, 
            z=payload.quantum_horizon
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from q_shield.engine.reports import ReportGenerator

@app.post("/report/cbom")
def get_cbom(payload: ScanRequest):
    scanner = CryptoScanner()
    findings = scanner.scan_path(payload.path)
    engine = MoscaRiskEngine()
    risk = engine.evaluate(findings, x=payload.shelf_life, y=payload.migration_time, z=payload.quantum_horizon)
    return ReportGenerator.generate_cbom(findings, risk)

@app.post("/report/sarif")
def get_sarif(payload: ScanRequest):
    scanner = CryptoScanner()
    findings = scanner.scan_path(payload.path)
    return ReportGenerator.generate_sarif(findings)

from pydantic import BaseModel as PydanticBaseModel
class RefactorRequest(PydanticBaseModel):
    code: str

from q_shield.parsers.refactor import refactor_code

@app.post("/refactor")
def refactor_source(payload: RefactorRequest):
    try:
        updated_code = refactor_code(payload.code)
        return {"original": payload.code, "refactored": updated_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
