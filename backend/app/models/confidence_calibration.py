"""
Confidence Calibration Model

Stores confidence calibration analysis results for AI responses.
"""

from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ConfidenceCalibration(Base):
    """Model for storing confidence calibration analysis"""

    __tablename__ = "confidence_calibration"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Confidence analysis
    confidence_score = Column(Float, nullable=False)  # 0=uncertain, 1=certain
    appropriate_confidence = Column(Float, nullable=False)
    calibration_quality = Column(Float, nullable=False)  # 1.0 = perfect calibration

    # Markers
    overconfidence_markers = Column(JSON, nullable=False, default=list)
    hedging_words = Column(JSON, nullable=False, default=list)
    issues = Column(JSON, nullable=False, default=list)

    # Metadata
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    interaction = relationship("InteractionLog", back_populates="confidence_calibration")
