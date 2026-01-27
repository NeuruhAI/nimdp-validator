from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class TokenDef(BaseModel):
    desc: str
    weight: float
    keywords_any: List[str]
    hard_blocker: bool = False
    remediation: str

class PhaseDef(BaseModel):
    weight: float
    tokens: Dict[str, TokenDef]

class TokenResult(BaseModel):
    desc: str
    weight: float
    present: bool
    hard_blocker: bool

class Remediation(BaseModel):
    token: str
    issue: str
    fix: str

class PhaseResult(BaseModel):
    score_contrib: float
    tokens: Dict[str, TokenResult]

class ValidationResult(BaseModel):
    score: float
    status: str
    hard_block_triggered: bool
    phases: Dict[str, PhaseResult]
    remediations: List[Remediation]
    threshold: float
    hard_block_on_fail: bool
    timestamp_utc: str

class NimdpConfig(BaseModel):
    phases: Dict[str, PhaseDef]
    pass_threshold: float = 0.80
    hard_block_on_fail: bool = True
