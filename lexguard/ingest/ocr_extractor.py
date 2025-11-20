"""OCR-based text extraction using pytesseract."""

import logging
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

logger = logging.getLogger(__name__)


def extract_text_via_ocr(file_path: Path) -> str:
    """
    Extract text from a PDF using OCR (for scanned documents).

    This uses pytesseract to perform OCR on each page of the PDF.
    Note: Requires tesseract to be installed on the system.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text as a string

    Raises:
        ImportError: If pytesseract is not properly installed
    """
    try:
        import pytesseract
        from pdf2image import convert_from_path
    except ImportError:
        logger.error(
            "OCR dependencies not available. Install with: "
            "pip install pytesseract pdf2image"
        )
        raise

    try:
        # Convert PDF pages to images
        logger.info(f"Converting PDF to images for OCR: {file_path}")
        images = convert_from_path(file_path)

        text_parts = []
        for i, image in enumerate(images, 1):
            logger.info(f"Performing OCR on page {i}/{len(images)}")
            page_text = pytesseract.image_to_string(image)
            text_parts.append(page_text)

        full_text = "\n".join(text_parts)
        logger.info(f"OCR extracted {len(full_text)} characters")
        return full_text

    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        raise


def extract_text_from_image(image_path: Path) -> str:
    """
    Extract text from a single image file.

    Args:
        image_path: Path to the image file

    Returns:
        Extracted text
    """
    try:
        import pytesseract
    except ImportError:
        logger.error("pytesseract not available")
        raise

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


