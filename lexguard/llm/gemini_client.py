"""Google Gemini LLM client."""

import os
from typing import Any, Dict, List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

def get_gemini_llm(
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
) -> ChatGoogleGenerativeAI:
    """Get a configured Google Gemini Chat model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        max_output_tokens=max_tokens,
        google_api_key=api_key,
        convert_system_message_to_human=True,
    )

def get_gemini_embeddings(
    model_name: str = "models/embedding-001",
) -> GoogleGenerativeAIEmbeddings:
    """Get configured Google Gemini embeddings."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
    return GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=api_key,
    )
