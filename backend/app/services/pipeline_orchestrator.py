import asyncio
import logging
from app.database import SessionLocal
from app.models.interaction_log import InteractionLog
from app.services.analysis_agent import analysis_agent
from app.services.scoring_agent import scoring_agent
from app.services.explanation_agent import explanation_agent

logger = logging.getLogger("pipeline")


class PipelineOrchestrator:
    async def run(self, interaction_id: str) -> None:
        logger.info("Pipeline start interaction_id=%s", interaction_id)
        db = SessionLocal()
        try:
            interaction = (
                db.query(InteractionLog)
                .filter(InteractionLog.id == interaction_id)
                .first()
            )
            if not interaction:
                logger.warning("Pipeline missing interaction_id=%s", interaction_id)
                return
            logger.info(
                "Pipeline loaded interaction_id=%s model=%s user_id=%s",
                interaction.id,
                interaction.model_name,
                interaction.user_id,
            )

            analysis = await analysis_agent.analyze(db, interaction)
            logger.info("Pipeline analysis saved interaction_id=%s", interaction.id)

            scoring = await scoring_agent.score(db, interaction, analysis)
            logger.info(
                "Pipeline scoring saved interaction_id=%s flagged=%s",
                interaction.id,
                scoring.is_flagged,
            )

            if scoring.is_flagged:
                await explanation_agent.explain(db, interaction, scoring)
                logger.info(
                    "Pipeline explanation saved interaction_id=%s",
                    interaction.id,
                )
            else:
                logger.info(
                    "Pipeline skipped explanation interaction_id=%s",
                    interaction.id,
                )
        except Exception:
            logger.exception("Pipeline failed interaction_id=%s", interaction_id)
        finally:
            db.close()
            logger.info("Pipeline end interaction_id=%s", interaction_id)

    def run_sync(self, interaction_id: str) -> None:
        asyncio.run(self.run(interaction_id))


pipeline_orchestrator = PipelineOrchestrator()
