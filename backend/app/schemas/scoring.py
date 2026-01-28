from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any


class Scores(BaseModel):
    safety_risk: float = Field(ge=0.0, le=1.0)
    factuality_risk: float = Field(ge=0.0, le=1.0)
    triage_risk: float = Field(ge=0.0, le=1.0)
    medication_dosing_risk: float = Field(ge=0.0, le=1.0)
    anxiety_inducing_risk: float = Field(ge=0.0, le=1.0)
    overall_anomaly_score: float = Field(ge=0.0, le=1.0)


class ScoringRecordCreate(BaseModel):
    interaction_id: str
    scores: Scores
    flags: Dict[str, Any]
    is_flagged: bool


class ScoringRecordResponse(BaseModel):
    id: str
    scores: Dict[str, Any]
    flags: Dict[str, Any]
    is_flagged: bool
    scored_at: datetime

    class Config:
        from_attributes = True
