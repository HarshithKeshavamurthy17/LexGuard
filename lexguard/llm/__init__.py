"""LLM abstraction layer."""

import logging

from lexguard.config import settings
from lexguard.llm.base import LLMClient

logger = logging.getLogger(__name__)


def get_llm_client() -> LLMClient:
    """
    Get the configured LLM client.

    Checks LLM_PROVIDER environment variable:
    - "ollama" -> Use Ollama (free, local)
    - "openai" -> Use OpenAI API
    - "gemini" -> Use Gemini API (default)

    Returns:
        LLM client instance
    """
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        from lexguard.llm.ollama_client import OllamaClient
        logger.info(f"Using Ollama with model: {settings.ollama_model}")
        return OllamaClient(
            model=settings.ollama_model, base_url=settings.ollama_base_url
        )

    if provider == "openai":
        from lexguard.llm.openai_client import OpenAIClient
        logger.info("Using OpenAI API")
        return OpenAIClient()

    if provider == "gemini":
        from lexguard.llm.gemini_client import GeminiClient
        logger.info("Using Gemini API")
        return GeminiClient(model=settings.gemini_model)

    # Default to Gemini
    from lexguard.llm.gemini_client import GeminiClient
    logger.warning("Unknown LLM provider '%s'. Defaulting to Gemini.", provider)
    return GeminiClient(model=settings.gemini_model)


__all__ = ["LLMClient", "get_llm_client"]

