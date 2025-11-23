"""ChromaDB client management."""

import logging
from typing import Optional

import chromadb
from chromadb import Client

from lexguard.config import settings

logger = logging.getLogger(__name__)

# Global ChromaDB client
_chroma_client: Optional[Client] = None


def get_chroma_client() -> Client:
    """
    Get or create ChromaDB client.

    Returns:
        ChromaDB client instance
    """
    global _chroma_client

    if _chroma_client is None:
        logger.info(f"Initializing ChromaDB at {settings.chroma_db_path}")

        # Ensure directory exists
        settings.chroma_db_path.mkdir(parents=True, exist_ok=True)

        # Create persistent client
        _chroma_client = chromadb.PersistentClient(path=str(settings.chroma_db_path))

        logger.info("ChromaDB client initialized")

    return _chroma_client


def reset_chroma_client() -> None:
    """Reset the global ChromaDB client (useful for testing)."""
    global _chroma_client
    _chroma_client = None



