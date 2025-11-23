"""Base LLM factory."""

from typing import Any

from lexguard.config import settings
from lexguard.llm.ollama_client import get_ollama_llm, get_ollama_embeddings
from lexguard.llm.openai_client import get_openai_llm, get_openai_embeddings
# Import Gemini
from lexguard.llm.gemini_client import get_gemini_llm, get_gemini_embeddings

def get_llm() -> Any:
    """Get the configured LLM client."""
    provider = settings.llm_provider
    
    if provider == "openai":
        return get_openai_llm(model_name=settings.openai_model)
    elif provider == "gemini":
        return get_gemini_llm(model_name=settings.gemini_model)
    elif provider == "ollama":
        return get_ollama_llm(model_name=settings.ollama_model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

def get_embeddings() -> Any:
    """Get the configured embeddings client."""
    provider = settings.embedding_provider
    
    if provider == "openai":
        return get_openai_embeddings()
    elif provider == "gemini":
        return get_gemini_embeddings()
    elif provider == "sentence-transformers":
        # Fallback to Ollama or local HF if implemented, 
        # but for now let's assume sentence-transformers uses local HF
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
