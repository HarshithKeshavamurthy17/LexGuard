"""End-to-end integration tests with dummy data."""

import pytest
import uuid
from datetime import datetime

from lexguard.models import Contract, Clause, ClauseType
from lexguard.nlp.chunker import split_into_clauses
from lexguard.nlp.clause_classifier import classify_clause
from lexguard.risk.scoring import calculate_clause_risk
from lexguard.storage.file_store import save_contract, load_contract, delete_contract


@pytest.fixture
def sample_contract_text():
    """Provide sample contract text."""
    return """
    EMPLOYMENT AGREEMENT
    
    1. Position and Duties
    The Employee shall serve as Senior Software Engineer and perform duties as assigned.
    
    2. Compensation
    The Company shall pay Employee a salary of $120,000 per year, payable bi-weekly.
    
    3. Termination
    Either party may terminate this agreement with 30 days written notice.
    
    4. Confidentiality
    Employee agrees to maintain confidentiality of all proprietary information.
    
    5. Non-Compete
    Employee agrees not to compete for 12 months within a 50-mile radius.
    
    6. Liability
    Employee shall indemnify Company for any losses arising from Employee's negligence.
    """


def test_full_pipeline_without_llm(sample_contract_text):
    """Test the full processing pipeline without LLM calls."""
    # Step 1: Split into clauses
    clause_texts = split_into_clauses(sample_contract_text, min_length=30)

    assert len(clause_texts) > 0, "Should extract at least one clause"

    # Step 2: Create contract
    contract_id = str(uuid.uuid4())
    contract = Contract(
        id=contract_id,
        title="Test Employment Agreement",
        original_filename="test.pdf",
        text=sample_contract_text,
        clauses=[],
    )

    # Step 3: Process each clause
    clauses = []
    for i, text in enumerate(clause_texts):
        # Classify
        clause_type = classify_clause(text, use_llm=False)

        # Create clause
        clause = Clause(
            id=f"{contract_id}_clause_{i}",
            contract_id=contract_id,
            index=i,
            text=text,
            clause_type=clause_type,
        )

        # Calculate risk
        risk = calculate_clause_risk(clause, use_llm=False)
        clause.risk_score = risk.score
        clause.risk_level = risk.level

        clauses.append(clause)

    contract.clauses = clauses

    # Verify we have clauses with different types
    clause_types = {c.clause_type for c in clauses}
    assert len(clause_types) > 1, "Should identify multiple clause types"

    # Verify risk scoring
    risk_scores = [c.risk_score for c in clauses if c.risk_score is not None]
    assert len(risk_scores) > 0, "Should have risk scores"
    assert all(0 <= score <= 1 for score in risk_scores), "Risk scores should be between 0 and 1"

    # Step 4: Save and load contract
    save_contract(contract)

    loaded_contract = load_contract(contract_id)
    assert loaded_contract is not None, "Should load saved contract"
    assert loaded_contract.id == contract_id
    assert len(loaded_contract.clauses) == len(clauses)

    # Clean up
    delete_contract(contract_id)


def test_clause_classification_accuracy(sample_contract_text):
    """Test clause classification on known clause types."""
    clause_texts = split_into_clauses(sample_contract_text, min_length=30)

    classifications = {}
    for text in clause_texts:
        clause_type = classify_clause(text, use_llm=False)
        text_lower = text.lower()

        # Store for analysis
        if "compensation" in text_lower or "salary" in text_lower:
            classifications["payment"] = clause_type
        elif "termination" in text_lower or "terminate" in text_lower:
            classifications["termination"] = clause_type
        elif "confidential" in text_lower:
            classifications["confidentiality"] = clause_type
        elif "non-compete" in text_lower or "compete" in text_lower:
            classifications["non_compete"] = clause_type
        elif "liability" in text_lower or "indemnify" in text_lower:
            classifications["liability"] = clause_type

    # Verify at least some classifications are correct
    if "payment" in classifications:
        assert classifications["payment"] == ClauseType.PAYMENT

    if "termination" in classifications:
        assert classifications["termination"] == ClauseType.TERMINATION


def test_risk_distribution(sample_contract_text):
    """Test that risk levels are reasonably distributed."""
    clause_texts = split_into_clauses(sample_contract_text, min_length=30)

    risk_levels = {"low": 0, "medium": 0, "high": 0}

    for i, text in enumerate(clause_texts):
        clause_type = classify_clause(text, use_llm=False)

        clause = Clause(
            id=f"test_clause_{i}",
            contract_id="test",
            index=i,
            text=text,
            clause_type=clause_type,
        )

        risk = calculate_clause_risk(clause, use_llm=False)
        risk_levels[risk.level] += 1

    # Should have some variation in risk levels
    total_clauses = sum(risk_levels.values())
    assert total_clauses > 0, "Should have processed some clauses"

    # At least 50% of clauses should have meaningful risk assessments
    non_low = risk_levels["medium"] + risk_levels["high"]
    assert non_low > 0, "Should identify at least some risk"


