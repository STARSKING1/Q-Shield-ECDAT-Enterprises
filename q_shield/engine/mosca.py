import json
from dataclasses import dataclass

@dataclass
class MoscaAssessment:
    data_shelf_life_x: float
    migration_time_y: float
    time_to_crqc_z: float

    def evaluate(self) -> dict:
        is_vulnerable = (self.data_shelf_life_x + self.migration_time_y) > self.time_to_crqc_z
        qvi_score = min(100.0, max(0.0, ((self.data_shelf_life_x + self.migration_time_y) / max(0.1, self.time_to_crqc_z)) * 50))
        
        report = {
            "mosca_inequality": f"{self.data_shelf_life_x} + {self.migration_time_y} > {self.time_to_crqc_z}",
            "quantum_vulnerable": is_vulnerable,
            "qvi_score": round(qvi_score, 2),
            "urgency": "CRITICAL" if is_vulnerable else "MODERATE"
        }
        with open("risk_report.json", "w") as f:
            json.dump(report, f, indent=2)
        return report
