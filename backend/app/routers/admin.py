from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.interaction_log import InteractionLog
from app.models.scoring_record import ScoringRecord
from app.models.feedback_record import FeedbackRecord
from app.models.anomaly_score import AnomalyScore
from app.models.response_quality import ResponseQuality
from app.models.hallucination_detection import HallucinationDetection
from app.models.context_alignment import ContextAlignment
from app.models.safety_assessment import SafetyAssessment
from app.models.confidence_calibration import ConfidenceCalibration
from app.schemas.user import UserResponse
from app.schemas.interaction import InteractionLogResponse
from app.schemas.enhanced_detection import (
    DetailedAnalysisResponse,
    AnomalyBreakdownResponse,
    AnomalyCategoryCount,
    EnhancedMetricsResponse,
    InteractionWithScoresResponse,
    DimensionScoresSummary,
)
from app.utils.admin_dependencies import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    return db.query(User).order_by(User.id.asc()).all()


@router.get("/interactions", response_model=list[InteractionLogResponse])
def list_interactions(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    return (
        db.query(InteractionLog)
        .order_by(desc(InteractionLog.timestamp))
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/interactions/flagged", response_model=list[InteractionLogResponse])
def list_flagged_interactions(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    return (
        db.query(InteractionLog)
        .join(ScoringRecord, ScoringRecord.id == InteractionLog.id)
        .filter(ScoringRecord.is_flagged.is_(True))
        .order_by(desc(InteractionLog.timestamp))
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/interactions/user/{user_id}", response_model=list[InteractionLogResponse])
def list_user_interactions(
    user_id: int,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    return (
        db.query(InteractionLog)
        .filter(InteractionLog.user_id == user_id)
        .order_by(desc(InteractionLog.timestamp))
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/metrics")
def get_metrics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    now = datetime.now(timezone.utc)
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)

    total_interactions = db.query(func.count(InteractionLog.id)).scalar() or 0
    flagged_interactions = (
        db.query(func.count(ScoringRecord.id))
        .filter(ScoringRecord.is_flagged.is_(True))
        .scalar()
        or 0
    )
    flagged_rate = (
        float(flagged_interactions) / float(total_interactions)
        if total_interactions
        else 0.0
    )

    reviewed_count = db.query(func.count(FeedbackRecord.id)).scalar() or 0

    review_time_avg = (
        db.query(
            func.avg(
                func.extract(
                    "epoch",
                    FeedbackRecord.timestamp - InteractionLog.timestamp,
                )
            )
        )
        .join(InteractionLog, InteractionLog.id == FeedbackRecord.id)
        .scalar()
    )

    last_24h_count = (
        db.query(func.count(InteractionLog.id))
        .filter(InteractionLog.timestamp >= last_24h)
        .scalar()
        or 0
    )
    last_7d_count = (
        db.query(func.count(InteractionLog.id))
        .filter(InteractionLog.timestamp >= last_7d)
        .scalar()
        or 0
    )

    return {
        "total_interactions": total_interactions,
        "flagged_interactions": flagged_interactions,
        "flagged_rate": round(flagged_rate, 4),
        "reviewed_count": reviewed_count,
        "avg_review_time_seconds": float(review_time_avg or 0.0),
        "volume": {
            "last_24h": last_24h_count,
            "last_7d": last_7d_count,
        },
    }


# ============================================================================
# ENHANCED DETECTION ENDPOINTS
# ============================================================================


@router.get("/interactions/{interaction_id}/detailed", response_model=DetailedAnalysisResponse)
def get_detailed_analysis(
    interaction_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Get detailed analysis including all detection layers for a specific interaction.

    Returns comprehensive analysis with:
    - Response quality scores
    - Hallucination detection results
    - Context alignment analysis
    - Safety assessment
    - Confidence calibration
    - Final anomaly score and classification
    """
    interaction = db.query(InteractionLog).filter(
        InteractionLog.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    # Build response with all available detection data
    return DetailedAnalysisResponse(
        interaction_id=interaction.id,
        prompt=interaction.prompt,
        response=interaction.response,
        model_name=interaction.model_name,
        timestamp=interaction.timestamp,
        quality_analysis=interaction.quality_analysis,
        hallucination_detection=interaction.hallucination_detection,
        context_alignment=interaction.context_alignment,
        safety_assessment=interaction.safety_assessment,
        confidence_calibration=interaction.confidence_calibration,
        anomaly_score=interaction.anomaly_score,
        explanation=None,  # Can add legacy explanation if needed
    )


@router.get("/analytics/anomaly-breakdown", response_model=AnomalyBreakdownResponse)
def get_anomaly_breakdown(
    time_period: Optional[str] = Query(None, regex="^(24h|7d|30d|all)$"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Get breakdown of anomalies by category.

    Query parameters:
    - time_period: Filter by time period (24h, 7d, 30d, all). Default: all

    Returns counts grouped by anomaly category:
    - UNSAFE_ADVICE
    - HALLUCINATION
    - CONTEXT_MISMATCH
    - POOR_QUALITY
    - CONFIDENCE_ISSUE
    - NONE
    """
    query = db.query(
        AnomalyScore.anomaly_category,
        func.count(AnomalyScore.id).label('count')
    ).filter(
        AnomalyScore.is_anomaly == True
    )

    # Apply time filter if specified
    if time_period and time_period != "all":
        now = datetime.now(timezone.utc)
        if time_period == "24h":
            cutoff = now - timedelta(hours=24)
        elif time_period == "7d":
            cutoff = now - timedelta(days=7)
        elif time_period == "30d":
            cutoff = now - timedelta(days=30)

        query = query.join(InteractionLog).filter(
            InteractionLog.timestamp >= cutoff
        )

    breakdown = query.group_by(AnomalyScore.anomaly_category).all()

    total_anomalies = sum(count for _, count in breakdown)

    return AnomalyBreakdownResponse(
        total_anomalies=total_anomalies,
        breakdown=[
            AnomalyCategoryCount(category=cat, count=count)
            for cat, count in breakdown
        ],
        time_period=time_period or "all"
    )


@router.get("/interactions/anomalies/by-category", response_model=list[InteractionWithScoresResponse])
def get_anomalies_by_category(
    category: str = Query(..., regex="^(UNSAFE_ADVICE|HALLUCINATION|CONTEXT_MISMATCH|POOR_QUALITY|CONFIDENCE_ISSUE|NONE)$"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Get flagged interactions filtered by anomaly category.

    Query parameters:
    - category: Anomaly category to filter by (required)
    - limit: Maximum number of results (default: 100, max: 500)
    - offset: Number of results to skip (default: 0)

    Returns interactions with enhanced anomaly scores and dimension breakdowns.
    """
    interactions = db.query(InteractionLog).join(
        AnomalyScore
    ).filter(
        AnomalyScore.is_anomaly == True,
        AnomalyScore.anomaly_category == category
    ).order_by(
        desc(InteractionLog.timestamp)
    ).offset(offset).limit(limit).all()

    # Build response with dimension scores
    results = []
    for interaction in interactions:
        if interaction.anomaly_score:
            dimension_scores = DimensionScoresSummary(
                quality=interaction.anomaly_score.quality_anomaly_score,
                hallucination=interaction.anomaly_score.hallucination_anomaly_score,
                alignment=interaction.anomaly_score.alignment_anomaly_score,
                safety=interaction.anomaly_score.safety_anomaly_score,
                confidence=interaction.anomaly_score.confidence_anomaly_score,
            )
        else:
            dimension_scores = None

        results.append(
            InteractionWithScoresResponse(
                id=interaction.id,
                prompt=interaction.prompt,
                response=interaction.response,
                model_name=interaction.model_name,
                timestamp=interaction.timestamp,
                user_id=interaction.user_id,
                is_anomaly=interaction.anomaly_score.is_anomaly if interaction.anomaly_score else False,
                anomaly_category=interaction.anomaly_score.anomaly_category if interaction.anomaly_score else "NONE",
                final_anomaly_score=interaction.anomaly_score.final_anomaly_score if interaction.anomaly_score else 0.0,
                dimension_scores=dimension_scores,
            )
        )

    return results


@router.get("/metrics/enhanced", response_model=EnhancedMetricsResponse)
def get_enhanced_metrics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Get enhanced metrics including multi-dimensional scores.

    Returns:
    - Overall interaction and anomaly counts
    - Average scores for each detection dimension
    - Breakdown of anomalies by category
    - Volume metrics (24h, 7d)
    """
    now = datetime.now(timezone.utc)
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)

    # Basic counts
    total_interactions = db.query(func.count(InteractionLog.id)).scalar() or 0
    total_anomalies = (
        db.query(func.count(AnomalyScore.id))
        .filter(AnomalyScore.is_anomaly == True)
        .scalar() or 0
    )
    anomaly_rate = (
        float(total_anomalies) / float(total_interactions)
        if total_interactions else 0.0
    )

    # Average dimension scores
    avg_scores = db.query(
        func.avg(ResponseQuality.overall_quality_score).label('avg_quality'),
        func.avg(HallucinationDetection.hallucination_risk_score).label('avg_hallucination'),
        func.avg(ContextAlignment.overall_alignment_score).label('avg_alignment'),
        func.avg(SafetyAssessment.safety_risk_score).label('avg_safety'),
        func.avg(ConfidenceCalibration.calibration_quality).label('avg_confidence'),
    ).first()

    # Anomaly breakdown
    breakdown = db.query(
        AnomalyScore.anomaly_category,
        func.count(AnomalyScore.id).label('count')
    ).filter(
        AnomalyScore.is_anomaly == True
    ).group_by(
        AnomalyScore.anomaly_category
    ).all()

    # Volume metrics
    last_24h_count = (
        db.query(func.count(InteractionLog.id))
        .filter(InteractionLog.timestamp >= last_24h)
        .scalar() or 0
    )
    last_7d_count = (
        db.query(func.count(InteractionLog.id))
        .filter(InteractionLog.timestamp >= last_7d)
        .scalar() or 0
    )

    return EnhancedMetricsResponse(
        total_interactions=total_interactions,
        total_anomalies=total_anomalies,
        anomaly_rate=round(anomaly_rate, 4),
        avg_quality_score=round(float(avg_scores.avg_quality or 0.0), 3),
        avg_hallucination_risk=round(float(avg_scores.avg_hallucination or 0.0), 3),
        avg_alignment_score=round(float(avg_scores.avg_alignment or 0.0), 3),
        avg_safety_risk=round(float(avg_scores.avg_safety or 0.0), 3),
        avg_confidence_calibration=round(float(avg_scores.avg_confidence or 0.0), 3),
        anomaly_breakdown=[
            AnomalyCategoryCount(category=cat, count=count)
            for cat, count in breakdown
        ],
        last_24h_count=last_24h_count,
        last_7d_count=last_7d_count,
    )


@router.get("/interactions/anomalies/all", response_model=list[InteractionWithScoresResponse])
def get_all_anomalies(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    min_score: Optional[float] = Query(None, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Get all flagged interactions with enhanced anomaly scores.

    Query parameters:
    - limit: Maximum number of results (default: 100, max: 500)
    - offset: Number of results to skip (default: 0)
    - min_score: Minimum anomaly score threshold (optional, 0.0-1.0)

    Returns interactions ordered by anomaly score (highest first).
    """
    query = db.query(InteractionLog).join(
        AnomalyScore
    ).filter(
        AnomalyScore.is_anomaly == True
    )

    # Apply score filter if specified
    if min_score is not None:
        query = query.filter(AnomalyScore.final_anomaly_score >= min_score)

    interactions = query.order_by(
        desc(AnomalyScore.final_anomaly_score),
        desc(InteractionLog.timestamp)
    ).offset(offset).limit(limit).all()

    # Build response with dimension scores
    results = []
    for interaction in interactions:
        if interaction.anomaly_score:
            dimension_scores = DimensionScoresSummary(
                quality=interaction.anomaly_score.quality_anomaly_score,
                hallucination=interaction.anomaly_score.hallucination_anomaly_score,
                alignment=interaction.anomaly_score.alignment_anomaly_score,
                safety=interaction.anomaly_score.safety_anomaly_score,
                confidence=interaction.anomaly_score.confidence_anomaly_score,
            )
        else:
            dimension_scores = None

        results.append(
            InteractionWithScoresResponse(
                id=interaction.id,
                prompt=interaction.prompt,
                response=interaction.response,
                model_name=interaction.model_name,
                timestamp=interaction.timestamp,
                user_id=interaction.user_id,
                is_anomaly=interaction.anomaly_score.is_anomaly if interaction.anomaly_score else False,
                anomaly_category=interaction.anomaly_score.anomaly_category if interaction.anomaly_score else "NONE",
                final_anomaly_score=interaction.anomaly_score.final_anomaly_score if interaction.anomaly_score else 0.0,
                dimension_scores=dimension_scores,
            )
        )

    return results
