import json
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_cbom(findings: list, risk_evaluation: dict) -> dict:
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "version": 1,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "tools": [{"vendor": "Q-Shield", "name": "ECDAT", "version": "1.0.0"}]
            },
            "components": [
                {
                    "type": "cryptographic-asset",
                    "name": f.get("algorithm", "Unknown"),
                    "cryptoProperties": {
                        "assetType": "algorithm",
                        "primitive": f.get("primitive", "public-key"),
                        "qlc": {"score": risk_evaluation.get("qvi", 0)}
                    }
                } for f in findings
            ]
        }

    @staticmethod
    def generate_sarif(findings: list) -> dict:
        return {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "Q-Shield ECDAT",
                            "version": "1.0.0",
                            "rules": [
                                {
                                    "id": "QS001",
                                    "name": "QuantumVulnerablePrimitive",
                                    "shortDescription": {"text": "Usage of quantum-vulnerable cryptographic algorithm."}
                                }
                            ]
                        }
                    },
                    "results": [
                        {
                            "ruleId": "QS001",
                            "message": {"text": f"Vulnerable algorithm detected: {f.get('algorithm')}"},
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": f.get("file", "unknown")},
                                        "region": {"startLine": f.get("line", 1)}
                                    }
                                }
                            ]
                        } for f in findings
                    ]
                }
            ]
        }
