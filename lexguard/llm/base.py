"""Base LLM factory and interface."""

from typing import Any, Dict, List, Optional
from lexguard.config import settings

class LLMClient:
    """Base class for LLM clients."""
    
    def chat(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1000
    ) -> str:
        """Send a chat completion request."""
        raise NotImplementedError
        
    def chat_structured(
        self, messages: List[Dict[str, str]], schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a chat request expecting structured JSON output."""
        raise NotImplementedError

def get_llm() -> Any:
    """Get the configured LLM client."""
    provider = settings.llm_provider
    
    if provider == "openai":
        from lexguard.llm.openai_client import get_openai_llm
        return get_openai_llm(model_name=settings.openai_model)
    elif provider == "gemini":
        from lexguard.llm.gemini_client import get_gemini_llm
        return get_gemini_llm(model_name=settings.gemini_model)
    elif provider == "ollama":
        from lexguard.llm.ollama_client import get_ollama_llm
        return get_ollama_llm(model_name=settings.ollama_model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

def get_embeddings() -> Any:
    """Get the configured embeddings client."""
    provider = settings.embedding_provider
    
    if provider == "openai":
        from lexguard.llm.openai_client import get_openai_embeddings
        return get_openai_embeddings()
    elif provider == "gemini":
        from lexguard.llm.gemini_client import get_gemini_embeddings
        return get_gemini_embeddings()
    elif provider == "sentence-transformers":
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")

