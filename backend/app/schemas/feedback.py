from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FeedbackRecordCreate(BaseModel):
    interaction_id: str
    human_label: str
    corrected_response: Optional[str] = None
    comments: Optional[str] = None
    reviewer_id: Optional[int] = None


class FeedbackRecordResponse(BaseModel):
    id: str
    human_label: str
    corrected_response: Optional[str]
    comments: Optional[str]
    timestamp: datetime
    reviewer_id: Optional[int]

    class Config:
        from_attributes = True
