"""Tests for text chunking functionality."""

import pytest

from lexguard.nlp.chunker import split_into_clauses, merge_short_clauses


def test_split_into_clauses_with_numbered_sections():
    """Test splitting text with numbered sections."""
    text = """
    1. Payment Terms
    The contractor shall be paid $5,000 per month.
    
    2. Termination
    Either party may terminate with 30 days notice.
    
    3. Confidentiality
    All information shall remain confidential.
    """

    clauses = split_into_clauses(text, min_length=20)

    assert len(clauses) > 0
    assert any("payment" in c.lower() for c in clauses)
    assert any("termination" in c.lower() for c in clauses)


def test_split_into_clauses_with_paragraphs():
    """Test splitting text by paragraphs."""
    text = """
    This agreement is between Party A and Party B.
    
    The payment terms are as follows: $1000 per month for services rendered.
    
    Confidentiality obligations shall survive termination of this agreement.
    """

    clauses = split_into_clauses(text, min_length=20)

    assert len(clauses) > 0
    for clause in clauses:
        assert len(clause) >= 20


def test_split_empty_text():
    """Test handling of empty text."""
    clauses = split_into_clauses("", min_length=20)
    assert clauses == []


def test_split_short_text():
    """Test handling of very short text."""
    text = "Short."
    clauses = split_into_clauses(text, min_length=10)
    assert len(clauses) == 0  # Too short


def test_merge_short_clauses():
    """Test merging of short clauses."""
    short_clauses = [
        "First short clause.",
        "Second short.",
        "This is a much longer clause that exceeds the minimum length requirement.",
        "Another short.",
    ]

    merged = merge_short_clauses(short_clauses, min_length=50)

    assert len(merged) <= len(short_clauses)
    # At least one clause should be longer after merging
    assert any(len(c) >= 50 for c in merged)



