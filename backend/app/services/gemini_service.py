import json
import logging
import re
import google.generativeai as genai
from typing import List, Dict, Any
from app.config import settings

logger = logging.getLogger("pipeline")

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Service for interacting with Google Gemini API"""

    def __init__(self):
        self.available_models = [
            "gemini-2.5-flash-lite",
        ]

    def get_available_models(self) -> List[str]:
        """Get list of available Gemini models"""
        return self.available_models

    async def generate_response(
        self,
        message: str,
        model_name: str = "gemini-2.5-flash-lite",
        conversation_history: List[Dict[str, str]] = None,
    ) -> str:
        """
        Generate a response using Gemini API

        Args:
            message: User's message
            model_name: Gemini model to use
            conversation_history: Previous messages for context

        Returns:
            Generated response text
        """
        try:
            model = genai.GenerativeModel(model_name)

            # Build context from conversation history
            if conversation_history:
                history_text = "\n".join(
                    [
                        f"{msg['role']}: {msg['content']}"
                        for msg in conversation_history[-10:]
                    ]
                )
                full_prompt = f"{history_text}\nuser: {message}\nassistant:"
            else:
                full_prompt = message

            # Add medical context system prompt
            system_prompt = (
                "You are a helpful medical assistant AI.\n"
                # "Provide accurate,\n"
                # "evidence-based medical information. Always remind users to consult with healthcare\n"
                # "professionals for personal medical advice. Do not provide diagnoses or treatment\n"
                # "recommendations without proper medical consultation."
            )

            full_prompt = f"{system_prompt}\n\n{full_prompt}"

            # Generate response
            response = model.generate_content(full_prompt)

            return response.text

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def stream_response(
        self,
        message: str,
        model_name: str = "gemini-2.5-flash-lite",
        conversation_history: List[Dict[str, str]] = None,
    ):
        """
        Stream response from Gemini API (for future WebSocket implementation)

        Args:
            message: User's message
            model_name: Gemini model to use
            conversation_history: Previous messages for context

        Yields:
            Response chunks
        """
        try:
            model = genai.GenerativeModel(model_name)

            # Build context
            if conversation_history:
                history_text = "\n".join(
                    [
                        f"{msg['role']}: {msg['content']}"
                        for msg in conversation_history[-10:]
                    ]
                )
                full_prompt = f"{history_text}\nuser: {message}\nassistant:"
            else:
                full_prompt = message

            system_prompt = (
                "You are a helpful medical assistant AI.\n"
                "Provide accurate,\n"
                "evidence-based medical information."
            )

            full_prompt = f"{system_prompt}\n\n{full_prompt}"

            # Stream response
            response = model.generate_content(full_prompt, stream=True)

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            raise Exception(f"Gemini streaming error: {str(e)}")

    async def generate_json(
        self,
        prompt: str,
        model_name: str | None = None,
        temperature: float | None = None,
    ) -> Dict[str, Any]:
        """Generate a strict JSON response from Gemini."""
        json_prompt = (
            "Return ONLY valid JSON. Do not include markdown fences.\n\n"
            f"{prompt}"
        )
        generation_config = genai.GenerationConfig(
            temperature=settings.GEMINI_TEMPERATURE
            if temperature is None
            else temperature,
        )

        def _extract_json(text: str) -> Dict[str, Any]:
            if not text:
                raise json.JSONDecodeError("Empty response", text, 0)
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", text, re.DOTALL)
                if match:
                    return json.loads(match.group(0))
                raise

        def _run_request(target_model: str) -> Dict[str, Any]:
            logger.info("Gemini JSON request model=%s", target_model)
            model = genai.GenerativeModel(target_model)
            response = model.generate_content(
                json_prompt,
                generation_config=generation_config,
            )
            if not response.text:
                raise Exception("Empty JSON response from Gemini")
            logger.info("Gemini JSON response bytes=%s", len(response.text))
            return _extract_json(response.text)

        try:
            return _run_request(model_name or settings.GEMINI_JSON_MODEL)
        except json.JSONDecodeError as exc:
            logger.exception("Gemini JSON parse error")
            raise Exception(f"Gemini JSON parse error: {str(exc)}") from exc
        except Exception as exc:
            message = str(exc)
            if "is not found" in message or "not supported for generateContent" in message:
                fallback = "gemini-2.5-flash-lite"
                logger.warning("Gemini JSON model failed, retrying with %s", fallback)
                return _run_request(fallback)
            logger.exception("Gemini JSON error")
            raise Exception(f"Gemini JSON error: {message}") from exc

# Create singleton instance
gemini_service = GeminiService()
