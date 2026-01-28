import enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class HumanLabel(enum.Enum):
    SAFE = "SAFE"
    UNSAFE = "UNSAFE"
    BORDERLINE = "BORDERLINE"


class FeedbackRecord(Base):
    __tablename__ = "feedback_records"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    human_label = Column(Enum(HumanLabel), nullable=False)
    corrected_response = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    interaction = relationship("InteractionLog", back_populates="feedback")
    reviewer = relationship("User")
