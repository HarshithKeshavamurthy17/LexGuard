"""No-op LLM client for when LLM is disabled."""

import logging
from typing import Any, Dict, List

from lexguard.llm.base import LLMClient

logger = logging.getLogger(__name__)


class NoneClient(LLMClient):
    """Dummy LLM client that always fails gracefully."""

    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1000
    ) -> str:
        """
        Always raises an exception to trigger rule-based fallback.
        """
        raise RuntimeError("LLM is disabled. Use rule-based fallback.")

    def chat_structured(
        self, messages: List[Dict[str, str]], schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Always raises an exception to trigger rule-based fallback.
        """
        raise RuntimeError("LLM is disabled. Use rule-based fallback.")

