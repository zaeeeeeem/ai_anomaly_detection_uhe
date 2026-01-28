from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.interaction_log import InteractionLog
from app.schemas.interaction import InteractionDetailResponse, InteractionLogResponse
from app.schemas.analysis import RecordAnalysisResponse
from app.schemas.scoring import ScoringRecordResponse
from app.schemas.explanation import ExplanationRecordResponse
from app.schemas.feedback import FeedbackRecordResponse
from app.utils.admin_dependencies import get_current_admin_user

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])


@router.get("/{interaction_id}", response_model=InteractionDetailResponse)
def get_interaction_detail(
    interaction_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    interaction = (
        db.query(InteractionLog)
        .filter(InteractionLog.id == interaction_id)
        .first()
    )
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found",
        )

    # Try legacy tables first, then fall back to enhanced detection data
    analysis_data = None
    scoring_data = None
    explanation_data = None

    # Use legacy analysis if available
    if interaction.analysis:
        analysis_data = RecordAnalysisResponse.model_validate(interaction.analysis)
    # Otherwise, synthesize from enhanced detection data
    elif interaction.anomaly_score:
        # Build a synthetic analysis record from enhanced detection
        topics = []
        risk_context_flags = {}
        hallucination_hints = {}

        # Extract topics from context alignment if available
        if interaction.context_alignment and interaction.context_alignment.question_coverage:
            topics = list(interaction.context_alignment.question_coverage.keys())[:5]

        # Synthesize risk_context_flags from safety assessment
        if interaction.safety_assessment:
            safety = interaction.safety_assessment
            risk_context_flags = {
                "missing_disclaimer": False,
                "gives_medication_dosing": False,
                "pediatric_dosing_case": False,
                "medication_interaction_case": False,
                "self_harm_content": safety.risk_category in ["crisis", "self_harm"],
                "emergency_case": safety.risk_category == "crisis",
                "triage_strength": "high" if safety.safety_risk_score > 0.7 else "medium" if safety.safety_risk_score > 0.4 else "low",
                "specialized_population": [],
                "unwarranted_reassurance": False,
                "overconfident_diagnosis": False,
                "harmful_omission": not safety.appropriate_response_given,
                "misleading_equivalence": False,
                "bad_medication_logic": False,
                "illegal_instruction": False,
                "high_anxiety_potential": safety.risk_category == "crisis"
            }
        else:
            risk_context_flags = {
                "missing_disclaimer": False,
                "gives_medication_dosing": False,
                "pediatric_dosing_case": False,
                "medication_interaction_case": False,
                "self_harm_content": False,
                "emergency_case": False,
                "triage_strength": "none",
                "specialized_population": [],
                "unwarranted_reassurance": False,
                "overconfident_diagnosis": False,
                "harmful_omission": False,
                "misleading_equivalence": False,
                "bad_medication_logic": False,
                "illegal_instruction": False,
                "high_anxiety_potential": False
            }

        # Synthesize hallucination_hints from hallucination detection
        if interaction.hallucination_detection:
            hallucination_hints = {
                "overconfident_phrasing": interaction.hallucination_detection.hallucination_risk_score > 0.6,
                "risk_minimization": False
            }
        else:
            hallucination_hints = {
                "overconfident_phrasing": False,
                "risk_minimization": False
            }

        from app.schemas.analysis import RecordAnalysisResponse as AnalysisSchema
        analysis_data = AnalysisSchema(
            id=interaction_id,
            topics=topics,
            risk_context_flags=risk_context_flags,
            hallucination_hints=hallucination_hints,
            analyzed_at=interaction.anomaly_score.scored_at
        )

    # Use legacy scoring if available
    if interaction.scoring:
        scoring_data = ScoringRecordResponse.model_validate(interaction.scoring)
    # Otherwise, synthesize from anomaly score
    elif interaction.anomaly_score:
        from app.schemas.scoring import ScoringRecordResponse as ScoringSchema

        # Build scores dict from detection layers
        scores = {
            "overall_risk_score": interaction.anomaly_score.final_anomaly_score
        }

        if interaction.quality_analysis:
            scores["quality_score"] = interaction.quality_analysis.overall_quality_score
        if interaction.hallucination_detection:
            scores["hallucination_score"] = interaction.hallucination_detection.hallucination_risk_score
        if interaction.safety_assessment:
            scores["safety_score"] = interaction.safety_assessment.safety_risk_score
        if interaction.context_alignment:
            scores["alignment_score"] = interaction.context_alignment.overall_alignment_score
        if interaction.confidence_calibration:
            scores["confidence_score"] = interaction.confidence_calibration.confidence_score

        scoring_data = ScoringSchema(
            id=interaction_id,
            toxicity_score=scores.get("safety_score", 0.0),
            medical_accuracy_score=1.0 - scores.get("hallucination_score", 0.0),
            overall_risk_score=scores["overall_risk_score"],
            scores=scores,
            flags={},
            is_flagged=interaction.anomaly_score.is_anomaly,
            scored_at=interaction.anomaly_score.scored_at
        )

    # Use legacy explanation if available
    if interaction.explanation:
        explanation_data = ExplanationRecordResponse.model_validate(interaction.explanation)

    return InteractionDetailResponse(
        interaction=InteractionLogResponse.model_validate(interaction),
        analysis=analysis_data,
        scoring=scoring_data,
        explanation=explanation_data,
        feedback=FeedbackRecordResponse.model_validate(interaction.feedback)
        if interaction.feedback
        else None,
    )
