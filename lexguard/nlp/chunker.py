"""Text chunking utilities for splitting contracts into clauses."""

import re
import logging
from typing import List

logger = logging.getLogger(__name__)


def split_into_clauses(text: str, min_length: int = 50) -> List[str]:
    """
    Split contract text into individual clauses.

    Uses multiple heuristics:
    - Numbered sections (1., 2., a., b., etc.)
    - Section headers (uppercase lines)
    - Double line breaks (paragraph boundaries)
    - Semicolons in legal lists

    Args:
        text: Contract text to split
        min_length: Minimum character length for a valid clause

    Returns:
        List of clause texts
    """
    logger.info("Splitting text into clauses")

    # First, split by numbered sections
    clauses = _split_by_numbered_sections(text)

    # If we didn't find numbered sections, use paragraph-based splitting
    if len(clauses) <= 1:
        clauses = _split_by_paragraphs(text)

    # Clean and filter clauses
    cleaned_clauses = []
    for clause in clauses:
        clause = clause.strip()

        # Skip very short clauses
        if len(clause) < min_length:
            continue

        # Skip lines that are just section headers
        if _is_likely_header(clause):
            continue

        cleaned_clauses.append(clause)

    logger.info(f"Split text into {len(cleaned_clauses)} clauses")
    return cleaned_clauses


def _split_by_numbered_sections(text: str) -> List[str]:
    """Split text by numbered sections (1., 2., a), b), etc.)."""
    # Pattern for numbered sections: "1.", "2.1", "a)", "(i)", etc.
    pattern = re.compile(
        r"(?:^|\n)(?:\d+\.(?:\d+\.?)?|[a-z]\)|[ivx]+\)|\([ivx]+\)|\([a-z]\))\s+",
        re.IGNORECASE | re.MULTILINE,
    )

    splits = pattern.split(text)
    positions = [m.start() for m in pattern.finditer(text)]

    if not positions:
        return [text]

    clauses = []
    for i, match in enumerate(pattern.finditer(text)):
        start = match.start()
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        clause = text[start:end]
        clauses.append(clause)

    return clauses if clauses else [text]


def _split_by_paragraphs(text: str) -> List[str]:
    """Split text by paragraph breaks."""
    # Split by double newlines or more
    paragraphs = re.split(r"\n{2,}", text)
    return [p.strip() for p in paragraphs if p.strip()]


def _is_likely_header(text: str) -> bool:
    """
    Check if text is likely a section header rather than content.

    Headers typically are:
    - Very short (< 100 chars)
    - All uppercase
    - End without punctuation
    """
    text = text.strip()

    # Very short and all uppercase
    if len(text) < 100 and text.isupper():
        return True

    # Single line, short, no period at end
    if len(text) < 80 and "\n" not in text and not text.endswith("."):
        return True

    return False


def merge_short_clauses(clauses: List[str], min_length: int = 100) -> List[str]:
    """
    Merge consecutive short clauses together.

    This helps when chunking is too aggressive.

    Args:
        clauses: List of clause texts
        min_length: Minimum desired length

    Returns:
        Merged clause list
    """
    if not clauses:
        return []

    merged = []
    current = clauses[0]

    for clause in clauses[1:]:
        if len(current) < min_length:
            current = current + " " + clause
        else:
            merged.append(current)
            current = clause

    # Don't forget the last clause
    merged.append(current)

    return merged



