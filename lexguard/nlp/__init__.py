"""NLP components for text processing and analysis."""

from lexguard.nlp.chunker import split_into_clauses
from lexguard.nlp.clause_classifier import classify_clause
from lexguard.nlp.embedders import get_embedding
from lexguard.nlp.vector_store import VectorStore

__all__ = ["split_into_clauses", "classify_clause", "get_embedding", "VectorStore"]


