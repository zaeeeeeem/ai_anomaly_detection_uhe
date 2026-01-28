from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.conversation import ModelType


class ConversationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    model_type: ModelType
    model_name: str


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    model_type: ModelType = ModelType.GEMINI
    model_name: str = "gemini-2.5-flash-lite"


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    model_type: Optional[ModelType] = None
    model_name: Optional[str] = None


class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    message_count: Optional[int] = 0
    last_message_preview: Optional[str] = None

    class Config:
        from_attributes = True
