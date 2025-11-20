"""Document ingestion and extraction pipeline."""

from lexguard.ingest.cleaner import clean_contract_text, normalize_whitespace
from lexguard.ingest.ocr_extractor import extract_text_via_ocr
from lexguard.ingest.pdf_extractor import extract_text_from_pdf

__all__ = [
    "extract_text_from_pdf",
    "extract_text_via_ocr",
    "clean_contract_text",
    "normalize_whitespace",
]


