"""
Response Quality Model

Stores quality analysis results for AI responses.
"""

from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ResponseQuality(Base):
    """Model for storing response quality analysis"""

    __tablename__ = "response_quality_analysis"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Quality scores (0.0-1.0)
    relevance_score = Column(Float, nullable=False)
    completeness_score = Column(Float, nullable=False)
    coherence_score = Column(Float, nullable=False)
    specificity_score = Column(Float, nullable=False)
    overall_quality_score = Column(Float, nullable=False)

    # Details
    quality_issues = Column(JSON, nullable=False, default=list)
    strengths = Column(JSON, nullable=False, default=list)
    has_quality_issues = Column(Boolean, default=False)

    # Metadata
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    interaction = relationship("InteractionLog", back_populates="quality_analysis")
