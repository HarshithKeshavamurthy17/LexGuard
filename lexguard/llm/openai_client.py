"""OpenAI LLM client implementation."""

import json
import logging
from typing import Dict, List, Any

from openai import OpenAI

from lexguard.config import settings
from lexguard.llm.base import LLMClient

logger = logging.getLogger(__name__)


class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""

    def __init__(self):
        """Initialize OpenAI client."""
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        logger.info(f"Initialized OpenAI client with model: {self.model}")

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
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            return content

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

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
        try:
            # Add instruction for JSON output
            messages = messages.copy()
            messages[-1]["content"] += "\n\nRespond with valid JSON only."

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for structured output
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            logger.error(f"OpenAI structured API error: {e}")
            raise


