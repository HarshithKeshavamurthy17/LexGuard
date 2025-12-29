"""Negotiation suggestions for contract clauses."""

import logging
from typing import List

from lexguard.models.clause import Clause, ClauseType

logger = logging.getLogger(__name__)


def suggest_negotiation_points(clause: Clause, use_llm: bool = False) -> List[str]:
    """
    Generate negotiation suggestions for a clause.

    Args:
        clause: Clause to analyze
        use_llm: Whether to use LLM for suggestions

    Returns:
        List of negotiation suggestions
    """
    # Get rule-based suggestions
    suggestions = _get_rule_based_suggestions(clause)

    # Enhance with LLM if requested
    if use_llm and clause.risk_level in ("medium", "high"):
        try:
            llm_suggestions = _get_llm_suggestions(clause)
            suggestions.extend(llm_suggestions)
        except Exception as e:
            logger.warning(f"LLM suggestion generation failed: {e}")

    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        if s.lower() not in seen:
            seen.add(s.lower())
            unique_suggestions.append(s)

    return unique_suggestions[:5]  # Limit to top 5


def _get_rule_based_suggestions(clause: Clause) -> List[str]:
    """
    Generate rule-based negotiation suggestions.

    Args:
        clause: Clause to analyze

    Returns:
        List of suggestions
    """
    suggestions = []

    if clause.clause_type == ClauseType.LIABILITY:
        suggestions.extend(
            [
                "Request a cap on total liability (e.g., contract value or specific amount)",
                "Exclude indirect, consequential, or punitive damages",
                "Add mutual indemnification provisions",
                "Clarify what events trigger indemnification",
                "Request right to defend claims with own counsel",
            ]
        )

    elif clause.clause_type == ClauseType.TERMINATION:
        suggestions.extend(
            [
                "Negotiate longer notice period (30-90 days)",
                "Request termination only 'for cause' with defined reasons",
                "Add severance or termination payment provisions",
                "Include dispute resolution before termination",
                "Clarify obligations upon termination",
            ]
        )

    elif clause.clause_type == ClauseType.NON_COMPETE:
        suggestions.extend(
            [
                "Reduce duration to 6-12 months maximum",
                "Narrow geographic scope to specific regions",
                "Define 'competing business' more narrowly",
                "Add exceptions for existing commitments",
                "Include compensation for non-compete period",
            ]
        )

    elif clause.clause_type == ClauseType.IP:
        suggestions.extend(
            [
                "Exclude pre-existing intellectual property",
                "Limit assignment to work created during employment",
                "Add carve-out for personal projects",
                "Clarify ownership of derivative works",
                "Request license-back for your contributions",
            ]
        )

    elif clause.clause_type == ClauseType.CONFIDENTIALITY:
        suggestions.extend(
            [
                "Define 'confidential information' more clearly",
                "Add exceptions for public information",
                "Limit duration of confidentiality obligations",
                "Exclude information already known",
                "Allow disclosure when legally required",
            ]
        )

    elif clause.clause_type == ClauseType.PAYMENT:
        suggestions.extend(
            [
                "Specify exact payment amounts and schedule",
                "Add late payment penalties or interest",
                "Include expense reimbursement terms",
                "Clarify payment method and currency",
                "Add cost-of-living or performance adjustments",
            ]
        )

    else:
        suggestions.extend(
            [
                "Request clearer definitions of key terms",
                "Add specific performance metrics or criteria",
                "Include dispute resolution procedures",
            ]
        )

    return suggestions


def _get_llm_suggestions(clause: Clause) -> List[str]:
    """
    Use LLM to generate contextual negotiation suggestions.

    Args:
        clause: Clause to analyze

    Returns:
        List of LLM-generated suggestions
    """
    from lexguard.llm import get_llm_client
    from lexguard.llm.prompts import NEGOTIATION_SUGGESTIONS_PROMPT

    llm = get_llm_client()

    clause_type_str = clause.clause_type if isinstance(clause.clause_type, str) else clause.clause_type.value
    prompt = NEGOTIATION_SUGGESTIONS_PROMPT.format(
        clause_type=clause_type_str,
        risk_level=clause.risk_level or "unknown",
        clause_text=clause.text,
    )

    messages = [
        {"role": "system", "content": "You are a contract negotiation expert."},
        {"role": "user", "content": prompt},
    ]

    try:
        result = llm.chat_structured(messages, schema={})

        # Try to extract array from response
        if isinstance(result, dict) and "suggestions" in result:
            return result["suggestions"]
        elif isinstance(result, list):
            return result
        else:
            # Fallback: parse as list
            return []

    except Exception as e:
        logger.error(f"Error parsing LLM suggestions: {e}")
        return []

