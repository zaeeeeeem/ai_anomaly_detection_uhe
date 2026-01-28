from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from .anomaly_scoring import AnomalyScoringAgent
from .log_agent import LogAgent
from .ml_classifier import MLClassifier
from .misbehavior_analysis import MisbehaviorAnalysisAgent
from .schemas import AnalysisRecord, ExplanationRecord, ScoringRecord
from .storage import SQLiteStore


class WatchtowerOrchestrator:
    def __init__(
        self,
        log_agent: Optional[LogAgent] = None,
        analysis_agent: Optional[Any] = None,
        scoring_agent: Optional[Any] = None,
        rag_system: Optional[Any] = None,
        ml_classifier: Optional[MLClassifier] = None,
        alpha: float = 0.7,
        store: Optional[SQLiteStore] = None,
    ) -> None:
        self.store = store or SQLiteStore()
        self.log_agent = log_agent or LogAgent(store=self.store)
        self.analysis_agent = analysis_agent or MisbehaviorAnalysisAgent()
        self.scoring_agent = scoring_agent or AnomalyScoringAgent()
        self.rag_system = rag_system
        self.ml_classifier = ml_classifier
        self.alpha = alpha

    def run(
        self,
        filters: Optional[Dict[str, Any]] = None,
        batch_size: int = 100,
        anomaly_threshold: float = 0.75,
        mode: str = "shadow",
    ) -> Iterable[Dict[str, Any]]:
        for log in self.log_agent.stream_logs(filters=filters, batch_size=batch_size):
            analysis = None
            scores = None
            explanation = None
            intercepted = False

            if self.analysis_agent is not None:
                analysis = self.analysis_agent.analyze(log)
                if isinstance(analysis, AnalysisRecord):
                    self.store.insert_analysis(analysis, timestamp=log.timestamp)

            if self.scoring_agent is not None and analysis is not None:
                scores = self.scoring_agent.score(log, analysis)
                if self.ml_classifier is not None:
                    ml_score = self.ml_classifier.predict(log, analysis)
                    if ml_score is not None and isinstance(scores, ScoringRecord):
                        rule_score = scores.scores.get("overall_anomaly_score", 0.0)
                        final_score = self.alpha * rule_score + (1 - self.alpha) * ml_score
                        scores.scores["final_score"] = round(final_score, 3)
                if isinstance(scores, ScoringRecord):
                    self.store.insert_scoring(scores, timestamp=log.timestamp)

            effective_score = None
            if isinstance(scores, ScoringRecord):
                effective_score = scores.scores.get(
                    "final_score", scores.scores.get("overall_anomaly_score", 0.0)
                )
                if mode == "intercept" and effective_score >= anomaly_threshold:
                    intercepted = True

            if (
                self.rag_system is not None
                and isinstance(scores, ScoringRecord)
                and effective_score is not None
                and effective_score > anomaly_threshold
            ):
                explanation = self.rag_system.explain(
                    {
                        "interaction_id": log.id,
                        "prompt": log.prompt,
                        "response": log.response,
                        "flags": scores.flags,
                    }
                )
                if isinstance(explanation, ExplanationRecord):
                    self.store.insert_explanation(explanation, timestamp=log.timestamp)

            yield {
                "log": log,
                "analysis": analysis,
                "scores": scores,
                "explanation": explanation,
                "intercepted": intercepted,
            }
