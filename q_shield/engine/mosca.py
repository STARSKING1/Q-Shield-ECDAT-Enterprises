from typing import Any, Dict

PRIMITIVE_WEIGHTS = {
    "RSA-1024": 2.0,
    "RSA-2048": 1.0,
    "RSA-4096": 0.8,
    "ECDSA-P256": 1.0,
    "ECDSA-P384": 0.9,
    "AES-128": 0.3,
    "AES-256": 0.0,
    "ML-KEM-768": 0.0,
    "ML-DSA-65": 0.0,
}


def evaluate_mosca_risk(x: int, y: int, z: int, primitive: str) -> Dict[str, Any]:
    weight = PRIMITIVE_WEIGHTS.get(primitive, 1.0)
    is_vulnerable = (x + y) > z and weight > 0.0

    if weight == 0.0 or z <= 0:
        qvi = 0.0
    else:
        raw_diff = x + y - z
        qvi = min(100.0, max(0.0, (raw_diff / float(z)) * 100.0 * weight))

    if qvi >= 75.0 or (is_vulnerable and weight >= 1.0):
        urgency = "CRITICAL"
    elif qvi >= 40.0 or is_vulnerable:
        urgency = "MODERATE"
    else:
        urgency = "SAFE"

    return {
        "x_shelf_life": x,
        "y_migration_time": y,
        "z_crqc_horizon": z,
        "primitive": primitive,
        "is_vulnerable": is_vulnerable,
        "qvi_score": round(qvi, 2),
        "urgency": urgency,
    }
