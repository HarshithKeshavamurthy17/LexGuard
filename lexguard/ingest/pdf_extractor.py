"""PDF text extraction using pypdf."""

import logging
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text as a string

    Raises:
        Exception: If PDF cannot be read
    """
    try:
        reader = PdfReader(file_path)
        text_parts = []

        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
            else:
                logger.warning(f"Page {page_num} has no extractable text")

        full_text = "\n".join(text_parts)

        # Check if extraction was successful
        if len(full_text.strip()) < 100:
            logger.warning("Extracted text is suspiciously short, may need OCR")
            return full_text

        logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
        return full_text

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise


def should_use_ocr(text: str, min_length: int = 100) -> bool:
    """
    Determine if OCR should be used based on extracted text quality.

    Args:
        text: Extracted text
        min_length: Minimum expected text length

    Returns:
        True if OCR should be attempted
    """
    if not text or len(text.strip()) < min_length:
        return True

    # Check for gibberish or non-standard characters
    printable_ratio = sum(c.isprintable() or c.isspace() for c in text) / len(text)
    if printable_ratio < 0.8:
        return True

    return False



