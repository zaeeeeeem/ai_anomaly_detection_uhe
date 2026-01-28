import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.interaction_log import InteractionLog
from app.models.scoring_record import ScoringRecord
from app.models.explanation_record import ExplanationRecord, RiskType
from app.services.gemini_service import gemini_service
from app.services.rag_service import rag_service
from app.utils.prompts import LEVEL_4_EXPLANATION_PROMPT

logger = logging.getLogger("pipeline")


def _format_context(hits: List[Dict[str, Any]]) -> str:
    if not hits:
        return "No relevant documents found."
    lines = []
    for hit in hits:
        lines.append(
            f"[doc_id={hit.get('doc_id')}, chunk_id={hit.get('chunk_id')}, score={hit.get('score'):.2f}]\n{hit.get('text')}"
        )
    return "\n\n".join(lines)


class ExplanationAgent:
    async def explain(
        self,
        db: Session,
        interaction: InteractionLog,
        scoring: ScoringRecord,
    ) -> ExplanationRecord:
        logger.info("Level4 start interaction_id=%s", interaction.id)
        query_text = f"{interaction.prompt}\n{interaction.response}"
        hits = rag_service.query(query_text, top_k=5)
        logger.info("Level4 RAG hits interaction_id=%s count=%s", interaction.id, len(hits))
        prompt = LEVEL_4_EXPLANATION_PROMPT.format(
            prompt=interaction.prompt,
            response=interaction.response,
            scores=scoring.scores,
            flags=scoring.flags,
            retrieved_context=_format_context(hits),
        )
        explanation_data = await gemini_service.generate_json(prompt)
        logger.info(
            "Level4 response interaction_id=%s keys=%s",
            interaction.id,
            list(explanation_data.keys()),
        )

        risk_type_value = str(explanation_data.get("risk_type", "other")).strip().lower()
        logger.info(
            "Level4 risk_type raw=%s normalized=%s",
            explanation_data.get("risk_type"),
            risk_type_value,
        )
        try:
            risk_type = RiskType(risk_type_value)
        except ValueError:
            risk_type = RiskType.OTHER

        citations = explanation_data.get("citations", [])
        if not citations and hits:
            citations = [
                {
                    "doc_id": hit.get("doc_id"),
                    "chunk_id": hit.get("chunk_id"),
                    "score": hit.get("score"),
                }
                for hit in hits
            ]

        record = ExplanationRecord(
            id=interaction.id,
            risk_type=risk_type,
            explanation=explanation_data.get("explanation", ""),
            citations=citations,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info("Level4 saved interaction_id=%s", interaction.id)
        return record


explanation_agent = ExplanationAgent()
