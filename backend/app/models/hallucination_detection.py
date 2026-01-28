"""
Hallucination Detection Model

Stores hallucination detection results for AI responses.
"""

from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class HallucinationDetection(Base):
    """Model for storing hallucination detection results"""

    __tablename__ = "hallucination_detection"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Claims analysis
    extracted_claims = Column(JSON, nullable=False, default=list)
    verified_claims = Column(JSON, nullable=False, default=list)
    unverified_claims = Column(JSON, nullable=False, default=list)

    # Risk assessment
    hallucination_risk_score = Column(Float, nullable=False)
    hallucination_markers = Column(JSON, nullable=False, default=list)
    confidence_issues = Column(JSON, nullable=False, default=list)
    recommended_action = Column(String, nullable=False)  # flag|review|safe

    # Metadata
    analysis_metadata = Column(JSON, nullable=True)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    interaction = relationship("InteractionLog", back_populates="hallucination_detection")
