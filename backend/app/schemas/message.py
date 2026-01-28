from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.message import MessageRole
from app.models.conversation import ModelType


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)
    role: MessageRole


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)


class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    conversation_id: int
    message: str = Field(..., min_length=1)
    model_type: Optional[ModelType] = None
    model_name: Optional[str] = None


class ChatResponse(BaseModel):
    message_id: int
    content: str
    role: MessageRole
    created_at: datetime
