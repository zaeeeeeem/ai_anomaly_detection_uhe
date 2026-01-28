from __future__ import annotations

from typing import Optional

from .schemas import AnalysisRecord, InteractionLog


class MLClassifier:
    """Placeholder ML classifier for Phase 5 hybrid scoring."""

    def predict(self, log: InteractionLog, analysis: AnalysisRecord) -> Optional[float]:
        return None
