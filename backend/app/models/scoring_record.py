from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ScoringRecord(Base):
    __tablename__ = "scoring_records"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    scores = Column(JSON, nullable=False)
    flags = Column(JSON, nullable=False)
    is_flagged = Column(Boolean, nullable=False, default=False, index=True)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("InteractionLog", back_populates="scoring")
