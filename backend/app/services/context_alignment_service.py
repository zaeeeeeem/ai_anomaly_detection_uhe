"""
Context Alignment Service

Detects when AI responses don't properly address the user's question.

Analyzes:
1. Intent matching - Does response address what user wanted to know?
2. Topic relevance - Is response on-topic or did it drift?
3. Question coverage - Are all parts of multi-part questions answered?
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class ContextAlignmentService:
    """Service for analyzing context alignment between question and response"""

    def __init__(self, db: Session):
        self.db = db
        self.gemini_service = GeminiService()

    async def analyze_alignment(
        self,
        user_question: str,
        ai_response: str,
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Analyze if AI response properly addresses the user's question.

        Args:
            user_question: Original user question
            ai_response: AI-generated response to analyze
            conversation_context: Optional conversation history

        Returns:
            Dictionary containing:
            - intent_match_score: 0.0-1.0 (how well response matches intent)
            - topic_relevance_score: 0.0-1.0 (how relevant response is)
            - question_coverage: Analysis of multi-part question coverage
            - alignment_issues: List of specific misalignments
            - response_category: Classification of response type
        """
        try:
            # Build context if available
            context_str = ""
            if conversation_context:
                context_str = "\n\nCONVERSATION HISTORY:\n"
                for msg in conversation_context[-5:]:  # Last 5 messages
                    role = msg.get("role", "unknown")
                    content = msg.get("content", "")
                    context_str += f"{role.upper()}: {content}\n"

            CONTEXT_ALIGNMENT_PROMPT = f"""Analyze if the AI response properly addresses the user's question.

USER QUESTION:
{user_question}

AI RESPONSE:
{ai_response}
{context_str}

Evaluate on these dimensions:

1. INTENT MATCH (0.0-1.0):
   - Does the response address what the user actually wanted to know?
   - Is the core question answered or deflected?
   - Score: 1.0 = perfectly addresses intent, 0.0 = completely misses intent

2. TOPIC RELEVANCE (0.0-1.0):
   - Is the response on-topic or did it drift to unrelated topics?
   - Does it stay focused on the user's concern?
   - Score: 1.0 = perfectly relevant, 0.0 = completely off-topic

3. QUESTION COVERAGE:
   - If multi-part question: Are all parts answered?
   - If single question: Is it comprehensively answered?
   - Identify: Total parts, answered parts, missing parts

4. ALIGNMENT ISSUES:
   - What specific misalignments exist?
   - What did user ask for vs. what AI provided?

5. RESPONSE CATEGORY:
   - direct_answer: Directly answers the question
   - partial_answer: Answers some but not all parts
   - tangential: Related but doesn't directly answer
   - off_topic: Unrelated to the question

Return JSON in this exact format:
{{
  "intent_match_score": 0.0,
  "topic_relevance_score": 0.0,
  "question_coverage": {{
    "is_multi_part": false,
    "total_parts": 1,
    "answered_parts": 0,
    "missing_parts": ["description of missing parts"]
  }},
  "alignment_issues": ["specific issue 1", "specific issue 2"],
  "response_category": "direct_answer|partial_answer|tangential|off_topic",
  "explanation": "Brief explanation of alignment quality"
}}
"""

            result = await self.gemini_service.generate_json(
                prompt=CONTEXT_ALIGNMENT_PROMPT,
                temperature=0.1
            )

            # Validate and normalize scores
            intent_score = float(result.get("intent_match_score", 0.5))
            relevance_score = float(result.get("topic_relevance_score", 0.5))

            # Ensure scores are in valid range
            intent_score = max(0.0, min(1.0, intent_score))
            relevance_score = max(0.0, min(1.0, relevance_score))

            # Calculate overall alignment score
            overall_alignment_score = (intent_score + relevance_score) / 2.0

            return {
                "intent_match_score": intent_score,
                "topic_relevance_score": relevance_score,
                "overall_alignment_score": overall_alignment_score,
                "question_coverage": result.get("question_coverage", {
                    "is_multi_part": False,
                    "total_parts": 1,
                    "answered_parts": 1,
                    "missing_parts": []
                }),
                "alignment_issues": result.get("alignment_issues", []),
                "response_category": result.get("response_category", "unknown"),
                "explanation": result.get("explanation", ""),
                "is_misaligned": overall_alignment_score < 0.5
            }

        except Exception as e:
            logger.error(f"Error in context alignment analysis: {e}")
            return self._error_result(str(e))

    async def analyze_multi_turn_consistency(
        self,
        conversation_history: List[Dict[str, str]],
        current_response: str
    ) -> Dict[str, Any]:
        """
        Analyze if current response is consistent with conversation history.

        Args:
            conversation_history: List of previous messages
            current_response: Current AI response to check

        Returns:
            Dictionary containing:
            - consistency_score: 0.0-1.0
            - contradictions: List of contradictions found
            - context_drift: Whether conversation drifted off-topic
        """
        if not conversation_history or len(conversation_history) < 2:
            return {
                "consistency_score": 1.0,
                "contradictions": [],
                "context_drift": False,
                "note": "Insufficient history for consistency check"
            }

        try:
            # Build conversation summary
            history_text = "\n".join([
                f"{msg.get('role', '').upper()}: {msg.get('content', '')}"
                for msg in conversation_history
            ])

            CONSISTENCY_PROMPT = f"""Analyze if the current AI response is consistent with the conversation history.

CONVERSATION HISTORY:
{history_text}

CURRENT AI RESPONSE:
{current_response}

Check for:
1. CONTRADICTIONS: Does current response contradict earlier statements?
2. CONTEXT DRIFT: Has the conversation drifted away from original topic?
3. CONTINUITY: Does response build on previous context appropriately?

Return JSON:
{{
  "consistency_score": 0.0,
  "contradictions": ["contradiction 1", "contradiction 2"],
  "context_drift": false,
  "drift_explanation": "why topic drifted if applicable"
}}

Score: 1.0 = perfectly consistent, 0.0 = major contradictions
"""

            result = await self.gemini_service.generate_json(
                prompt=CONSISTENCY_PROMPT,
                temperature=0.1
            )

            consistency_score = float(result.get("consistency_score", 1.0))
            consistency_score = max(0.0, min(1.0, consistency_score))

            return {
                "consistency_score": consistency_score,
                "contradictions": result.get("contradictions", []),
                "context_drift": result.get("context_drift", False),
                "drift_explanation": result.get("drift_explanation", ""),
                "has_issues": consistency_score < 0.7 or result.get("context_drift", False)
            }

        except Exception as e:
            logger.error(f"Error in multi-turn consistency analysis: {e}")
            return {
                "consistency_score": 1.0,
                "contradictions": [],
                "context_drift": False,
                "error": str(e)
            }

    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """Return error result when analysis fails"""
        return {
            "intent_match_score": 0.5,  # Neutral score on error
            "topic_relevance_score": 0.5,
            "overall_alignment_score": 0.5,
            "question_coverage": {
                "is_multi_part": False,
                "total_parts": 1,
                "answered_parts": 1,
                "missing_parts": []
            },
            "alignment_issues": ["analysis_error"],
            "response_category": "unknown",
            "explanation": f"Error during analysis: {error_message}",
            "is_misaligned": False,
            "error": error_message
        }
