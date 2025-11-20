"""Upload and processing endpoints."""

import logging
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from lexguard.config import settings
from lexguard.ingest import clean_contract_text, extract_text_from_pdf
from lexguard.ingest.pdf_extractor import should_use_ocr
from lexguard.models import Clause, Contract
from lexguard.nlp import VectorStore, classify_clause, split_into_clauses
from lexguard.risk import calculate_clause_risk, suggest_negotiation_points
from lexguard.storage import save_contract

logger = logging.getLogger(__name__)

router = APIRouter()


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""

    contract_id: str
    title: str
    clause_count: int
    message: str


@router.post("/upload", response_model=UploadResponse)
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload and process a contract PDF.

    Steps:
    1. Save uploaded file
    2. Extract text
    3. Clean text
    4. Split into clauses
    5. Classify each clause
    6. Calculate risk scores
    7. Generate embeddings
    8. Store in vector database
    9. Save contract to file storage

    Args:
        file: Uploaded PDF file

    Returns:
        Contract ID and metadata
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    logger.info(f"Processing uploaded file: {file.filename}")

    try:
        # Generate contract ID
        contract_id = str(uuid.uuid4())

        # Save uploaded file
        uploads_dir = settings.data_dir / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)
        upload_path = uploads_dir / f"{contract_id}.pdf"

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Saved file to {upload_path}")

        # Extract text
        logger.info("Extracting text from PDF...")
        text = extract_text_from_pdf(upload_path)

        # Check if OCR is needed
        if should_use_ocr(text):
            logger.warning("PDF may be scanned, consider using OCR")
            # For now, we'll continue with what we have

        # Clean text
        logger.info("Cleaning extracted text...")
        text = clean_contract_text(text)

        if len(text) < 100:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from PDF. File may be corrupted or scanned.",
            )

        # Split into clauses
        logger.info("Splitting into clauses...")
        clause_texts = split_into_clauses(text)

        if not clause_texts:
            raise HTTPException(
                status_code=400, detail="Could not identify clauses in the document"
            )

        logger.info(f"Found {len(clause_texts)} clauses")

        # Create contract object
        title = file.filename.replace(".pdf", "")
        contract = Contract(
            id=contract_id,
            title=title,
            original_filename=file.filename,
            text=text,
            clauses=[],
        )

        # Process each clause
        clauses = []
        for i, clause_text in enumerate(clause_texts):
            # Classify clause
            clause_type = classify_clause(clause_text, use_llm=False)

            # Create clause object
            clause = Clause(
                id=f"{contract_id}_clause_{i}",
                contract_id=contract_id,
                index=i,
                text=clause_text,
                clause_type=clause_type,
            )

            # Calculate risk
            risk = calculate_clause_risk(clause, use_llm=False)
            clause.risk_score = risk.score
            clause.risk_level = risk.level

            # Get negotiation suggestions (only for high/medium risk)
            if risk.level in ("high", "medium"):
                suggestions = suggest_negotiation_points(clause, use_llm=False)
                risk.recommendations = suggestions

            clauses.append(clause)

        contract.clauses = clauses

        # Store embeddings in vector database
        logger.info("Generating embeddings and storing in vector database...")
        vector_store = VectorStore()
        vector_store.upsert_clauses(contract_id, clauses)

        # Save contract to file storage
        logger.info("Saving contract to storage...")
        save_contract(contract)

        logger.info(f"Successfully processed contract {contract_id}")

        return UploadResponse(
            contract_id=contract_id,
            title=title,
            clause_count=len(clauses),
            message="Contract processed successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


