"""
Enhanced Detection Response Schemas

Pydantic schemas for API responses from the enhanced anomaly detection system.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# Response Quality Schemas
class ResponseQualityResponse(BaseModel):
    """Response quality analysis result"""

    relevance_score: float = Field(..., ge=0.0, le=1.0)
    completeness_score: float = Field(..., ge=0.0, le=1.0)
    coherence_score: float = Field(..., ge=0.0, le=1.0)
    specificity_score: float = Field(..., ge=0.0, le=1.0)
    overall_quality_score: float = Field(..., ge=0.0, le=1.0)
    quality_issues: List[str]
    strengths: List[str]
    has_quality_issues: bool
    analyzed_at: datetime

    class Config:
        from_attributes = True


# Hallucination Detection Schemas
class HallucinationDetectionResponse(BaseModel):
    """Hallucination detection result"""

    extracted_claims: List[Dict[str, Any]]
    verified_claims: List[Dict[str, Any]]
    unverified_claims: List[Dict[str, Any]]
    hallucination_risk_score: float = Field(..., ge=0.0, le=1.0)
    hallucination_markers: List[str]
    confidence_issues: List[str]
    recommended_action: str
    analysis_metadata: Optional[Dict[str, Any]] = None
    analyzed_at: datetime

    class Config:
        from_attributes = True


# Context Alignment Schemas
class ContextAlignmentResponse(BaseModel):
    """Context alignment analysis result"""

    intent_match_score: float = Field(..., ge=0.0, le=1.0)
    topic_relevance_score: float = Field(..., ge=0.0, le=1.0)
    overall_alignment_score: float = Field(..., ge=0.0, le=1.0)
    question_coverage: Dict[str, Any]
    alignment_issues: List[str]
    response_category: str
    explanation: Optional[str] = None
    is_misaligned: bool
    analyzed_at: datetime

    class Config:
        from_attributes = True


# Safety Assessment Schemas
class SafetyAssessmentResponse(BaseModel):
    """Safety assessment result"""

    safety_risk_score: float = Field(..., ge=0.0, le=1.0)
    safety_issues: List[Dict[str, Any]]
    appropriate_response_given: bool
    risk_category: str
    analyzed_at: datetime

    class Config:
        from_attributes = True


# Confidence Calibration Schemas
class ConfidenceCalibrationResponse(BaseModel):
    """Confidence calibration analysis result"""

    confidence_score: float = Field(..., ge=0.0, le=1.0)
    appropriate_confidence: float = Field(..., ge=0.0, le=1.0)
    calibration_quality: float = Field(..., ge=0.0, le=1.0)
    overconfidence_markers: List[str]
    hedging_words: List[str]
    issues: List[str]
    analyzed_at: datetime

    class Config:
        from_attributes = True


# Anomaly Score Schemas
class AnomalyScoreResponse(BaseModel):
    """Final anomaly score and classification"""

    quality_anomaly_score: float = Field(..., ge=0.0, le=1.0)
    hallucination_anomaly_score: float = Field(..., ge=0.0, le=1.0)
    alignment_anomaly_score: float = Field(..., ge=0.0, le=1.0)
    safety_anomaly_score: float = Field(..., ge=0.0, le=1.0)
    confidence_anomaly_score: float = Field(..., ge=0.0, le=1.0)
    final_anomaly_score: float = Field(..., ge=0.0, le=1.0)
    is_anomaly: bool
    anomaly_category: str
    scored_at: datetime

    class Config:
        from_attributes = True


# Detailed Analysis Response (combines all layers)
class DetailedAnalysisResponse(BaseModel):
    """Complete detailed analysis including all detection layers"""

    interaction_id: str
    prompt: str
    response: str
    model_name: str
    timestamp: datetime

    # Enhanced detection results
    quality_analysis: Optional[ResponseQualityResponse] = None
    hallucination_detection: Optional[HallucinationDetectionResponse] = None
    context_alignment: Optional[ContextAlignmentResponse] = None
    safety_assessment: Optional[SafetyAssessmentResponse] = None
    confidence_calibration: Optional[ConfidenceCalibrationResponse] = None
    anomaly_score: Optional[AnomalyScoreResponse] = None

    # Legacy fields (optional for backward compatibility)
    explanation: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# Anomaly Breakdown Response
class AnomalyCategoryCount(BaseModel):
    """Count of anomalies by category"""

    category: str
    count: int


class AnomalyBreakdownResponse(BaseModel):
    """Breakdown of anomalies by category"""

    total_anomalies: int
    breakdown: List[AnomalyCategoryCount]
    time_period: Optional[str] = None


# Analytics Response
class EnhancedMetricsResponse(BaseModel):
    """Enhanced metrics including multi-dimensional scores"""

    # Overall metrics
    total_interactions: int
    total_anomalies: int
    anomaly_rate: float

    # Dimension-specific metrics
    avg_quality_score: float
    avg_hallucination_risk: float
    avg_alignment_score: float
    avg_safety_risk: float
    avg_confidence_calibration: float

    # Category breakdown
    anomaly_breakdown: List[AnomalyCategoryCount]

    # Volume metrics
    last_24h_count: int
    last_7d_count: int


# Dimension Scores Summary (for listing views)
class DimensionScoresSummary(BaseModel):
    """Summary of dimension scores for an interaction"""

    quality: float = Field(..., ge=0.0, le=1.0)
    hallucination: float = Field(..., ge=0.0, le=1.0)
    alignment: float = Field(..., ge=0.0, le=1.0)
    safety: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)


class InteractionWithScoresResponse(BaseModel):
    """Interaction with enhanced anomaly scores"""

    id: str
    prompt: str
    response: str
    model_name: str
    timestamp: datetime
    user_id: int

    # Anomaly information
    is_anomaly: bool
    anomaly_category: str
    final_anomaly_score: float
    dimension_scores: Optional[DimensionScoresSummary] = None

    class Config:
        from_attributes = True
