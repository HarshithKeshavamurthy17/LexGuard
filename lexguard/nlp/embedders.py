"""Text embedding utilities."""

import logging
import os
from typing import List

from lexguard.config import settings

logger = logging.getLogger(__name__)

# Check availability of sentence_transformers
try:
    import sentence_transformers
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

# Default local-friendly model for sentence-transformers
DEFAULT_ST_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Cache for embedding model
_embedding_model = None


def _resolve_sentence_transformer_model_name() -> str:
    """Return a valid SentenceTransformer model name regardless of env overrides."""
    model_name = (settings.embedding_model or "").strip()
    if not model_name or model_name.startswith("models/"):
        return DEFAULT_ST_MODEL
    return model_name


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for text.
    """
    provider = settings.embedding_provider
    logger.info(f"Generating embedding using provider: '{provider}'")
    
    if provider == "openai":
        return _get_openai_embedding(text)
    elif provider == "gemini":
        return _get_gemini_embedding(text)
    elif provider == "sentence-transformers" and HAS_SENTENCE_TRANSFORMERS:
        return _get_sentence_transformer_embedding(text)
    else:
        # Fallback
        if provider == "sentence-transformers":
            logger.warning("sentence-transformers requested but not installed. Falling back to Gemini.")
        else:
            logger.warning(f"Unknown or missing provider '{provider}'. Defaulting to Gemini.")
        return _get_gemini_embedding(text)


def _get_sentence_transformer_embedding(text: str) -> List[float]:
    """Get embedding using SentenceTransformers."""
    global _embedding_model

    if not HAS_SENTENCE_TRANSFORMERS:
        raise ImportError("sentence_transformers is not installed")

    if _embedding_model is None:
        model_name = _resolve_sentence_transformer_model_name()
        logger.info(f"Loading embedding model: {model_name}")
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(model_name)

    embedding = _embedding_model.encode(text, convert_to_tensor=False)
    return embedding.tolist()


def _get_openai_embedding(text: str) -> List[float]:
    """Get embedding using OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding


def _get_gemini_embedding(text: str) -> List[float]:
    """Get embedding using Google Gemini."""
    from lexguard.llm.gemini_client import get_gemini_embeddings
    
    embeddings = get_gemini_embeddings(model_name=settings.embedding_model)
    return embeddings.embed_query(text)


def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently.
    """
    provider = settings.embedding_provider
    logger.info(f"Generating batch embeddings using provider: '{provider}'")

    if provider == "openai":
        return _get_openai_embeddings_batch(texts)
    elif provider == "gemini":
        return _get_gemini_embeddings_batch(texts)
    elif provider == "sentence-transformers" and HAS_SENTENCE_TRANSFORMERS:
        return _get_sentence_transformer_embeddings_batch(texts)
    else:
        # Fallback
        if provider == "sentence-transformers":
            logger.warning("sentence-transformers requested but not installed. Falling back to Gemini.")
        else:
            logger.warning(f"Unknown or missing provider '{provider}'. Defaulting to Gemini.")
        return _get_gemini_embeddings_batch(texts)


def _get_sentence_transformer_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using SentenceTransformers."""
    global _embedding_model

    if not HAS_SENTENCE_TRANSFORMERS:
        raise ImportError("sentence_transformers is not installed")

    if _embedding_model is None:
        model_name = _resolve_sentence_transformer_model_name()
        logger.info(f"Loading embedding model: {model_name}")
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(model_name)

    embeddings = _embedding_model.encode(texts, convert_to_tensor=False)
    return [emb.tolist() for emb in embeddings]


def _get_openai_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.embeddings.create(
        model="text-embedding-3-small", input=texts
    )

    return [item.embedding for item in response.data]


def _get_gemini_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using Google Gemini."""
    from lexguard.llm.gemini_client import get_gemini_embeddings
    
    embeddings = get_gemini_embeddings(model_name=settings.embedding_model)
    return embeddings.embed_documents(texts)

