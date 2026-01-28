from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class InteractionLog:
    id: str
    prompt: str
    response: str
    model_name: str
    timestamp: str
    user_id: str
    conversation_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnalysisRecord:
    interaction_id: str
    topics: List[str] = field(default_factory=list)
    risk_context_flags: Dict[str, Any] = field(default_factory=dict)
    hallucination_hints: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScoringRecord:
    interaction_id: str
    scores: Dict[str, float] = field(default_factory=dict)
    flags: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExplanationRecord:
    interaction_id: str
    risk_type: str
    explanation: str
    citations: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FeedbackRecord:
    interaction_id: str
    human_label: str
    corrected_response: Optional[str] = None
    comments: Optional[str] = None
    timestamp: Optional[str] = None
    reviewer_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
