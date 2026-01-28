"""
Anomaly Score Model

Stores final anomaly scores and classifications for AI responses.
"""

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database import Base


class AnomalyCategory(str, Enum):
    """Enum for anomaly categories"""
    NONE = "NONE"
    UNSAFE_ADVICE = "UNSAFE_ADVICE"
    HALLUCINATION = "HALLUCINATION"
    CONTEXT_MISMATCH = "CONTEXT_MISMATCH"
    POOR_QUALITY = "POOR_QUALITY"
    CONFIDENCE_ISSUE = "CONFIDENCE_ISSUE"


class AnomalyScore(Base):
    """Model for storing final anomaly scores"""

    __tablename__ = "anomaly_scores"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Individual dimension scores
    quality_anomaly_score = Column(Float, nullable=False)
    hallucination_anomaly_score = Column(Float, nullable=False)
    alignment_anomaly_score = Column(Float, nullable=False)
    safety_anomaly_score = Column(Float, nullable=False)
    confidence_anomaly_score = Column(Float, nullable=False)

    # Final aggregated score
    final_anomaly_score = Column(Float, nullable=False)
    is_anomaly = Column(Boolean, default=False, index=True)
    anomaly_category = Column(String, default=AnomalyCategory.NONE.value)

    # Metadata
    scored_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    interaction = relationship("InteractionLog", back_populates="anomaly_score")
