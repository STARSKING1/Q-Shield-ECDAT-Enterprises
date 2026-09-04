import json

ALGORITHM_WEIGHTS = {
    "RSA-2048": 1.0,
    "RSA-4096": 1.0,
    "ECC-256": 1.0,
    "ECDSA P-256": 1.0,
    "AES-128": 0.5,
    "AES-256": 0.1,
    "SHA-384": 0.1
}

def evaluate_mosca_risk(x: float, y: float, z: float, primitive: str = "RSA-2048") -> dict:
    w_alg = ALGORITHM_WEIGHTS.get(primitive, 1.0)
    is_vulnerable = (x + y) > z
    
    # Calculate weighted QVI Score
    raw_qvi = ((x + y) / max(0.1, z)) * 50.0 * w_alg
    qvi_score = round(min(100.0, max(0.0, raw_qvi)), 2)
    
    if qvi_score >= 80.0:
        urgency = "CRITICAL"
    elif qvi_score >= 40.0:
        urgency = "MODERATE"
    else:
        urgency = "SAFE"
        
    report = {
        "primitive": primitive,
        "algorithm_weight": w_alg,
        "mosca_inequality": f"{x} + {y} > {z}",
        "is_vulnerable": is_vulnerable,
        "quantum_vulnerable": is_vulnerable,
        "qvi_score": qvi_score,
        "urgency": urgency
    }
    
    with open("risk_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    return report

class MoscaAssessment:
    """Orchestrator-compatible Mosca Assessment Engine wrapper."""
    def __init__(self, x: float = 10.0, y: float = 5.0, z: float = 8.0, primitive: str = "RSA-2048", **kwargs):
        # Support named arguments from main.py orchestrator
        self.x = kwargs.get("data_shelf_life_x", x)
        self.y = kwargs.get("migration_time_y", y)
        self.z = kwargs.get("time_to_crqc_z", z)
        self.primitive = primitive

    def evaluate(self) -> dict:
        return evaluate_mosca_risk(self.x, self.y, self.z, self.primitive)
    
    def calculate_qvi(self) -> dict:
        return evaluate_mosca_risk(self.x, self.y, self.z, self.primitive)
