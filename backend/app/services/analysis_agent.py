import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.interaction_log import InteractionLog
from app.models.record_analysis import RecordAnalysis
from app.services.gemini_service import gemini_service
from app.utils.prompts import LEVEL_2_ANALYSIS_PROMPT

logger = logging.getLogger("pipeline")


class AnalysisAgent:
    async def analyze(self, db: Session, interaction: InteractionLog) -> RecordAnalysis:
        logger.info("Level2 start interaction_id=%s", interaction.id)
        prompt = LEVEL_2_ANALYSIS_PROMPT.format(
            prompt=interaction.prompt,
            response=interaction.response,
            model_name=interaction.model_name,
        )
        analysis_data = await gemini_service.generate_json(prompt)
        logger.info(
            "Level2 response interaction_id=%s keys=%s",
            interaction.id,
            list(analysis_data.keys()),
        )

        record = RecordAnalysis(
            id=interaction.id,
            topics=analysis_data.get("topics", []),
            risk_context_flags=analysis_data.get("risk_context_flags", {}),
            hallucination_hints=analysis_data.get("hallucination_hints", {}),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info("Level2 saved interaction_id=%s", interaction.id)
        return record


analysis_agent = AnalysisAgent()
