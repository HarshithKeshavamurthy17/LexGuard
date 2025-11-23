"""Google Gemini LLM client."""

import json
import logging
from typing import Any, Dict, List, Optional

import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from lexguard.config import settings
from lexguard.llm.base import LLMClient

logger = logging.getLogger(__name__)

DEFAULT_GEMINI_MODEL = "models/gemini-1.5-flash-latest"


def _normalize_gemini_model_name(model_name: Optional[str]) -> str:
    """Ensure the Gemini model name uses the `models/...` syntax expected by v1beta."""
    if not model_name:
        return DEFAULT_GEMINI_MODEL

    model_name = model_name.strip()
    if model_name.startswith("models/"):
        return model_name

    return f"models/{model_name}"


class GeminiClient(LLMClient):
    """Gemini API client implementation."""

    def __init__(self, model: Optional[str] = None):
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not configured")

        genai.configure(api_key=settings.google_api_key)
        normalized_model = _normalize_gemini_model_name(model or settings.gemini_model)
        self.model_name = normalized_model
        self.client = genai.GenerativeModel(self.model_name)
        logger.info(f"Initialized Gemini client with model: {self.model_name}")

    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 800
    ) -> str:
        """Send a chat completion request to Gemini."""
        prompt = self._messages_to_prompt(messages)

        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text or ""
        except Exception as exc:
            logger.error(f"Gemini API error: {exc}")
            raise

    def chat_structured(
        self, messages: List[Dict[str, str]], schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send a chat request expecting structured JSON output.
        Gemini does not support JSON schemas directly, so we prompt the model.
        """
        messages = messages.copy()
        messages[-1]["content"] += "\n\nRespond with valid JSON only."

        raw_response = self.chat(messages, temperature=0.3, max_tokens=1200)
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            logger.warning("Gemini response was not valid JSON; returning fallback payload.")
            return {"error": "Failed to parse structured output", "raw": raw_response}

    @staticmethod
    def _messages_to_prompt(messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a Gemini-friendly prompt."""
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
            else:
                prompt_parts.append(f"User: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)


def get_gemini_llm(
    model_name: str = DEFAULT_GEMINI_MODEL,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
) -> genai.GenerativeModel:
    """Backwards-compatible helper to create a raw Gemini model."""
    genai.configure(api_key=settings.google_api_key)
    normalized_model = _normalize_gemini_model_name(model_name)
    return genai.GenerativeModel(normalized_model)


def get_gemini_embeddings(
    model_name: str = "models/embedding-001",
) -> GoogleGenerativeAIEmbeddings:
    """Get configured Google Gemini embeddings."""
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    return GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=settings.google_api_key,
    )
