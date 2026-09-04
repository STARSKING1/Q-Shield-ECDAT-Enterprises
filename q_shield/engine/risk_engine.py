class MoscaRiskEngine:
    def evaluate(self, findings, x=10, y=3, z=7):
        # Calculate QVI Score based on Mosca Inequality (x + y - z)
        hndl = x + y - z
        qvi_score = min(max(hndl * 10.0, 0.0), 100.0)
        
        urgency = "SAFE"
        if qvi_score >= 75:
            urgency = "CRITICAL"
        elif qvi_score >= 50:
            urgency = "HIGH"
        elif qvi_score >= 25:
            urgency = "MODERATE"

        cbom = {
            "specVersion": "1.6",
            "bomFormat": "CycloneDX",
            "components": [{"type": "cryptographic-asset", "name": f.get("primitive", "unknown")} for f in findings]
        }

        return {
            "qvi_score": qvi_score,
            "urgency": urgency,
            "cbom": cbom
        }
