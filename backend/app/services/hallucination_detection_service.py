"""
Hallucination Detection Service

Detects when AI responses contain fabricated or unverified information.

Multi-stage approach:
1. Extract factual claims from AI response
2. Verify claims against RAG knowledge base
3. Assess hallucination risk for unverified claims
"""

import json
import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.services.gemini_service import GeminiService
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)


class HallucinationDetectionService:
    """Service for detecting hallucinations in AI responses"""

    def __init__(self, db: Session):
        self.db = db
        self.gemini_service = GeminiService()
        self.rag_service = RAGService()

    async def detect_hallucinations(
        self,
        user_question: str,
        ai_response: str,
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Detect hallucinations in an AI response.

        Args:
            user_question: Original user question
            ai_response: AI-generated response to analyze
            conversation_context: Optional conversation history

        Returns:
            Dictionary containing:
            - extracted_claims: List of factual claims
            - verified_claims: Claims verified against knowledge base
            - unverified_claims: Claims that couldn't be verified
            - hallucination_risk_score: 0.0-1.0 risk score
            - hallucination_markers: Warning signs detected
            - recommended_action: flag|review|safe
        """
        try:
            # Stage 1: Extract claims
            logger.info("Stage 1: Extracting claims from AI response")
            extracted_claims = await self._extract_claims(ai_response)

            if not extracted_claims:
                # No factual claims to verify
                return self._safe_result()

            # Stage 2: Verify claims via RAG
            logger.info(f"Stage 2: Verifying {len(extracted_claims)} claims")
            verified_claims, unverified_claims = await self._verify_claims(
                extracted_claims
            )

            # Stage 3: Assess hallucination risk
            logger.info("Stage 3: Assessing hallucination risk")
            risk_assessment = await self._assess_hallucination_risk(
                ai_response=ai_response,
                unverified_claims=unverified_claims
            )

            return {
                "extracted_claims": extracted_claims,
                "verified_claims": verified_claims,
                "unverified_claims": unverified_claims,
                "hallucination_risk_score": risk_assessment["hallucination_risk_score"],
                "hallucination_markers": risk_assessment["hallucination_markers"],
                "recommended_action": risk_assessment["recommended_action"],
                "analysis_metadata": {
                    "total_claims": len(extracted_claims),
                    "verified_count": len(verified_claims),
                    "unverified_count": len(unverified_claims)
                }
            }

        except Exception as e:
            logger.error(f"Error in hallucination detection: {e}")
            return self._error_result(str(e))

    async def _extract_claims(self, ai_response: str) -> List[Dict[str, Any]]:
        """Extract factual claims from AI response using Gemini"""

        CLAIM_EXTRACTION_PROMPT = f"""Extract all factual claims from this AI response.

AI RESPONSE:
{ai_response}

For each claim, identify:
1. The specific fact being stated
2. How confidently it's presented (certain/uncertain/hedged)
3. The type of claim (medical_fact/statistical/recommendation/general)

Return JSON in this exact format:
{{
  "claims": [
    {{
      "claim_text": "specific claim as stated",
      "confidence_level": "certain|uncertain|hedged",
      "claim_type": "medical_fact|statistical|recommendation|general",
      "context": "surrounding sentence for context"
    }}
  ]
}}

Rules:
- Only extract verifiable factual claims, not opinions
- Include dosage numbers, statistics, medical facts
- Skip subjective statements and general advice
- If no claims exist, return empty array
"""

        try:
            result = await self.gemini_service.generate_json(
                prompt=CLAIM_EXTRACTION_PROMPT,
                temperature=0.1
            )

            if not result or "claims" not in result:
                logger.warning("No claims extracted from response")
                return []

            return result["claims"]

        except Exception as e:
            logger.error(f"Error extracting claims: {e}")
            return []

    async def _verify_claims(
        self,
        claims: List[Dict[str, Any]]
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Verify claims against RAG knowledge base"""

        verified_claims = []
        unverified_claims = []

        for claim in claims:
            claim_text = claim["claim_text"]

            try:
                # Query RAG for verification
                rag_results = self.rag_service.query(
                    query_text=claim_text,
                    top_k=3
                )

                # Check if any result strongly supports the claim
                verification_confidence = 0.0
                supporting_sources = []

                if rag_results:
                    for result in rag_results:
                        if result.get("score", 0.0) > 0.7:  # Strong match
                            verification_confidence = max(
                                verification_confidence,
                                result["score"]
                            )
                            supporting_sources.append({
                                "doc_id": result.get("doc_id"),
                                "score": result.get("score"),
                                "text": result.get("text", "")[:200]
                            })

                if verification_confidence >= 0.6:
                    # Claim is verified
                    verified_claims.append({
                        **claim,
                        "verification_confidence": verification_confidence,
                        "supporting_sources": supporting_sources
                    })
                else:
                    # Claim couldn't be verified
                    unverified_claims.append({
                        **claim,
                        "verification_confidence": verification_confidence,
                        "rag_results": supporting_sources if supporting_sources else None
                    })

            except Exception as e:
                logger.error(f"Error verifying claim '{claim_text}': {e}")
                unverified_claims.append({
                    **claim,
                    "verification_confidence": 0.0,
                    "error": str(e)
                })

        return verified_claims, unverified_claims

    async def _assess_hallucination_risk(
        self,
        ai_response: str,
        unverified_claims: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess overall hallucination risk for unverified claims"""

        if not unverified_claims:
            return {
                "hallucination_risk_score": 0.0,
                "hallucination_markers": [],
                "recommended_action": "safe"
            }

        HALLUCINATION_ASSESSMENT_PROMPT = f"""Review these unverified claims from an AI response.

UNVERIFIED CLAIMS:
{json.dumps(unverified_claims, indent=2)}

FULL AI RESPONSE:
{ai_response}

Assess hallucination risk by analyzing:
1. Are these claims presented as definite facts or with uncertainty?
2. Are there hedging words (might, could, possibly, may)?
3. Is the AI overconfident about information that couldn't be verified?
4. Are specific numbers/statistics given without sources?
5. Are there markers of fabrication (overly specific details, confident tone on rare topics)?

Return JSON in this exact format:
{{
  "hallucination_risk_score": 0.0,
  "hallucination_markers": ["list", "of", "specific", "warning", "signs"],
  "confidence_issues": ["overconfident phrase 1", "overconfident phrase 2"],
  "recommended_action": "flag|review|safe"
}}

Score guidelines:
- 0.0-0.3: Claims are hedged appropriately, low risk
- 0.4-0.6: Some confidence issues, medium risk
- 0.7-1.0: High confidence on unverified claims, high risk
"""

        try:
            result = await self.gemini_service.generate_json(
                prompt=HALLUCINATION_ASSESSMENT_PROMPT,
                temperature=0.1
            )

            return {
                "hallucination_risk_score": float(result.get("hallucination_risk_score", 0.5)),
                "hallucination_markers": result.get("hallucination_markers", []),
                "confidence_issues": result.get("confidence_issues", []),
                "recommended_action": result.get("recommended_action", "review")
            }

        except Exception as e:
            logger.error(f"Error assessing hallucination risk: {e}")
            return {
                "hallucination_risk_score": 0.5,
                "hallucination_markers": ["error_during_assessment"],
                "recommended_action": "review"
            }

    def _safe_result(self) -> Dict[str, Any]:
        """Return safe result when no claims to verify"""
        return {
            "extracted_claims": [],
            "verified_claims": [],
            "unverified_claims": [],
            "hallucination_risk_score": 0.0,
            "hallucination_markers": [],
            "recommended_action": "safe",
            "analysis_metadata": {
                "total_claims": 0,
                "verified_count": 0,
                "unverified_count": 0
            }
        }

    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """Return error result when analysis fails"""
        return {
            "extracted_claims": [],
            "verified_claims": [],
            "unverified_claims": [],
            "hallucination_risk_score": 0.5,  # Neutral score on error
            "hallucination_markers": ["analysis_error"],
            "recommended_action": "review",
            "analysis_metadata": {
                "error": error_message
            }
        }
