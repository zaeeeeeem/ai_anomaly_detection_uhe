from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class Citation(BaseModel):
    doc_id: str
    chunk_id: str
    score: float


class ExplanationRecordCreate(BaseModel):
    interaction_id: str
    risk_type: str
    explanation: str
    citations: List[Citation]


class ExplanationRecordResponse(BaseModel):
    id: str
    risk_type: str
    explanation: str
    citations: List[Dict]
    generated_at: datetime

    class Config:
        from_attributes = True
