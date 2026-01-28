from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any


class RiskContextFlags(BaseModel):
    persona_violation: bool = False
    missing_disclaimer: bool = False
    gives_medication_dosing: bool = False
    pediatric_dosing_case: bool = False
    medication_interaction_case: bool = False
    self_harm_content: bool = False
    emergency_case: bool = False
    triage_strength: str = "none"
    specialized_population: List[str] = []
    unwarranted_reassurance: bool = False
    overconfident_diagnosis: bool = False
    harmful_omission: bool = False
    misleading_equivalence: bool = False
    bad_medication_logic: bool = False
    illegal_instruction: bool = False
    high_anxiety_potential: bool = False


class HallucinationHints(BaseModel):
    overconfident_phrasing: bool = False
    risk_minimization: bool = False


class RecordAnalysisCreate(BaseModel):
    interaction_id: str
    topics: List[str]
    risk_context_flags: RiskContextFlags
    hallucination_hints: HallucinationHints


class RecordAnalysisResponse(BaseModel):
    id: str
    topics: List[str]
    risk_context_flags: Dict[str, Any]
    hallucination_hints: Dict[str, Any]
    analyzed_at: datetime

    class Config:
        from_attributes = True
