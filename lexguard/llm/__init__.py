"""LLM abstraction layer."""

import logging

from lexguard.config import settings
from lexguard.llm.base import LLMClient
from lexguard.llm.openai_client import OpenAIClient
from lexguard.llm.ollama_client import OllamaClient
from lexguard.llm.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


def get_llm_client() -> LLMClient:
    """
    Get the configured LLM client.

    Checks LLM_PROVIDER environment variable:
    - "ollama" -> Use Ollama (free, local)
    - "openai" -> Use OpenAI API
    - Default -> Ollama if available, else OpenAI

    Returns:
        LLM client instance
    """
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        logger.info(f"Using Ollama with model: {settings.ollama_model}")
        return OllamaClient(
            model=settings.ollama_model, base_url=settings.ollama_base_url
        )

    if provider == "openai":
        logger.info("Using OpenAI API")
        return OpenAIClient()

    if provider == "gemini":
        logger.info("Using Gemini API")
        return GeminiClient(model=settings.gemini_model)

    logger.warning("Unknown LLM provider '%s'. Defaulting to Gemini.", provider)
    return GeminiClient(model=settings.gemini_model)


__all__ = ["LLMClient", "OpenAIClient", "OllamaClient", "GeminiClient", "get_llm_client"]

