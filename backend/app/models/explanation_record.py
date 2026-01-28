import enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RiskType(enum.Enum):
    TRIAGE = "triage"
    DOSING = "dosing"
    DISCLAIMER = "disclaimer"
    SELF_HARM = "self_harm"
    OTHER = "other"


class ExplanationRecord(Base):
    __tablename__ = "explanation_records"

    id = Column(
        String,
        ForeignKey("interaction_logs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    risk_type = Column(
        Enum(
            RiskType,
            name="risktype",
            values_callable=lambda obj: [item.value for item in obj],
        ),
        nullable=False,
    )
    explanation = Column(Text, nullable=False)
    citations = Column(JSON, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("InteractionLog", back_populates="explanation")
