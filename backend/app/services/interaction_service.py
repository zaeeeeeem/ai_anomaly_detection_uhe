import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.interaction_log import InteractionLog

logger = logging.getLogger("pipeline")


class InteractionService:
    def log_interaction(
        self,
        db: Session,
        *,
        prompt: str,
        response: str,
        model_name: str,
        user_id: int,
        conversation_id: int,
        metadata_json: Optional[Dict[str, Any]] = None,
    ) -> InteractionLog:
        logger.info(
            "Log interaction user_id=%s conversation_id=%s model=%s",
            user_id,
            conversation_id,
            model_name,
        )
        interaction = InteractionLog(
            prompt=prompt,
            response=response,
            model_name=model_name,
            user_id=user_id,
            conversation_id=conversation_id,
            metadata_json=metadata_json,
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        logger.info("Logged interaction id=%s", interaction.id)
        return interaction


interaction_service = InteractionService()
