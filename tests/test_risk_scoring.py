"""Tests for risk scoring functionality."""

import pytest

from lexguard.models import Clause, ClauseType
from lexguard.risk.scoring import calculate_clause_risk, score_to_level


def test_liability_clause_high_risk():
    """Test that liability clauses with unlimited liability are high risk."""
    clause = Clause(
        id="test_1",
        contract_id="test_contract",
        index=0,
        text="The contractor shall have unlimited liability and shall indemnify the company for all damages.",
        clause_type=ClauseType.LIABILITY,
    )

    risk = calculate_clause_risk(clause, use_llm=False)

    assert risk.score > 0.5
    assert risk.level in ("medium", "high")
    assert len(risk.reasons) > 0


def test_termination_clause_short_notice():
    """Test that termination with short notice is flagged as risky."""
    clause = Clause(
        id="test_2",
        contract_id="test_contract",
        index=1,
        text="This agreement may be terminated immediately without cause by either party.",
        clause_type=ClauseType.TERMINATION,
    )

    risk = calculate_clause_risk(clause, use_llm=False)

    assert risk.score > 0.3
    assert len(risk.reasons) > 0
    assert any("immediate" in r.lower() for r in risk.reasons)


def test_non_compete_long_duration():
    """Test that long non-compete periods are high risk."""
    clause = Clause(
        id="test_3",
        contract_id="test_contract",
        index=2,
        text="Employee agrees not to compete for a period of 3 years globally.",
        clause_type=ClauseType.NON_COMPETE,
    )

    risk = calculate_clause_risk(clause, use_llm=False)

    assert risk.score > 0.5
    assert risk.level in ("medium", "high")


def test_low_risk_clause():
    """Test that benign clauses have low risk."""
    clause = Clause(
        id="test_4",
        contract_id="test_contract",
        index=3,
        text="This agreement is governed by the laws of the State of California.",
        clause_type=ClauseType.MISC,
    )

    risk = calculate_clause_risk(clause, use_llm=False)

    assert risk.score < 0.5
    assert risk.level in ("low", "medium")


def test_score_to_level():
    """Test risk score to level conversion."""
    assert score_to_level(0.1) == "low"
    assert score_to_level(0.3) == "low"
    assert score_to_level(0.5) == "medium"
    assert score_to_level(0.7) == "high"
    assert score_to_level(0.9) == "high"


def test_payment_clause_unpaid():
    """Test that unpaid positions are flagged."""
    clause = Clause(
        id="test_5",
        contract_id="test_contract",
        index=4,
        text="This is a volunteer position with no compensation or salary.",
        clause_type=ClauseType.PAYMENT,
    )

    risk = calculate_clause_risk(clause, use_llm=False)

    assert risk.score > 0.3
    assert any("no pay" in r.lower() or "unpaid" in r.lower() for r in risk.reasons)



