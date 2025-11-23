"""Advanced analysis endpoints."""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from lexguard.analysis import (
    extract_key_terms,
    identify_parties,
    extract_important_dates,
    extract_obligations,
)
from lexguard.storage import load_contract

logger = logging.getLogger(__name__)

router = APIRouter()


class ComprehensiveAnalysis(BaseModel):
    """Comprehensive contract analysis response."""

    key_terms: dict
    parties: list[dict]
    important_dates: list[dict]
    obligations: dict


@router.get("/contracts/{contract_id}/analysis", response_model=ComprehensiveAnalysis)
async def get_comprehensive_analysis(contract_id: str):
    """
    Get comprehensive analysis of a contract.

    Includes:
    - Key terms and definitions
    - Identified parties
    - Important dates
    - Obligations and requirements

    Args:
        contract_id: Contract ID

    Returns:
        Comprehensive analysis data
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        logger.info(f"Running comprehensive analysis for contract {contract_id}")

        # Run all analysis modules
        key_terms = extract_key_terms(contract.text)
        parties = identify_parties(contract.text)
        important_dates = extract_important_dates(contract.text)
        obligations = extract_obligations(contract.text)

        return ComprehensiveAnalysis(
            key_terms=key_terms,
            parties=parties,
            important_dates=important_dates,
            obligations=obligations,
        )

    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error performing analysis")



