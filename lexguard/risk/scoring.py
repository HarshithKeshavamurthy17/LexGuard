"""Risk scoring logic for contract clauses."""

import re
import logging
from typing import Literal, Tuple, List

from lexguard.models.clause import Clause, ClauseType
from lexguard.models.risk import ClauseRisk

logger = logging.getLogger(__name__)


def calculate_clause_risk(clause: Clause, use_llm: bool = False) -> ClauseRisk:
    """
    Calculate risk assessment for a clause.

    Args:
        clause: Clause to assess
        use_llm: Whether to use LLM for enhanced scoring

    Returns:
        ClauseRisk assessment
    """
    # Calculate base score using rules
    score, reasons = _calculate_risk_score(clause)

    # Optionally enhance with LLM
    if use_llm:
        try:
            llm_score, llm_reasons = _calculate_risk_with_llm(clause)
            # Blend scores (70% LLM, 30% rules)
            score = 0.7 * llm_score + 0.3 * score
            reasons.extend(llm_reasons)
        except Exception as e:
            logger.warning(f"LLM risk scoring failed: {e}")

    # Convert score to level
    level = score_to_level(score)

    # Update clause with risk info
    clause.risk_score = score
    clause.risk_level = level

    return ClauseRisk(
        clause_id=clause.id,
        score=score,
        level=level,
        reasons=reasons,
        recommendations=[],  # Will be filled by negotiation module
    )


def _calculate_risk_score(clause: Clause) -> Tuple[float, List[str]]:
    """
    Calculate risk score using rule-based heuristics.

    Returns:
        (score, reasons) tuple
    """
    score = 0.0
    reasons = []
    text_lower = clause.text.lower()

    # Base risk by clause type
    type_risk = {
        ClauseType.LIABILITY: 0.6,
        ClauseType.NON_COMPETE: 0.5,
        ClauseType.TERMINATION: 0.4,
        ClauseType.IP: 0.4,
        ClauseType.CONFIDENTIALITY: 0.3,
        ClauseType.PAYMENT: 0.2,
        ClauseType.MISC: 0.1,
        ClauseType.UNSURE: 0.2,
    }
    score = type_risk.get(clause.clause_type, 0.2)

    # Liability-specific risks
    if clause.clause_type == ClauseType.LIABILITY:
        if re.search(r"\bunlimited\b", text_lower):
            score += 0.2
            reasons.append("Contains 'unlimited' liability")

        if re.search(r"\bindemnif(?:y|ication)\b", text_lower):
            score += 0.15
            reasons.append("Includes indemnification obligations")

        if re.search(r"\bhold\s+harmless\b", text_lower):
            score += 0.1
            reasons.append("Contains hold harmless clause")

        if not re.search(r"\blimit(?:ed|ation)\b", text_lower):
            score += 0.1
            reasons.append("No liability limitation mentioned")

    # Termination-specific risks
    elif clause.clause_type == ClauseType.TERMINATION:
        # Check for short notice periods
        notice_match = re.search(r"(\d+)\s*(?:day|hour)", text_lower)
        if notice_match:
            days = int(notice_match.group(1))
            if days < 7:
                score += 0.25
                reasons.append(f"Very short notice period ({days} days)")
            elif days < 30:
                score += 0.1
                reasons.append(f"Short notice period ({days} days)")

        if re.search(r"\bimmediate(?:ly)?\b", text_lower):
            score += 0.2
            reasons.append("Allows immediate termination")

        if re.search(r"\bwithout\s+cause\b", text_lower):
            score += 0.15
            reasons.append("Allows termination without cause")

    # Non-compete specific risks
    elif clause.clause_type == ClauseType.NON_COMPETE:
        # Check duration
        duration_match = re.search(r"(\d+)\s*(?:year|month)", text_lower)
        if duration_match:
            value = int(duration_match.group(1))
            if "year" in text_lower:
                months = value * 12
            else:
                months = value

            if months > 24:
                score += 0.3
                reasons.append(f"Very long non-compete duration ({months} months)")
            elif months > 12:
                score += 0.15
                reasons.append(f"Long non-compete duration ({months} months)")

        if re.search(r"\bglobal(?:ly)?\b|\bworldwide\b", text_lower):
            score += 0.2
            reasons.append("Global or worldwide scope")

    # IP-specific risks
    elif clause.clause_type == ClauseType.IP:
        if re.search(r"\ball\s+(?:work|invention|creation)", text_lower):
            score += 0.15
            reasons.append("Broad IP assignment clause")

        if not re.search(r"\bpre-existing\b", text_lower):
            score += 0.1
            reasons.append("No mention of pre-existing IP")

    # Payment-specific checks
    elif clause.clause_type == ClauseType.PAYMENT:
        if re.search(r"\bno\s+(?:pay|compensation|salary)\b", text_lower):
            score += 0.4
            reasons.append("Unpaid or volunteer position")

        if re.search(r"\bat\s+will\b", text_lower):
            score += 0.1
            reasons.append("At-will payment terms")

    # General red flags
    if re.search(r"\birrevocable\b", text_lower):
        score += 0.1
        reasons.append("Contains irrevocable terms")

    if re.search(r"\bperpetual\b", text_lower):
        score += 0.15
        reasons.append("Perpetual/indefinite terms")

    if re.search(r"\bwaive\b", text_lower):
        score += 0.1
        reasons.append("Contains rights waiver")

    # Cap score at 1.0
    score = min(score, 1.0)

    if not reasons:
        # clause_type might be string or enum depending on Pydantic serialization
        clause_type_str = clause.clause_type if isinstance(clause.clause_type, str) else clause.clause_type.value
        reasons.append(f"Standard {clause_type_str} clause")

    return score, reasons


def _calculate_risk_with_llm(clause: Clause) -> Tuple[float, List[str]]:
    """
    Use LLM to assess clause risk.

    Returns:
        (score, reasons) tuple
    """
    from lexguard.llm import get_llm_client
    from lexguard.llm.prompts import RISK_SCORING_PROMPT

    llm = get_llm_client()

    clause_type_str = clause.clause_type if isinstance(clause.clause_type, str) else clause.clause_type.value
    prompt = RISK_SCORING_PROMPT.format(
        clause_type=clause_type_str, clause_text=clause.text
    )

    messages = [
        {"role": "system", "content": "You are a legal risk analyst."},
        {"role": "user", "content": prompt},
    ]

    result = llm.chat_structured(messages, schema={})

    score = float(result.get("score", 0.5))
    reasons = result.get("reasons", [])

    return score, reasons


def score_to_level(score: float) -> Literal["low", "medium", "high"]:
    """
    Convert numerical risk score to categorical level.

    Args:
        score: Risk score (0-1)

    Returns:
        Risk level category
    """
    if score < 0.33:
        return "low"
    elif score < 0.66:
        return "medium"
    else:
        return "high"

