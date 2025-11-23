"""Contract summary generation."""

import logging
from typing import Optional

from lexguard.models.contract import Contract

logger = logging.getLogger(__name__)


def build_contract_summary(contract: Contract, use_llm: bool = True) -> str:
    """
    Build a plain-English summary of a contract.

    Args:
        contract: Contract to summarize
        use_llm: Whether to use LLM for summary

    Returns:
        Summary text
    """
    if use_llm:
        try:
            return _build_llm_summary(contract)
        except Exception as e:
            logger.warning(f"LLM summary failed, falling back to rule-based: {e}")

    return _build_rule_based_summary(contract)


def _build_llm_summary(contract: Contract) -> str:
    """
    Generate summary using LLM.

    Args:
        contract: Contract to summarize

    Returns:
        Generated summary
    """
    from lexguard.llm import get_llm_client
    from lexguard.llm.prompts import CONTRACT_SUMMARY_PROMPT

    llm = get_llm_client()

    # Truncate text if too long (keep first 8000 chars)
    text = contract.text[:8000]
    if len(contract.text) > 8000:
        text += "\n\n[Document truncated for analysis...]"

    prompt = CONTRACT_SUMMARY_PROMPT.format(contract_text=text)

    messages = [
        {
            "role": "system",
            "content": "You are a legal expert who explains contracts in plain English.",
        },
        {"role": "user", "content": prompt},
    ]

    summary = llm.chat(messages, temperature=0.5, max_tokens=800)
    return summary


def _build_rule_based_summary(contract: Contract) -> str:
    """
    Generate a basic summary using rules.

    Args:
        contract: Contract to summarize

    Returns:
        Summary text
    """
    clauses = contract.clauses

    # Count clause types and risks
    clause_type_counts = {}
    risk_counts = {"high": 0, "medium": 0, "low": 0}

    for clause in clauses:
        # Count clause types
        clause_type = _get_clause_type_value(clause)
        clause_type_counts[clause_type] = clause_type_counts.get(clause_type, 0) + 1

        # Count risk levels
        if clause.risk_level:
            risk_counts[clause.risk_level] += 1

    # Build summary
    summary_parts = [
        f"Contract Summary: {contract.title}",
        f"\nDocument: {contract.original_filename}",
        f"Uploaded: {contract.uploaded_at.strftime('%Y-%m-%d %H:%M')}",
        f"\nThis contract contains {len(clauses)} clauses covering the following areas:",
    ]

    # List clause types
    for clause_type, count in sorted(
        clause_type_counts.items(), key=lambda x: x[1], reverse=True
    ):
        summary_parts.append(f"  • {clause_type.replace('_', ' ').title()}: {count} clauses")

    # Risk summary
    summary_parts.append(f"\nRisk Assessment:")
    summary_parts.append(f"  • High Risk: {risk_counts['high']} clauses")
    summary_parts.append(f"  • Medium Risk: {risk_counts['medium']} clauses")
    summary_parts.append(f"  • Low Risk: {risk_counts['low']} clauses")

    # Overall assessment
    if risk_counts["high"] > 0:
        summary_parts.append(
            "\n⚠️  This contract contains high-risk clauses that require careful review."
        )
    elif risk_counts["medium"] > 3:
        summary_parts.append(
            "\n⚠️  This contract has several medium-risk items worth reviewing."
        )
    else:
        summary_parts.append("\n✓ This contract appears to have standard, low-risk terms.")

    return "\n".join(summary_parts)


def get_key_risks(contract: Contract, limit: int = 5) -> list[str]:
    """
    Extract key risk points from a contract.

    Args:
        contract: Contract to analyze
        limit: Maximum number of risks to return

    Returns:
        List of key risk descriptions
    """
    high_risk_clauses = [
        clause for clause in contract.clauses if clause.risk_level == "high"
    ]

    risks = []
    for clause in high_risk_clauses[:limit]:
        clause_type_str = _get_clause_type_value(clause).replace("_", " ").title()
        risk_text = f"{clause_type_str}: {clause.text[:100]}..."
        risks.append(risk_text)

    return risks


def _get_clause_type_value(clause) -> str:
    """Normalize clause_type to a plain string regardless of enum usage."""
    clause_type = getattr(clause, "clause_type", "")
    if hasattr(clause_type, "value"):
        return clause_type.value
    return str(clause_type)



