from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.schemas.analysis import RecordAnalysisResponse
from app.schemas.scoring import ScoringRecordResponse
from app.schemas.explanation import ExplanationRecordResponse
from app.schemas.feedback import FeedbackRecordResponse


class InteractionLogBase(BaseModel):
    prompt: str
    response: str
    model_name: str
    user_id: int
    conversation_id: int
    metadata_json: Optional[Dict[str, Any]] = None


class InteractionLogCreate(InteractionLogBase):
    pass


class InteractionLogResponse(InteractionLogBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True


class InteractionDetailResponse(BaseModel):
    interaction: InteractionLogResponse
    analysis: Optional[RecordAnalysisResponse] = None
    scoring: Optional[ScoringRecordResponse] = None
    explanation: Optional[ExplanationRecordResponse] = None
    feedback: Optional[FeedbackRecordResponse] = None
