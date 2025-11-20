"""Ollama LLM client implementation."""

import json
import logging
from typing import Dict, List, Any

import httpx

from lexguard.llm.base import LLMClient

logger = logging.getLogger(__name__)


class OllamaClient(LLMClient):
    """Ollama local LLM client implementation."""

    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client.

        Args:
            model: Model name (e.g., 'llama3.2', 'mistral', 'phi3')
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        logger.info(f"Initialized Ollama client with model: {model}")

    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1000
    ) -> str:
        """
        Send a chat completion request to Ollama.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        try:
            # Convert messages to Ollama format
            prompt = self._messages_to_prompt(messages)

            # Call Ollama API
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens,
                        },
                    },
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")

        except httpx.ConnectError:
            logger.error("Could not connect to Ollama. Is it running? Run: ollama serve")
            raise ConnectionError(
                "Ollama is not running. Please start it with: ollama serve"
            )
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
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
            # Add JSON instruction
            messages = messages.copy()
            messages[-1]["content"] += "\n\nRespond with valid JSON only, no other text."

            response_text = self.chat(messages, temperature=0.3, max_tokens=1000)

            # Try to extract JSON from response
            response_text = response_text.strip()

            # Sometimes models wrap JSON in markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            return json.loads(response_text)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Ollama response: {e}")
            # Return a fallback structure
            return {"error": "Failed to parse structured output"}
        except Exception as e:
            logger.error(f"Ollama structured API error: {e}")
            raise

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert OpenAI-style messages to a single prompt string.

        Args:
            messages: List of message dicts

        Returns:
            Formatted prompt string
        """
        prompt_parts = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)


