import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class MoscaTimeline:
    x_data_shelflife_years: float  # Shelf-life of secret data
    y_migration_years: float       # Time required to migrate infrastructure to PQC
    z_time_to_crqc_years: float    # Time until a Cryptographically Relevant Quantum Computer arrives

class MoscaEngine:
    def __init__(self, timeline: MoscaTimeline):
        self.timeline = timeline

    def evaluate_risk(self, assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        x = self.timeline.x_data_shelflife_years
        y = self.timeline.y_migration_years
        z = self.timeline.z_time_to_crqc_years

        # Mosca's Inequality: x + y > z
        is_vulnerable = (x + y) > z
        margin = (x + y) - z

        # Calculate Quantum Vulnerability Index (QVI) score (0-100 scale)
        # Higher score indicates higher urgency
        qvi_score = min(100.0, max(0.0, ((x + y) / z) * 50.0))

        status = "IN_IMMEDIATE_DANGER" if is_vulnerable else "SAFE_WINDOW"

        report = {
            "risk_status": status,
            "is_vulnerable": is_vulnerable,
            "qvi_score": round(qvi_score, 2),
            "mosca_variables": asdict(self.timeline),
            "threat_margin_years": round(margin, 2),
            "evaluated_assets_count": len(assets),
            "recommendation": (
                "Initiate immediate hybrid PQC transition (NIST FIPS 203/204). "
                "Data is susceptible to Harvest Now, Decrypt Later attacks."
                if is_vulnerable else "Monitor timeline and prepare PQC roadmap."
            )
        }

        with open("risk_report.json", "w") as f:
            json.dump(report, f, indent=2)

        return report

def run_mosca_assessment(data_shelf_life=10.0, migration_time=3.0, time_to_crqc=7.0):
    timeline = MoscaTimeline(
        x_data_shelflife_years=data_shelf_life,
        y_migration_years=migration_time,
        z_time_to_crqc_years=time_to_crqc
    )
    engine = MoscaEngine(timeline)
    
    cbom_data = []
    try:
        with open("cbom.json", "r") as f:
            cbom_data = json.load(f).get("components", [])
    except Exception:
        pass

    return engine.evaluate_risk(cbom_data)

if __name__ == "__main__":
    report = run_mosca_assessment()
    print(f"[+] Mosca Assessment Complete. Status: {report['risk_status']} (QVI Score: {report['qvi_score']})")
