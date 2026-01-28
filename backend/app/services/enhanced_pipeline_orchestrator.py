"""
Enhanced Pipeline Orchestrator

Replaces Level 2 & 3 detection logic with multi-dimensional detection.
Keeps Level 1, 4, 5 unchanged.
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.interaction_log import InteractionLog
from app.models.response_quality import ResponseQuality
from app.models.hallucination_detection import HallucinationDetection
from app.models.context_alignment import ContextAlignment
from app.models.safety_assessment import SafetyAssessment
from app.models.confidence_calibration import ConfidenceCalibration
from app.models.anomaly_score import AnomalyScore, AnomalyCategory

from app.services.response_quality_service import ResponseQualityService
from app.services.hallucination_detection_service import HallucinationDetectionService
from app.services.context_alignment_service import ContextAlignmentService
from app.services.safety_assessment_service import SafetyAssessmentService
from app.services.confidence_calibration_service import ConfidenceCalibrationService
from app.services.explanation_agent import ExplanationAgent

logger = logging.getLogger("pipeline")


class EnhancedPipelineOrchestrator:
    """Enhanced orchestrator with new detection logic"""

    def __init__(self, db: Session):
        self.db = db

        # Initialize all detection services
        self.quality_service = ResponseQualityService(db)
        self.hallucination_service = HallucinationDetectionService(db)
        self.alignment_service = ContextAlignmentService(db)
        self.safety_service = SafetyAssessmentService(db)
        self.confidence_service = ConfidenceCalibrationService(db)
        self.explanation_agent = ExplanationAgent()

    async def run(self, interaction_id: str) -> Dict[str, Any]:
        """
        Run enhanced detection pipeline.

        Pipeline:
        1. Load interaction (Level 1) ✓ Keep existing
        2. Run multi-dimensional detection (Level 2) ← NEW
        3. Aggregate scores (Level 3) ← NEW
        4. Generate explanation if flagged (Level 4) ✓ Keep existing
        5. Human review (Level 5) ✓ Keep existing
        """
        try:
            logger.info(f"Enhanced pipeline start interaction_id={interaction_id}")

            # LEVEL 1: Load interaction
            interaction = self.db.query(InteractionLog).filter(
                InteractionLog.id == interaction_id
            ).first()

            if not interaction:
                logger.warning(f"Enhanced pipeline missing interaction_id={interaction_id}")
                raise ValueError(f"Interaction {interaction_id} not found")

            logger.info(
                f"Enhanced pipeline loaded interaction_id={interaction.id} "
                f"model={interaction.model_name} user_id={interaction.user_id}"
            )

            # LEVEL 2: Multi-dimensional detection (run in parallel)
            detection_results = await self._run_detection_layers(interaction)

            # LEVEL 3: Aggregate scores
            anomaly_result = await self._aggregate_scores(
                interaction_id,
                detection_results
            )

            # LEVEL 4: Generate explanation if flagged
            if anomaly_result["is_anomaly"]:
                await self._generate_explanation(
                    interaction,
                    anomaly_result,
                    detection_results
                )
                logger.info(f"Enhanced pipeline explanation generated interaction_id={interaction_id}")
            else:
                logger.info(f"Enhanced pipeline skipped explanation interaction_id={interaction_id}")

            logger.info(
                f"Enhanced pipeline completed interaction_id={interaction_id} "
                f"is_anomaly={anomaly_result['is_anomaly']} "
                f"category={anomaly_result['anomaly_category']}"
            )

            return {
                "interaction_id": interaction_id,
                "is_anomaly": anomaly_result["is_anomaly"],
                "anomaly_category": anomaly_result["anomaly_category"],
                "final_score": anomaly_result["final_anomaly_score"],
                "detection_results": detection_results
            }

        except Exception as e:
            logger.error(f"Enhanced pipeline failed interaction_id={interaction_id}: {e}")
            raise

    async def _run_detection_layers(self, interaction: InteractionLog) -> Dict[str, Any]:
        """Run all 5 detection layers in parallel"""

        user_question = interaction.prompt
        ai_response = interaction.response

        logger.info(f"Running detection layers for interaction_id={interaction.id}")

        # Run detection services in parallel for speed
        # Use return_exceptions to prevent one failure from stopping all
        results = await asyncio.gather(
            self.quality_service.evaluate_quality(user_question, ai_response),
            self.hallucination_service.detect_hallucinations(user_question, ai_response),
            self.alignment_service.analyze_alignment(user_question, ai_response),
            self.safety_service.assess_safety(user_question, ai_response),
            return_exceptions=True
        )

        # Handle potential exceptions
        quality_result = results[0] if not isinstance(results[0], Exception) else self._get_default_quality()
        hallucination_result = results[1] if not isinstance(results[1], Exception) else self._get_default_hallucination()
        alignment_result = results[2] if not isinstance(results[2], Exception) else self._get_default_alignment()
        safety_result = results[3] if not isinstance(results[3], Exception) else self._get_default_safety()

        # Log any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Detection layer {i} failed: {result}")

        # Run confidence calibration (needs hallucination results)
        try:
            confidence_result = await self.confidence_service.analyze_calibration(
                user_question,
                ai_response,
                verified_claims=hallucination_result.get("verified_claims", []),
                unverified_claims=hallucination_result.get("unverified_claims", [])
            )
        except Exception as e:
            logger.error(f"Confidence calibration failed: {e}")
            confidence_result = self._get_default_confidence()

        # Save all detection results to database
        await self._save_detection_results(
            interaction.id,
            quality_result,
            hallucination_result,
            alignment_result,
            safety_result,
            confidence_result
        )

        logger.info(f"Detection layers completed for interaction_id={interaction.id}")

        return {
            "quality": quality_result,
            "hallucination": hallucination_result,
            "alignment": alignment_result,
            "safety": safety_result,
            "confidence": confidence_result
        }

    def _get_default_quality(self) -> Dict[str, Any]:
        """Return default quality scores on error"""
        return {
            "relevance_score": 0.5,
            "completeness_score": 0.5,
            "coherence_score": 0.5,
            "specificity_score": 0.5,
            "overall_quality_score": 0.5,
            "quality_issues": [],
            "strengths": [],
            "has_quality_issues": False
        }

    def _get_default_hallucination(self) -> Dict[str, Any]:
        """Return default hallucination scores on error"""
        return {
            "extracted_claims": [],
            "verified_claims": [],
            "unverified_claims": [],
            "hallucination_risk_score": 0.5,
            "hallucination_markers": [],
            "confidence_issues": [],
            "recommended_action": "review",
            "analysis_metadata": {}
        }

    def _get_default_alignment(self) -> Dict[str, Any]:
        """Return default alignment scores on error"""
        return {
            "intent_match_score": 0.5,
            "topic_relevance_score": 0.5,
            "overall_alignment_score": 0.5,
            "question_coverage": {},
            "alignment_issues": [],
            "response_category": "partial_answer",
            "explanation": "",
            "is_misaligned": False
        }

    def _get_default_safety(self) -> Dict[str, Any]:
        """Return default safety scores on error"""
        return {
            "safety_risk_score": 0.5,
            "safety_issues": [],
            "appropriate_response_given": True,
            "risk_category": "review",
            "has_critical_issues": False
        }

    def _get_default_confidence(self) -> Dict[str, Any]:
        """Return default confidence scores on error"""
        return {
            "confidence_score": 0.5,
            "appropriate_confidence": 0.5,
            "calibration_quality": 0.7,
            "overconfidence_markers": [],
            "hedging_words": [],
            "issues": [],
            "has_calibration_issues": False
        }

    async def _save_detection_results(
        self,
        interaction_id: str,
        quality: Dict,
        hallucination: Dict,
        alignment: Dict,
        safety: Dict,
        confidence: Dict
    ):
        """Save detection results to database"""

        try:
            # Save ResponseQuality
            quality_record = ResponseQuality(
                id=interaction_id,
                relevance_score=quality["relevance_score"],
                completeness_score=quality["completeness_score"],
                coherence_score=quality["coherence_score"],
                specificity_score=quality["specificity_score"],
                overall_quality_score=quality["overall_quality_score"],
                quality_issues=quality["quality_issues"],
                strengths=quality.get("strengths", []),
                has_quality_issues=quality.get("has_quality_issues", False)
            )
            self.db.add(quality_record)

            # Save HallucinationDetection
            hallucination_record = HallucinationDetection(
                id=interaction_id,
                extracted_claims=hallucination["extracted_claims"],
                verified_claims=hallucination["verified_claims"],
                unverified_claims=hallucination["unverified_claims"],
                hallucination_risk_score=hallucination["hallucination_risk_score"],
                hallucination_markers=hallucination["hallucination_markers"],
                confidence_issues=hallucination.get("confidence_issues", []),
                recommended_action=hallucination["recommended_action"],
                analysis_metadata=hallucination.get("analysis_metadata", {})
            )
            self.db.add(hallucination_record)

            # Save ContextAlignment
            alignment_record = ContextAlignment(
                id=interaction_id,
                intent_match_score=alignment["intent_match_score"],
                topic_relevance_score=alignment["topic_relevance_score"],
                overall_alignment_score=alignment["overall_alignment_score"],
                question_coverage=alignment["question_coverage"],
                alignment_issues=alignment["alignment_issues"],
                response_category=alignment["response_category"],
                explanation=alignment.get("explanation", ""),
                is_misaligned=alignment.get("is_misaligned", False)
            )
            self.db.add(alignment_record)

            # Save SafetyAssessment
            safety_record = SafetyAssessment(
                id=interaction_id,
                safety_risk_score=safety["safety_risk_score"],
                safety_issues=safety["safety_issues"],
                appropriate_response_given=safety["appropriate_response_given"],
                risk_category=safety["risk_category"]
            )
            self.db.add(safety_record)

            # Save ConfidenceCalibration
            confidence_record = ConfidenceCalibration(
                id=interaction_id,
                confidence_score=confidence["confidence_score"],
                appropriate_confidence=confidence["appropriate_confidence"],
                calibration_quality=confidence["calibration_quality"],
                overconfidence_markers=confidence["overconfidence_markers"],
                hedging_words=confidence["hedging_words"],
                issues=confidence["issues"]
            )
            self.db.add(confidence_record)

            self.db.commit()
            logger.info(f"Detection results saved for interaction_id={interaction_id}")

        except Exception as e:
            logger.error(f"Error saving detection results for interaction_id={interaction_id}: {e}")
            self.db.rollback()
            raise

    async def _aggregate_scores(
        self,
        interaction_id: str,
        detection_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate scores from all detection layers"""

        quality = detection_results["quality"]
        hallucination = detection_results["hallucination"]
        alignment = detection_results["alignment"]
        safety = detection_results["safety"]
        confidence = detection_results["confidence"]

        # Calculate dimension-specific anomaly scores
        quality_anomaly = 1.0 - quality["overall_quality_score"]
        hallucination_anomaly = hallucination["hallucination_risk_score"]
        alignment_anomaly = 1.0 - alignment["overall_alignment_score"]
        safety_anomaly = safety["safety_risk_score"]
        confidence_anomaly = 1.0 - confidence["calibration_quality"]

        # Weighted aggregation
        final_score = (
            0.15 * quality_anomaly +
            0.25 * hallucination_anomaly +
            0.20 * alignment_anomaly +
            0.30 * safety_anomaly +
            0.10 * confidence_anomaly
        )

        # Multi-dimensional thresholding
        is_anomaly = (
            final_score >= 0.65 or
            safety_anomaly >= 0.75 or
            hallucination_anomaly >= 0.70 or
            alignment_anomaly >= 0.70
        )

        # Classify anomaly type
        anomaly_category = self._classify_anomaly(
            quality_anomaly,
            hallucination_anomaly,
            alignment_anomaly,
            safety_anomaly,
            confidence_anomaly
        )

        # Save to database
        try:
            anomaly_record = AnomalyScore(
                id=interaction_id,
                quality_anomaly_score=quality_anomaly,
                hallucination_anomaly_score=hallucination_anomaly,
                alignment_anomaly_score=alignment_anomaly,
                safety_anomaly_score=safety_anomaly,
                confidence_anomaly_score=confidence_anomaly,
                final_anomaly_score=final_score,
                is_anomaly=is_anomaly,
                anomaly_category=anomaly_category.value
            )
            self.db.add(anomaly_record)
            self.db.commit()
            logger.info(
                f"Anomaly score saved interaction_id={interaction_id} "
                f"final_score={final_score:.3f} is_anomaly={is_anomaly}"
            )
        except Exception as e:
            logger.error(f"Error saving anomaly score for interaction_id={interaction_id}: {e}")
            self.db.rollback()
            raise

        return {
            "final_anomaly_score": final_score,
            "is_anomaly": is_anomaly,
            "anomaly_category": anomaly_category.value,
            "dimension_scores": {
                "quality": quality_anomaly,
                "hallucination": hallucination_anomaly,
                "alignment": alignment_anomaly,
                "safety": safety_anomaly,
                "confidence": confidence_anomaly
            }
        }

    def _classify_anomaly(
        self,
        quality: float,
        hallucination: float,
        alignment: float,
        safety: float,
        confidence: float
    ) -> AnomalyCategory:
        """Classify anomaly by dominant dimension"""

        # Priority: Safety > Hallucination > Alignment > Quality > Confidence
        if safety >= 0.75:
            return AnomalyCategory.UNSAFE_ADVICE
        elif hallucination >= 0.70:
            return AnomalyCategory.HALLUCINATION
        elif alignment >= 0.70:
            return AnomalyCategory.CONTEXT_MISMATCH
        elif quality >= 0.60:
            return AnomalyCategory.POOR_QUALITY
        elif confidence >= 0.60:
            return AnomalyCategory.CONFIDENCE_ISSUE
        else:
            return AnomalyCategory.NONE

    async def _generate_explanation(
        self,
        interaction: InteractionLog,
        anomaly_result: Dict,
        detection_results: Dict
    ):
        """Generate explanation for flagged anomaly"""

        try:
            # Create a mock scoring object for the existing explanation agent
            # This allows us to reuse the existing explanation logic
            class MockScoring:
                def __init__(self, anomaly_result, detection_results):
                    self.is_flagged = anomaly_result["is_anomaly"]
                    self.scores = anomaly_result["dimension_scores"]
                    self.flags = {
                        "quality_issues": detection_results["quality"]["has_quality_issues"],
                        "hallucination_risk": detection_results["hallucination"]["hallucination_risk_score"] >= 0.7,
                        "alignment_issues": detection_results["alignment"]["is_misaligned"],
                        "safety_issues": detection_results["safety"]["has_critical_issues"],
                        "confidence_issues": detection_results["confidence"]["has_calibration_issues"]
                    }

            mock_scoring = MockScoring(anomaly_result, detection_results)

            # Call existing explanation agent
            await self.explanation_agent.explain(
                self.db,
                interaction,
                mock_scoring
            )

            logger.info(f"Explanation generated for interaction_id={interaction.id}")

        except Exception as e:
            logger.error(f"Error generating explanation for interaction_id={interaction.id}: {e}")
            # Don't raise - explanation is optional


# Create singleton instance
def create_enhanced_orchestrator(db: Session) -> EnhancedPipelineOrchestrator:
    """Factory function to create orchestrator instance"""
    return EnhancedPipelineOrchestrator(db)
