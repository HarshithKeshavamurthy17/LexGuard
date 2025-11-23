"""Identify parties involved in the contract."""

import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def identify_parties(text: str) -> List[Dict[str, str]]:
    """
    Identify parties to the contract.

    Args:
        text: Contract text

    Returns:
        List of identified parties with roles
    """
    logger.info("Identifying parties in contract")

    parties = []

    # Look for common patterns
    patterns = [
        # "This Agreement is between X and Y"
        r'(?:between|by and between)\s+([^,]+?)\s+(?:and|&)\s+([^,\.]+)',
        # "Party A (Company Inc.)"
        r'([A-Z][A-Za-z\s&]+(?:LLC|Inc|Corp|Ltd|LLP|L\.L\.C\.|Corporation)\.?)',
        # "hereinafter referred to as 'X'"
        r'referred to as\s+["\']([^"\']+)["\']',
    ]

    text_start = text[:2000]  # Focus on first part where parties are usually mentioned

    for i, pattern in enumerate(patterns):
        matches = re.finditer(pattern, text_start, re.IGNORECASE)
        
        for match in matches:
            if i == 0:  # between pattern
                parties.append({"name": match.group(1).strip(), "role": "Party 1"})
                parties.append({"name": match.group(2).strip(), "role": "Party 2"})
            else:
                party_name = match.group(1).strip()
                if len(party_name) > 5 and party_name not in [p["name"] for p in parties]:
                    role = determine_party_role(party_name, text)
                    parties.append({"name": party_name, "role": role})

    # Remove duplicates
    seen = set()
    unique_parties = []
    for party in parties:
        if party["name"] not in seen:
            seen.add(party["name"])
            unique_parties.append(party)

    return unique_parties[:5]  # Top 5


def determine_party_role(party_name: str, text: str) -> str:
    """Determine the role of a party based on context."""
    text_lower = text.lower()
    party_lower = party_name.lower()

    # Look for role indicators near the party name
    if re.search(rf'{party_lower}.*?(?:employer|company)', text_lower[:1000]):
        return "Employer/Company"
    elif re.search(rf'{party_lower}.*?(?:employee|contractor)', text_lower[:1000]):
        return "Employee/Contractor"
    elif re.search(rf'{party_lower}.*?(?:vendor|supplier)', text_lower[:1000]):
        return "Vendor/Supplier"
    elif re.search(rf'{party_lower}.*?(?:client|customer)', text_lower[:1000]):
        return "Client/Customer"
    else:
        return "Party"



