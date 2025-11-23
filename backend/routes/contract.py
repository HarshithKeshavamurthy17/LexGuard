"""Contract retrieval and analysis endpoints."""

import logging
from typing import List

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel

from lexguard.storage.schema import ContractMetadata
from lexguard.models import Clause
from lexguard.models.risk import ClauseRisk
from lexguard.reports import build_contract_summary, generate_pdf_report
from lexguard.reports.docx_report import generate_docx_report
from lexguard.risk import calculate_clause_risk, suggest_negotiation_points
from lexguard.nlp.clause_classifier import classify_clause
from lexguard.storage import load_contract
from lexguard.storage.file_store import list_contracts, save_contract

logger = logging.getLogger(__name__)

router = APIRouter()


class ContractResponse(BaseModel):
    """Response model for contract details."""

    id: str
    title: str
    uploaded_at: str
    original_filename: str
    clause_count: int
    summary: str


class RiskSummaryResponse(BaseModel):
    """Response model for risk summary."""

    contract_id: str
    total_clauses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    clause_risks: List[ClauseRisk]


class ClauseUpdateRequest(BaseModel):
    """Request model for updating a clause."""
    text: str


@router.get("/contracts", response_model=List[ContractMetadata])
async def get_contracts():
    """
    List all stored contracts.

    Returns:
        List of contract metadata
    """
    try:
        contracts = list_contracts()
        return contracts
    except Exception as e:
        logger.error(f"Error listing contracts: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving contracts")


@router.get("/contracts/{contract_id}", response_model=ContractResponse)
async def get_contract(contract_id: str):
    """
    Get contract details and summary.

    Args:
        contract_id: Contract ID

    Returns:
        Contract details with summary
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        # Generate summary
        summary = build_contract_summary(contract, use_llm=True)

        return ContractResponse(
            id=contract.id,
            title=contract.title,
            uploaded_at=contract.uploaded_at.isoformat(),
            original_filename=contract.original_filename,
            clause_count=len(contract.clauses),
            summary=summary,
        )

    except Exception as e:
        logger.error(f"Error retrieving contract {contract_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving contract details")


@router.get("/contracts/{contract_id}/clauses", response_model=List[Clause])
async def get_contract_clauses(contract_id: str):
    """
    Get all clauses for a contract.

    Args:
        contract_id: Contract ID

    Returns:
        List of clauses
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract.clauses


@router.get("/contracts/{contract_id}/risk", response_model=RiskSummaryResponse)
async def get_contract_risk(contract_id: str):
    """
    Get risk assessment for a contract.

    Args:
        contract_id: Contract ID

    Returns:
        Risk summary with clause-level risks
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        # Calculate risks for all clauses
        clause_risks = []
        risk_counts = {"high": 0, "medium": 0, "low": 0}

        for clause in contract.clauses:
            # Recalculate or use stored risk
            if clause.risk_score is None:
                risk = calculate_clause_risk(clause, use_llm=False)
            else:
                risk = ClauseRisk(
                    clause_id=clause.id,
                    score=clause.risk_score,
                    level=clause.risk_level,
                    reasons=[],
                    recommendations=[],
                )

            # Get suggestions for high/medium risk
            if risk.level in ("high", "medium"):
                risk.recommendations = suggest_negotiation_points(clause, use_llm=False)

            clause_risks.append(risk)

            if risk.level in risk_counts:
                risk_counts[risk.level] += 1

        return RiskSummaryResponse(
            contract_id=contract_id,
            total_clauses=len(contract.clauses),
            high_risk_count=risk_counts["high"],
            medium_risk_count=risk_counts["medium"],
            low_risk_count=risk_counts["low"],
            clause_risks=clause_risks,
        )

    except Exception as e:
        logger.error(f"Error calculating risk for {contract_id}: {e}")
        raise HTTPException(status_code=500, detail="Error calculating risk")


@router.get("/contracts/{contract_id}/report")
async def download_report(contract_id: str):
    """
    Generate and download PDF risk report.

    Args:
        contract_id: Contract ID

    Returns:
        PDF file
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        # Generate summary
        summary = build_contract_summary(contract, use_llm=True)

        # Get clause risks
        clause_risks = []
        for clause in contract.clauses:
            if clause.risk_score is None:
                risk = calculate_clause_risk(clause, use_llm=False)
            else:
                risk = ClauseRisk(
                    clause_id=clause.id,
                    score=clause.risk_score,
                    level=clause.risk_level,
                    reasons=[f"Risk level: {clause.risk_level}"],
                    recommendations=suggest_negotiation_points(clause, use_llm=False),
                )
            clause_risks.append(risk)

        # Generate PDF
        pdf_path = generate_pdf_report(contract, clause_risks, summary)

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=f"lexguard_report_{contract_id}.pdf",
        )

    except Exception as e:
        logger.error(f"Error generating report for {contract_id}: {e}")
        raise HTTPException(status_code=500, detail="Error generating report")


@router.get("/contracts/{contract_id}/report/docx")
async def download_docx_report(contract_id: str):
    """
    Generate and download Word risk report.

    Args:
        contract_id: Contract ID

    Returns:
        Word file
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        # Calculate risks if needed
        risk_counts = {"high": 0, "medium": 0, "low": 0}
        for clause in contract.clauses:
            if clause.risk_score is None:
                calculate_clause_risk(clause, use_llm=False)
            
            if clause.risk_level in risk_counts:
                risk_counts[clause.risk_level] += 1

        risk_data = {
            "high_risk_count": risk_counts["high"],
            "medium_risk_count": risk_counts["medium"],
            "low_risk_count": risk_counts["low"]
        }

        # Generate Word doc
        docx_content = generate_docx_report(contract, risk_data)

        return Response(
            content=docx_content,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=lexguard_report_{contract_id}.docx"}
        )

    except Exception as e:
        logger.error(f"Error generating Word report for {contract_id}: {e}")
        raise HTTPException(status_code=500, detail="Error generating report")


@router.post("/contracts/{contract_id}/clauses/{clause_id}/analyze", response_model=Clause)
async def analyze_clause(contract_id: str, clause_id: str, request: ClauseUpdateRequest):
    """
    Update and re-analyze a specific clause.

    Args:
        contract_id: Contract ID
        clause_id: Clause ID
        request: Update request with new text

    Returns:
        Updated clause
    """
    contract = load_contract(contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Find clause
    target_clause = None
    for clause in contract.clauses:
        if clause.id == clause_id:
            target_clause = clause
            break
    
    if not target_clause:
        raise HTTPException(status_code=404, detail="Clause not found")

    try:
        # Update text
        target_clause.text = request.text

        # Re-classify
        target_clause.clause_type = classify_clause(request.text)

        # Re-calculate risk
        calculate_clause_risk(target_clause, use_llm=True)

        # Save contract
        save_contract(contract)

        return target_clause

    except Exception as e:
        logger.error(f"Error analyzing clause {clause_id}: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing clause")
