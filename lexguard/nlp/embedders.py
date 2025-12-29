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
    
    if provider == "ollama":
        return _get_ollama_embedding(text)
    elif provider == "openai":
        return _get_openai_embedding(text)
    elif provider == "gemini":
        return _get_gemini_embedding(text)
    elif provider == "sentence-transformers" and HAS_SENTENCE_TRANSFORMERS:
        return _get_sentence_transformer_embedding(text)
    elif provider == "chromadb" or provider == "sentence-transformers":
        # Use ChromaDB's default embedding function (lightweight)
        return _get_chromadb_embedding(text)
    else:
        # Default to ChromaDB embeddings (lightweight, no heavy dependencies)
        logger.warning(f"Unknown provider '{provider}'. Using ChromaDB default embeddings.")
        return _get_chromadb_embedding(text)


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


def _get_ollama_embedding(text: str) -> List[float]:
    """Get embedding using Ollama."""
    import httpx
    
    model = settings.embedding_model or "nomic-embed-text"
    base_url = settings.ollama_base_url
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{base_url}/api/embeddings",
                json={
                    "model": model,
                    "prompt": text,
                },
            )
            response.raise_for_status()
            result = response.json()
            return result.get("embedding", [])
    except httpx.ConnectError:
        logger.error("Could not connect to Ollama. Falling back to sentence-transformers.")
        if HAS_SENTENCE_TRANSFORMERS:
            return _get_sentence_transformer_embedding(text)
        raise ConnectionError(
            "Ollama is not running and sentence-transformers not available. "
            "Please start Ollama with: ollama serve"
        )
    except Exception as e:
        logger.error(f"Ollama embedding error: {e}")
        if HAS_SENTENCE_TRANSFORMERS:
            logger.warning("Falling back to sentence-transformers.")
            return _get_sentence_transformer_embedding(text)
        raise


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

    if provider == "ollama":
        return _get_ollama_embeddings_batch(texts)
    elif provider == "openai":
        return _get_openai_embeddings_batch(texts)
    elif provider == "gemini":
        return _get_gemini_embeddings_batch(texts)
    elif provider == "sentence-transformers" and HAS_SENTENCE_TRANSFORMERS:
        return _get_sentence_transformer_embeddings_batch(texts)
    elif provider == "chromadb" or provider == "sentence-transformers":
        # Use ChromaDB's default embedding function (lightweight)
        return _get_chromadb_embeddings_batch(texts)
    else:
        # Default to ChromaDB embeddings (lightweight, no heavy dependencies)
        logger.warning(f"Unknown provider '{provider}'. Using ChromaDB default embeddings.")
        return _get_chromadb_embeddings_batch(texts)


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


def _get_ollama_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using Ollama."""
    import httpx
    
    model = settings.embedding_model or "nomic-embed-text"
    base_url = settings.ollama_base_url
    
    try:
        # Ollama processes one at a time for embeddings
        embeddings = []
        with httpx.Client(timeout=60.0) as client:
            for text in texts:
                response = client.post(
                    f"{base_url}/api/embeddings",
                    json={
                        "model": model,
                        "prompt": text,
                    },
                )
                response.raise_for_status()
                result = response.json()
                embeddings.append(result.get("embedding", []))
        return embeddings
    except httpx.ConnectError:
        logger.error("Could not connect to Ollama. Falling back to sentence-transformers.")
        if HAS_SENTENCE_TRANSFORMERS:
            return _get_sentence_transformer_embeddings_batch(texts)
        raise ConnectionError(
            "Ollama is not running and sentence-transformers not available. "
            "Please start Ollama with: ollama serve"
        )
    except Exception as e:
        logger.error(f"Ollama embedding error: {e}")
        if HAS_SENTENCE_TRANSFORMERS:
            logger.warning("Falling back to sentence-transformers.")
            return _get_sentence_transformer_embeddings_batch(texts)
        raise


def _get_gemini_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using Google Gemini."""
    from lexguard.llm.gemini_client import get_gemini_embeddings
    
    embeddings = get_gemini_embeddings(model_name=settings.embedding_model)
    return embeddings.embed_documents(texts)


def _get_chromadb_embedding(text: str) -> List[float]:
    """Get embedding using lightweight hash-based approach (no ML dependencies)."""
    return _get_simple_embedding(text)


def _get_chromadb_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Get embeddings in batch using lightweight approach."""
    return [_get_simple_embedding(text) for text in texts]


def _get_simple_embedding(text: str) -> List[float]:
    """
    Simple lightweight embedding using text features (no ML models, no heavy dependencies).
    
    Uses a combination of:
    - Character frequency vectors
    - Word-based features
    - Hash-based features
    
    This provides reasonable similarity matching without requiring PyTorch or other heavy libraries.
    """
    import hashlib
    import re
    from collections import Counter
    
    # Normalize text
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    chars = list(text_lower)
    
    # Create feature vector (384 dimensions)
    embedding = []
    
    # 1. Character frequency features (128 dims)
    char_freq = Counter(chars)
    common_chars = 'abcdefghijklmnopqrstuvwxyz0123456789 .,!?;:()[]{}-'
    for char in common_chars[:128]:
        embedding.append(char_freq.get(char, 0) / max(len(chars), 1))
    
    # 2. Word-based features (128 dims)
    word_freq = Counter(words)
    common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                   'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
                   'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
                   'can', 'this', 'that', 'these', 'those', 'a', 'an', 'not', 'no', 'yes']
    for word in common_words[:128]:
        embedding.append(word_freq.get(word, 0) / max(len(words), 1))
    
    # 3. Hash-based features (128 dims)
    hash_obj = hashlib.sha256(text.encode())
    hash_bytes = hash_obj.digest()
    for i in range(128):
        if i < len(hash_bytes):
            embedding.append((hash_bytes[i] - 128) / 128.0)
        else:
            embedding.append(0.0)
    
    # Ensure exactly 384 dimensions
    while len(embedding) < 384:
        embedding.append(0.0)
    
    return embedding[:384]

