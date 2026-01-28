from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RecordAnalysis(Base):
    __tablename__ = "record_analyses"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    topics = Column(JSON, nullable=False)
    risk_context_flags = Column(JSON, nullable=False)
    hallucination_hints = Column(JSON, nullable=False)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("InteractionLog", back_populates="analysis")
