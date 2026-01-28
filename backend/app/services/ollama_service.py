import httpx
from typing import List, Dict, Optional
from app.config import settings


class OllamaService:
    """Service for interacting with local Ollama models"""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.OLLAMA_DEFAULT_MODEL

    async def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available Ollama models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [
                        {"name": model["name"], "size": model.get("size", "unknown")}
                        for model in data.get("models", [])
                    ]
                return []
        except Exception as e:
            print(f"Error fetching Ollama models: {str(e)}")
            return []

    async def generate_response(
        self,
        message: str,
        model_name: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None,
    ) -> str:
        """
        Generate a response using Ollama API

        Args:
            message: User's message
            model_name: Ollama model to use
            conversation_history: Previous messages for context

        Returns:
            Generated response text
        """
        if not model_name:
            model_name = self.default_model

        try:
            # Build conversation context
            context = self._build_context(conversation_history)

            # Medical system prompt
            system_prompt = (
                "You are a helpful medical assistant. Provide accurate medical\n"
                "information while reminding users to consult healthcare professionals for personal advice."
            )

            # Build prompt
            full_prompt = f"{system_prompt}\n\n{context}User: {message}\nAssistant:"

            # Make request to Ollama
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": full_prompt,
                        "stream": False,
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                else:
                    raise Exception(f"Ollama API returned status {response.status_code}")

        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")

    async def stream_response(
        self,
        message: str,
        model_name: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None,
    ):
        """
        Stream response from Ollama API

        Args:
            message: User's message
            model_name: Ollama model to use
            conversation_history: Previous messages for context

        Yields:
            Response chunks
        """
        if not model_name:
            model_name = self.default_model

        try:
            context = self._build_context(conversation_history)
            system_prompt = "You are a helpful medical assistant."

            full_prompt = f"{system_prompt}\n\n{context}User: {message}\nAssistant:"

            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": full_prompt,
                        "stream": True,
                    },
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                import json

                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            raise Exception(f"Ollama streaming error: {str(e)}")

    def _build_context(self, conversation_history: List[Dict[str, str]] = None) -> str:
        """Build conversation context from history"""
        if not conversation_history:
            return ""

        context = ""
        for msg in conversation_history[-10:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"

        return context

    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False


# Create singleton instance
ollama_service = OllamaService()
