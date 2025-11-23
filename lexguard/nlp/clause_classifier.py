"""Clause classification using rule-based and LLM approaches."""

import re
import logging
from typing import Optional

from lexguard.models.clause import ClauseType

logger = logging.getLogger(__name__)


# Keyword patterns for each clause type
CLAUSE_PATTERNS = {
    ClauseType.TERMINATION: [
        r"\btermination\b",
        r"\bterminate\b",
        r"\bexpir(?:e|ation)\b",
        r"\bend(?:ing)?\s+(?:of|this)\s+agreement\b",
        r"\bnotice\s+(?:of|to)\s+terminate\b",
        r"\bcancellation\b",
    ],
    ClauseType.LIABILITY: [
        r"\bliability\b",
        r"\bliable\b",
        r"\bindemnif(?:y|ication)\b",
        r"\bhold\s+harmless\b",
        r"\bdamages\b",
        r"\blosses\b",
        r"\blimitation\s+of\s+liability\b",
        r"\bexculpation\b",
    ],
    ClauseType.PAYMENT: [
        r"\bpayment\b",
        r"\bpay\b",
        r"\bcompensation\b",
        r"\bfee(?:s)?\b",
        r"\bsalary\b",
        r"\bwage(?:s)?\b",
        r"\bremuneration\b",
        r"\binvoice\b",
        r"\b\$\d+",
        r"\bamount\s+(?:of|due)\b",
    ],
    ClauseType.CONFIDENTIALITY: [
        r"\bconfidential(?:ity)?\b",
        r"\bnon-disclosure\b",
        r"\bproprietary\s+information\b",
        r"\btrade\s+secret(?:s)?\b",
        r"\bdisclosure\b",
        r"\bsecrecy\b",
    ],
    ClauseType.IP: [
        r"\bintellectual\s+property\b",
        r"\bcopyright(?:s)?\b",
        r"\bpatent(?:s)?\b",
        r"\btrademark(?:s)?\b",
        r"\bownership\s+of\s+work\b",
        r"\binvention(?:s)?\b",
        r"\bwork\s+product\b",
    ],
    ClauseType.NON_COMPETE: [
        r"\bnon-compete\b",
        r"\bnon\s+compete\b",
        r"\bcompete\b",
        r"\brestrictive\s+covenant\b",
        r"\bnon-solicitation\b",
        r"\bsolicitation\b",
    ],
}


def classify_clause(text: str, use_llm: bool = False) -> ClauseType:
    """
    Classify a clause into a specific type.

    Uses a two-stage approach:
    1. Rule-based classification using keyword patterns
    2. (Optional) LLM refinement for ambiguous cases

    Args:
        text: Clause text to classify
        use_llm: Whether to use LLM for refinement

    Returns:
        ClauseType enum value
    """
    # Stage 1: Rule-based classification
    clause_type = _classify_with_rules(text)

    # Stage 2: LLM refinement (if requested and clause is ambiguous)
    if use_llm and clause_type in (ClauseType.UNSURE, ClauseType.MISC):
        try:
            clause_type = _classify_with_llm(text)
        except Exception as e:
            logger.warning(f"LLM classification failed, using rule-based result: {e}")

    return clause_type


def _classify_with_rules(text: str) -> ClauseType:
    """
    Classify clause using keyword pattern matching.

    Args:
        text: Clause text

    Returns:
        Most likely ClauseType based on keyword matches
    """
    text_lower = text.lower()
    scores = {clause_type: 0 for clause_type in ClauseType}

    for clause_type, patterns in CLAUSE_PATTERNS.items():
        for pattern in patterns:
            matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
            scores[clause_type] += matches

    # Find the type with the highest score
    max_score = max(scores.values())

    if max_score == 0:
        return ClauseType.MISC

    # Get the clause type with the highest score
    best_type = max(scores.items(), key=lambda x: x[1])[0]

    return best_type


def _classify_with_llm(text: str) -> ClauseType:
    """
    Use LLM to classify clause (optional refinement).

    Args:
        text: Clause text

    Returns:
        ClauseType from LLM analysis
    """
    # Import here to avoid circular dependencies
    from lexguard.llm import get_llm_client
    from lexguard.llm.prompts import CLAUSE_CLASSIFICATION_PROMPT

    try:
        llm = get_llm_client()
        prompt = CLAUSE_CLASSIFICATION_PROMPT.format(clause_text=text)

        response = llm.chat(
            [
                {"role": "system", "content": "You are a legal document analyzer."},
                {"role": "user", "content": prompt},
            ]
        )

        # Parse response to extract clause type
        response_lower = response.lower()

        for clause_type in ClauseType:
            if clause_type.value in response_lower:
                return clause_type

        return ClauseType.MISC

    except Exception as e:
        logger.error(f"LLM classification error: {e}")
        raise


def get_classification_confidence(text: str, clause_type: ClauseType) -> float:
    """
    Get confidence score for a classification.

    Args:
        text: Clause text
        clause_type: Assigned clause type

    Returns:
        Confidence score between 0 and 1
    """
    if clause_type not in CLAUSE_PATTERNS:
        return 0.5  # Default confidence for MISC/UNSURE

    text_lower = text.lower()
    patterns = CLAUSE_PATTERNS[clause_type]

    match_count = 0
    for pattern in patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            match_count += 1

    # Normalize confidence
    confidence = min(match_count / 3, 1.0)  # Cap at 1.0
    return confidence



