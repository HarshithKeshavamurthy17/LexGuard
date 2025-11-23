"""Text embedding utilities."""

import logging
from typing import List

from lexguard.config import settings

logger = logging.getLogger(__name__)

# Cache for embedding model
_embedding_model = None


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for text.

    Uses the configured embedding provider.

    Args:
        text: Text to embed

    Returns:
        Embedding vector as list of floats
    """
    if settings.embedding_provider == "openai":
        return _get_openai_embedding(text)
    elif settings.embedding_provider == "gemini":
        return _get_gemini_embedding(text)
    else:
        return _get_sentence_transformer_embedding(text)


def _get_sentence_transformer_embedding(text: str) -> List[float]:
    """Get embedding using SentenceTransformers."""
    global _embedding_model

    if _embedding_model is None:
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(settings.embedding_model)

    embedding = _embedding_model.encode(text, convert_to_tensor=False)
    return embedding.tolist()


def _get_openai_embedding(text: str) -> List[float]:
    """Get embedding using OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.embeddings.create(
        model="text-embedding-3-small",  # or use settings.embedding_model
        input=text,
    )

    return response.data[0].embedding


def _get_gemini_embedding(text: str) -> List[float]:
    """Get embedding using Google Gemini."""
    from lexguard.llm.gemini_client import get_gemini_embeddings
    
    # Use the configured model name or default
    embeddings = get_gemini_embeddings(model_name=settings.embedding_model)
    return embeddings.embed_query(text)


def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    if settings.embedding_provider == "openai":
        return _get_openai_embeddings_batch(texts)
    elif settings.embedding_provider == "gemini":
        return _get_gemini_embeddings_batch(texts)
    else:
        return _get_sentence_transformer_embeddings_batch(texts)


def _get_sentence_transformer_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using SentenceTransformers."""
    global _embedding_model

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(settings.embedding_model)

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
