import datetime
from typing import Any, Dict


def build_cyclonedx_cbom(
    scan_id: str,
    primitive: str,
    qvi_score: float,
    urgency: str,
    transformations_count: int,
) -> Dict[str, Any]:
    is_pqc = primitive in ["ML-KEM-768", "ML-DSA-65", "AES-256"]

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:qshield-cbom-{scan_id}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "tools": [
                {
                    "vendor": "Q-Shield Enterprise",
                    "name": "ECDAT Engine",
                    "version": "1.0.0",
                }
            ],
        },
        "components": [
            {
                "type": "cryptographic-asset",
                "bom-ref": f"crypto-asset-{scan_id}",
                "name": primitive,
                "cryptoProperties": {
                    "assetType": "algorithm",
                    "algorithmProperties": {
                        "primitive": primitive,
                        "variant": "Standard",
                        "cryptoFunctions": [
                            "key-exchange"
                            if "KEM" in primitive or "RSA" in primitive
                            else "signature"
                        ],
                    },
                },
                "properties": [
                    {"name": "qshield:qvi_score", "value": str(qvi_score)},
                    {"name": "qshield:urgency", "value": urgency},
                    {
                        "name": "qshield:refactored_ast_nodes",
                        "value": str(transformations_count),
                    },
                    {
                        "name": "qshield:pqc_compliance",
                        "value": "COMPLIANT" if is_pqc else "NON_COMPLIANT",
                    },
                ],
            }
        ],
    }

if __name__ == "__main__":
    cbom = build_cyclonedx_cbom("test-123", "RSA-2048", 87.5, "CRITICAL", 2)
    print("Generated CBOM Object:")
    print(cbom)
