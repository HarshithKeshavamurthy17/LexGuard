"""Base LLM client interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1000
    ) -> str:
        """
        Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    def chat_structured(
        self, messages: List[Dict[str, str]], schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send a chat request expecting structured JSON output.

        Args:
            messages: List of message dicts
            schema: Expected JSON schema

        Returns:
            Parsed JSON response
        """
        pass


