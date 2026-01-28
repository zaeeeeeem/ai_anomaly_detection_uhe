"""
Response Quality Service

Evaluates the overall quality of AI responses regardless of content.

Metrics:
1. Relevance - Does response address the question?
2. Completeness - Are all question parts answered?
3. Coherence - Is response logically structured?
4. Specificity - Is response specific or vague/generic?
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class ResponseQualityService:
    """Service for evaluating AI response quality"""

    def __init__(self, db: Session):
        self.db = db
        self.gemini_service = GeminiService()

    async def evaluate_quality(
        self,
        user_question: str,
        ai_response: str
    ) -> Dict[str, Any]:
        """
        Evaluate the quality of an AI response.

        Args:
            user_question: Original user question
            ai_response: AI-generated response to evaluate

        Returns:
            Dictionary containing:
            - relevance_score: 0.0-1.0
            - completeness_score: 0.0-1.0
            - coherence_score: 0.0-1.0
            - specificity_score: 0.0-1.0
            - overall_quality_score: 0.0-1.0 (average)
            - quality_issues: List of specific problems
        """
        try:
            QUALITY_EVALUATION_PROMPT = f"""Analyze this AI response for quality issues.

USER QUESTION:
{user_question}

AI RESPONSE:
{ai_response}

Evaluate on these dimensions (0.0 = poor, 1.0 = excellent):

1. RELEVANCE (0.0-1.0):
   - Does the response directly address the user's question?
   - Is it on-topic and focused?
   - Score: 1.0 = highly relevant, 0.0 = completely irrelevant

2. COMPLETENESS (0.0-1.0):
   - Are all parts of the question answered?
   - Is the answer thorough without being excessive?
   - Score: 1.0 = fully complete, 0.0 = missing major parts

3. COHERENCE (0.0-1.0):
   - Is the response logically structured and clear?
   - Is it easy to understand?
   - Are ideas connected smoothly?
   - Score: 1.0 = very coherent, 0.0 = confusing/disjointed

4. SPECIFICITY (0.0-1.0):
   - Does it provide specific information vs. vague generalities?
   - Are concrete details included where appropriate?
   - Score: 1.0 = appropriately specific, 0.0 = overly vague

Return JSON in this exact format:
{{
  "relevance_score": 0.0,
  "completeness_score": 0.0,
  "coherence_score": 0.0,
  "specificity_score": 0.0,
  "quality_issues": ["specific issue 1", "specific issue 2"],
  "strengths": ["strength 1", "strength 2"]
}}
"""

            result = await self.gemini_service.generate_json(
                prompt=QUALITY_EVALUATION_PROMPT,
                temperature=0.1
            )

            # Extract and validate scores
            relevance = float(result.get("relevance_score", 0.5))
            completeness = float(result.get("completeness_score", 0.5))
            coherence = float(result.get("coherence_score", 0.5))
            specificity = float(result.get("specificity_score", 0.5))

            # Ensure all scores in valid range
            relevance = max(0.0, min(1.0, relevance))
            completeness = max(0.0, min(1.0, completeness))
            coherence = max(0.0, min(1.0, coherence))
            specificity = max(0.0, min(1.0, specificity))

            # Calculate overall quality score (weighted average)
            overall_quality = (
                relevance * 0.35 +        # Relevance is most important
                completeness * 0.30 +     # Then completeness
                coherence * 0.20 +        # Then coherence
                specificity * 0.15        # Then specificity
            )

            return {
                "relevance_score": relevance,
                "completeness_score": completeness,
                "coherence_score": coherence,
                "specificity_score": specificity,
                "overall_quality_score": overall_quality,
                "quality_issues": result.get("quality_issues", []),
                "strengths": result.get("strengths", []),
                "has_quality_issues": overall_quality < 0.5 or any([
                    relevance < 0.5,
                    completeness < 0.4,
                    coherence < 0.5
                ])
            }

        except Exception as e:
            logger.error(f"Error in quality evaluation: {e}")
            return self._error_result(str(e))

    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """Return neutral result when analysis fails"""
        return {
            "relevance_score": 0.5,
            "completeness_score": 0.5,
            "coherence_score": 0.5,
            "specificity_score": 0.5,
            "overall_quality_score": 0.5,
            "quality_issues": ["analysis_error"],
            "strengths": [],
            "has_quality_issues": False,
            "error": error_message
        }
