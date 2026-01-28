import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    metadata_json = Column(JSON, nullable=True)

    user = relationship("User")
    conversation = relationship("Conversation")

    # Legacy relationships (kept for backward compatibility)
    analysis = relationship(
        "RecordAnalysis",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    scoring = relationship(
        "ScoringRecord",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    explanation = relationship(
        "ExplanationRecord",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    feedback = relationship(
        "FeedbackRecord",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # New enhanced detection relationships
    quality_analysis = relationship(
        "ResponseQuality",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    hallucination_detection = relationship(
        "HallucinationDetection",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    context_alignment = relationship(
        "ContextAlignment",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    safety_assessment = relationship(
        "SafetyAssessment",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    confidence_calibration = relationship(
        "ConfidenceCalibration",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
    anomaly_score = relationship(
        "AnomalyScore",
        back_populates="interaction",
        uselist=False,
        cascade="all, delete-orphan",
    )
