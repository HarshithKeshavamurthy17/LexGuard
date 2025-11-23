"""LLM abstraction layer."""

import os
import logging

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
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        logger.info(f"Using Ollama with model: {model}")
        return OllamaClient(model=model, base_url=base_url)
    elif provider == "openai":
        logger.info("Using OpenAI API")
        return OpenAIClient()
    elif provider == "gemini":
        logger.info("Using Gemini API")
        return GeminiClient()
    else:
        # Try Ollama first, fallback to OpenAI
        try:
            logger.info("Auto-detecting LLM provider...")
            return OllamaClient()
        except Exception:
            logger.warning("Ollama not available, falling back to OpenAI")
            return OpenAIClient()


__all__ = ["LLMClient", "OpenAIClient", "OllamaClient", "GeminiClient", "get_llm_client"]

