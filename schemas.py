from typing import Literal
from pydantic import BaseModel, Field

ClaimType = Literal["statistical", "causal", "factual", "predictive", "opinion"]
Verdict = Literal["unsupported", "weak", "partial", "well_supported"]


class Claim(BaseModel):
    claim: str
    type: ClaimType
    evidence_needed: str
    gap: str
    verdict: Verdict
    hidden_assumptions: list[str] = Field(default_factory=list)
    rewritten_claim: str = ""


class Analysis(BaseModel):
    claims: list[Claim] = Field(default_factory=list)
    summary: str