"""Extract key terms and defined terms from contracts."""

import re
import logging
from typing import List, Dict
from collections import Counter

logger = logging.getLogger(__name__)


def extract_key_terms(text: str) -> Dict[str, List[str]]:
    """
    Extract key terms, definitions, and important concepts.

    Args:
        text: Contract text

    Returns:
        Dictionary with categorized terms
    """
    logger.info("Extracting key terms from contract")

    key_terms = {
        "defined_terms": extract_defined_terms(text),
        "monetary_amounts": extract_monetary_amounts(text),
        "important_entities": extract_entities(text),
        "time_periods": extract_time_periods(text),
        "key_concepts": extract_key_concepts(text),
    }

    logger.info(f"Extracted {sum(len(v) for v in key_terms.values())} key terms")
    return key_terms


def extract_defined_terms(text: str) -> List[Dict[str, str]]:
    """Extract defined terms (capitalized terms in quotes or after 'means')."""
    defined_terms = []

    # Pattern 1: "Term" means something
    pattern1 = r'"([A-Z][^"]+)"\s+(?:means?|refers? to|is defined as)'
    for match in re.finditer(pattern1, text):
        term = match.group(1)
        # Get definition (next 100 chars)
        start = match.end()
        definition = text[start:start + 100].split('.')[0].strip()
        defined_terms.append({"term": term, "definition": definition})

    # Pattern 2: Capitalized terms that appear multiple times
    capitalized = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b', text)
    common_caps = [term for term, count in Counter(capitalized).items() if count >= 3]

    for term in common_caps[:10]:  # Top 10
        if not any(d["term"] == term for d in defined_terms):
            defined_terms.append({"term": term, "definition": "Frequent term in contract"})

    return defined_terms[:15]  # Limit to 15


def extract_monetary_amounts(text: str) -> List[Dict[str, str]]:
    """Extract monetary amounts and what they're for."""
    amounts = []

    # Pattern for money
    pattern = r'\$\s*([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)\s*(?:per|for|to|as)?\s*([a-zA-Z\s]{0,30})'
    
    for match in re.finditer(pattern, text):
        amount = match.group(1)
        context = match.group(2).strip() if match.group(2) else ""
        amounts.append({
            "amount": f"${amount}",
            "context": context or "Not specified"
        })

    return amounts[:10]  # Top 10


def extract_entities(text: str) -> List[str]:
    """Extract company/entity names."""
    entities = []

    # Look for LLC, Inc, Corp, Ltd
    pattern = r'\b([A-Z][A-Za-z\s&]+(?:LLC|Inc|Corp|Ltd|LLP|L\.L\.C\.|Corporation)\.?)\b'
    matches = re.findall(pattern, text)

    entities = list(set(matches))[:10]
    return entities


def extract_time_periods(text: str) -> List[Dict[str, str]]:
    """Extract time periods and durations."""
    periods = []

    # Pattern for durations
    patterns = [
        (r'(\d+)\s*(day|week|month|year)s?', 'duration'),
        (r'(within|after|before)\s+(\d+)\s+(day|week|month|year)s?', 'relative_time'),
        (r'(annual|monthly|weekly|daily|quarterly)', 'frequency'),
    ]

    for pattern, period_type in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            periods.append({
                "text": match.group(0),
                "type": period_type
            })

    return periods[:10]


def extract_key_concepts(text: str) -> List[str]:
    """Extract important legal concepts mentioned."""
    legal_concepts = [
        "confidentiality", "indemnification", "termination", "liability",
        "intellectual property", "non-compete", "non-solicitation",
        "arbitration", "jurisdiction", "force majeure", "warranties",
        "representations", "governing law", "severability", "amendment"
    ]

    text_lower = text.lower()
    found_concepts = []

    for concept in legal_concepts:
        if concept in text_lower:
            # Count occurrences
            count = text_lower.count(concept)
            found_concepts.append(f"{concept.title()} ({count}x)")

    return found_concepts[:12]



