"""
Context Alignment Model

Stores context alignment analysis results for AI responses.
"""

from sqlalchemy import Column, String, Float, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ContextAlignment(Base):
    """Model for storing context alignment analysis"""

    __tablename__ = "context_alignment"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Alignment scores
    intent_match_score = Column(Float, nullable=False)
    topic_relevance_score = Column(Float, nullable=False)
    overall_alignment_score = Column(Float, nullable=False)

    # Question coverage
    question_coverage = Column(JSON, nullable=False, default=dict)

    # Issues
    alignment_issues = Column(JSON, nullable=False, default=list)
    response_category = Column(String, nullable=False)  # direct_answer|partial_answer|tangential|off_topic
    explanation = Column(String, nullable=True)
    is_misaligned = Column(Boolean, default=False)

    # Metadata
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    interaction = relationship("InteractionLog", back_populates="context_alignment")
