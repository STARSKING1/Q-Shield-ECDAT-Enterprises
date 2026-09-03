from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class PrimitiveType(str, Enum):
    ASYMMETRIC = "asymmetric"
    SYMMETRIC = "symmetric"
    HASH = "hash"
    PQC = "post-quantum"

class QuantumSecurityLevel(str, Enum):
    VULNERABLE = "vulnerable"
    HYBRID = "hybrid_safe"
    QUANTUM_SAFE = "quantum_safe"

class AlgorithmProperties(BaseModel):
    primitive: PrimitiveType
    parameterSet: Optional[str] = None
    executionEnvironment: Optional[str] = "software"
    implementationPlatform: Optional[str] = "generic"
    classicalSecurityLevel: int
    nistQuantumSecurityLevel: int = Field(default=0, ge=0, le=5)

class CryptoProperties(BaseModel):
    assetType: str = Field(default="algorithm")
    algorithmProperties: AlgorithmProperties
    oid: Optional[str] = None

class CBOMComponent(BaseModel):
    type: str = Field(default="cryptographic")
    name: str
    version: Optional[str] = "1.0.0"
    bom_ref: str
    cryptoProperties: CryptoProperties
    evidence: Dict[str, Any] = Field(default_factory=dict)

class CycloneDX16CBOM(BaseModel):
    bomFormat: str = Field(default="CycloneDX")
    specVersion: str = Field(default="1.6")
    serialNumber: str
    version: int = 1
    components: List[CBOMComponent] = Field(default_factory=list)
