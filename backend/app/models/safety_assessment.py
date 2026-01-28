"""
Safety Assessment Model

Stores safety assessment results for AI responses.
"""

from sqlalchemy import Column, String, Float, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SafetyAssessment(Base):
    """Model for storing safety assessment results"""

    __tablename__ = "safety_assessment"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Safety analysis
    safety_risk_score = Column(Float, nullable=False)
    safety_issues = Column(JSON, nullable=False, default=list)
    appropriate_response_given = Column(Boolean, default=True)
    risk_category = Column(String, nullable=False)  # safe|review|unsafe

    # Metadata
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    interaction = relationship("InteractionLog", back_populates="safety_assessment")
