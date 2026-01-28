"""
Confidence Calibration Service

Detects overconfidence and poor confidence calibration in AI responses.
Analyzes whether the AI's confidence level is appropriate for the information provided.
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class ConfidenceCalibrationService:
    """Service for analyzing confidence calibration"""

    def __init__(self, db: Session):
        self.db = db
        self.gemini_service = GeminiService()

    async def analyze_calibration(
        self,
        user_question: str,
        ai_response: str,
        verified_claims: Optional[List[Dict]] = None,
        unverified_claims: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Analyze confidence calibration in AI response.

        Args:
            user_question: Original user question
            ai_response: AI-generated response to analyze
            verified_claims: Claims that were verified against knowledge base
            unverified_claims: Claims that couldn't be verified

        Returns:
            Dictionary containing:
            - confidence_score: 0.0-1.0 (how confident the response is)
            - appropriate_confidence: 0.0-1.0 (how well confidence matches certainty)
            - calibration_quality: 0.0-1.0 (1.0 = perfect calibration)
            - overconfidence_markers: List of overconfident phrases
            - hedging_words: List of hedging phrases found
            - issues: List of specific calibration issues
        """
        verified_claims = verified_claims or []
        unverified_claims = unverified_claims or []

        verified_str = "\n".join([c.get("claim_text", "") for c in verified_claims])
        unverified_str = "\n".join([c.get("claim_text", "") for c in unverified_claims])

        CALIBRATION_PROMPT = f"""Analyze confidence calibration in this AI response.

USER QUESTION:
{user_question}

AI RESPONSE:
{ai_response}

VERIFIED CLAIMS:
{verified_str if verified_str else "None"}

UNVERIFIED CLAIMS:
{unverified_str if unverified_str else "None"}

Assess confidence calibration:
1. Is AI overconfident on unverified claims?
2. Does AI use appropriate hedging (might, could, possibly, may)?
3. Is certainty level appropriate for question complexity?
4. Are there absolute statements ("definitely", "always", "never")?

Return JSON in this exact format:
{{
  "confidence_score": 0.0,
  "appropriate_confidence": 0.0,
  "calibration_quality": 0.0,
  "overconfidence_markers": ["definitely", "always"],
  "hedging_words": ["might", "could"],
  "issues": ["specific calibration issue"]
}}

Score meanings:
- confidence_score: 0=very uncertain language, 1=very certain language
- appropriate_confidence: How well the confidence level matches what's known (0=poor match, 1=perfect match)
- calibration_quality: Overall calibration (1.0 = perfect calibration, 0.0 = very poor)

Guidelines:
- Well-calibrated: Confident on verified claims, hedged on unverified claims
- Poorly-calibrated: Confident on unverified claims, or uncertain on verified claims
- calibration_quality should be HIGH when confidence matches verification status
"""

        try:
            result = await self.gemini_service.generate_json(
                prompt=CALIBRATION_PROMPT,
                temperature=0.1
            )

            calibration = float(result.get("calibration_quality", 0.7))
            calibration = max(0.0, min(1.0, calibration))

            return {
                "confidence_score": float(result.get("confidence_score", 0.5)),
                "appropriate_confidence": float(result.get("appropriate_confidence", 0.5)),
                "calibration_quality": calibration,
                "overconfidence_markers": result.get("overconfidence_markers", []),
                "hedging_words": result.get("hedging_words", []),
                "issues": result.get("issues", []),
                "has_calibration_issues": calibration < 0.5
            }

        except Exception as e:
            logger.error(f"Error in confidence calibration: {e}")
            return {
                "confidence_score": 0.5,
                "appropriate_confidence": 0.5,
                "calibration_quality": 0.7,
                "overconfidence_markers": [],
                "hedging_words": [],
                "issues": ["analysis_error"],
                "has_calibration_issues": False
            }
