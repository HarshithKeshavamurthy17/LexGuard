"""Contract summary generation."""

import logging
from typing import Optional

from lexguard.models.contract import Contract

logger = logging.getLogger(__name__)


def build_contract_summary(contract: Contract, use_llm: bool = False) -> str:
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
    Generate a comprehensive rule-based summary with detailed analysis.

    Args:
        contract: Contract to summarize

    Returns:
        Detailed summary text
    """
    clauses = contract.clauses

    # Count clause types and risks
    clause_type_counts = {}
    risk_counts = {"high": 0, "medium": 0, "low": 0}
    high_risk_clauses = []
    key_clauses_by_type = {}

    for clause in clauses:
        # Count clause types
        clause_type = _get_clause_type_value(clause)
        clause_type_counts[clause_type] = clause_type_counts.get(clause_type, 0) + 1

        # Count risk levels
        if clause.risk_level:
            risk_counts[clause.risk_level] += 1
            if clause.risk_level == "high":
                high_risk_clauses.append(clause)

        # Collect key clauses by type (first 2 of each type)
        if clause_type not in key_clauses_by_type or len(key_clauses_by_type[clause_type]) < 2:
            if clause_type not in key_clauses_by_type:
                key_clauses_by_type[clause_type] = []
            key_clauses_by_type[clause_type].append(clause)

    # Build comprehensive summary
    summary_parts = [
        f"📄 **Contract Summary: {contract.title}**",
        f"\n📋 **Document Information:**",
        f"  • File: {contract.original_filename}",
        f"  • Uploaded: {contract.uploaded_at.strftime('%Y-%m-%d %H:%M')}",
        f"  • Total Clauses: {len(clauses)}",
        f"\n📊 **Contract Overview:**",
        f"\nThis contract contains {len(clauses)} clauses covering the following areas:",
    ]

    # List clause types with counts
    for clause_type, count in sorted(
        clause_type_counts.items(), key=lambda x: x[1], reverse=True
    ):
        clause_type_display = clause_type.replace('_', ' ').title()
        summary_parts.append(f"  • **{clause_type_display}**: {count} clause{'s' if count != 1 else ''}")

    # Risk assessment
    summary_parts.append(f"\n⚠️ **Risk Assessment:**")
    summary_parts.append(f"  • 🔴 High Risk: {risk_counts['high']} clause{'s' if risk_counts['high'] != 1 else ''}")
    summary_parts.append(f"  • 🟡 Medium Risk: {risk_counts['medium']} clause{'s' if risk_counts['medium'] != 1 else ''}")
    summary_parts.append(f"  • 🟢 Low Risk: {risk_counts['low']} clause{'s' if risk_counts['low'] != 1 else ''}")

    # Overall assessment with details
    if risk_counts["high"] > 0:
        summary_parts.append(
            f"\n⚠️ **Warning**: This contract contains {risk_counts['high']} high-risk clause(s) that require careful review. "
            "Pay special attention to liability, termination, and payment terms."
        )
    elif risk_counts["medium"] > 3:
        summary_parts.append(
            f"\n⚠️ **Note**: This contract has {risk_counts['medium']} medium-risk items worth reviewing. "
            "Consider discussing key terms with your legal advisor."
        )
    else:
        summary_parts.append(
            "\n✓ **Assessment**: This contract appears to have standard, low-risk terms. "
            "However, always review all clauses carefully before signing."
        )

    # Key highlights by type
    summary_parts.append(f"\n🔍 **Key Highlights:**")
    
    # Payment terms
    if "payment" in clause_type_counts:
        payment_clauses = key_clauses_by_type.get("payment", [])
        if payment_clauses:
            summary_parts.append(f"\n💰 **Payment Terms:**")
            for clause in payment_clauses[:2]:
                snippet = clause.text[:200] + "..." if len(clause.text) > 200 else clause.text
                summary_parts.append(f"  • {snippet}")

    # Termination terms
    if "termination" in clause_type_counts:
        term_clauses = key_clauses_by_type.get("termination", [])
        if term_clauses:
            summary_parts.append(f"\n🚪 **Termination Conditions:**")
            for clause in term_clauses[:2]:
                snippet = clause.text[:200] + "..." if len(clause.text) > 200 else clause.text
                summary_parts.append(f"  • {snippet}")

    # Liability terms
    if "liability" in clause_type_counts:
        liability_clauses = key_clauses_by_type.get("liability", [])
        if liability_clauses:
            summary_parts.append(f"\n🛡️ **Liability Terms:**")
            for clause in liability_clauses[:2]:
                snippet = clause.text[:200] + "..." if len(clause.text) > 200 else clause.text
                summary_parts.append(f"  • {snippet}")

    # High-risk clause warnings
    if high_risk_clauses:
        summary_parts.append(f"\n🚨 **High-Risk Clauses Requiring Attention:**")
        for clause in high_risk_clauses[:3]:
            clause_type = _get_clause_type_value(clause).replace("_", " ").title()
            snippet = clause.text[:180] + "..." if len(clause.text) > 180 else clause.text
            summary_parts.append(f"  • **{clause_type}**: {snippet}")

    # Recommendations
    summary_parts.append(f"\n💡 **Recommendations:**")
    if risk_counts["high"] > 0:
        summary_parts.append("  • Review all high-risk clauses with a legal professional")
        summary_parts.append("  • Consider negotiating terms for high-risk areas")
    summary_parts.append("  • Use the 'Questions' tab to explore specific contract terms")
    summary_parts.append("  • Download the full PDF report for detailed analysis")
    summary_parts.append("  • Keep this analysis for your records")

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



