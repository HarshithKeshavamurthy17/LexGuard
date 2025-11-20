"""Text cleaning and normalization utilities."""

import re
import logging

logger = logging.getLogger(__name__)


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    - Replaces multiple spaces with single space
    - Normalizes line breaks
    - Trims leading/trailing whitespace

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)

    # Replace multiple newlines with double newline (paragraph break)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces at line starts/ends
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    return text.strip()


def remove_headers_footers(text: str) -> str:
    """
    Attempt to remove common headers and footers using heuristics.

    This is a simple implementation that removes:
    - Page numbers
    - Common header/footer patterns
    - Repeated boilerplate text

    Args:
        text: Input text

    Returns:
        Text with headers/footers removed
    """
    lines = text.split("\n")
    cleaned_lines = []

    # Pattern for page numbers (e.g., "Page 1", "1 of 10", etc.)
    page_num_pattern = re.compile(
        r"^\s*(?:Page\s+)?\d+(?:\s+of\s+\d+)?\s*$", re.IGNORECASE
    )

    # Pattern for dates in headers/footers
    date_pattern = re.compile(r"^\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\s*$")

    for line in lines:
        # Skip page numbers
        if page_num_pattern.match(line):
            continue

        # Skip standalone dates
        if date_pattern.match(line):
            continue

        # Skip very short lines that are likely headers/footers
        if len(line.strip()) < 5 and line.strip().isdigit():
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_excessive_punctuation(text: str) -> str:
    """
    Clean up excessive punctuation that may result from OCR errors.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    # Replace multiple periods with ellipsis
    text = re.sub(r"\.{4,}", "...", text)

    # Remove excessive dashes
    text = re.sub(r"-{3,}", "--", text)

    # Clean up excessive underscores
    text = re.sub(r"_{3,}", "__", text)

    return text


def clean_contract_text(text: str) -> str:
    """
    Apply full cleaning pipeline to contract text.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text ready for processing
    """
    logger.info("Cleaning contract text")

    # Apply cleaning steps
    text = normalize_whitespace(text)
    text = remove_headers_footers(text)
    text = remove_excessive_punctuation(text)

    # Final normalization
    text = normalize_whitespace(text)

    logger.info(f"Cleaned text: {len(text)} characters")
    return text


