"""Extract obligations and requirements from contracts."""

import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def extract_obligations(text: str) -> Dict[str, List[str]]:
    """
    Extract obligations, requirements, and prohibitions.

    Args:
        text: Contract text

    Returns:
        Dictionary with categorized obligations
    """
    logger.info("Extracting obligations from contract")

    obligations = {
        "must_do": extract_requirements(text, positive=True),
        "must_not_do": extract_requirements(text, positive=False),
        "rights": extract_rights(text),
        "responsibilities": extract_responsibilities(text),
    }

    logger.info(f"Extracted {sum(len(v) for v in obligations.values())} obligations")
    return obligations


def extract_requirements(text: str, positive: bool = True) -> List[str]:
    """Extract things that must or must not be done."""
    requirements = []

    if positive:
        # Things that MUST be done
        patterns = [
            r'(?:shall|must|required to|obligated to|agrees? to)\s+([^\.]{20,150})',
            r'(?:will|is to)\s+([^\.]{20,150})',
        ]
    else:
        # Things that MUST NOT be done
        patterns = [
            r'(?:shall not|must not|may not|prohibited from|forbidden to)\s+([^\.]{20,150})',
            r'(?:will not|cannot|restrictions? on)\s+([^\.]{20,150})',
        ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            obligation = match.group(1).strip()
            # Clean up
            obligation = re.sub(r'\s+', ' ', obligation)
            if 10 < len(obligation) < 200:
                requirements.append(obligation)

    return requirements[:8]  # Top 8


def extract_rights(text: str) -> List[str]:
    """Extract rights granted or reserved."""
    rights = []

    patterns = [
        r'(?:has the right to|entitled to|may)\s+([^\.]{20,150})',
        r'(?:reserves? the right to)\s+([^\.]{20,150})',
        r'(?:grants?|grant(?:s|ed))\s+([^\.]{20,150})',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            right = match.group(1).strip()
            right = re.sub(r'\s+', ' ', right)
            if 10 < len(right) < 200:
                rights.append(right)

    return rights[:8]


def extract_responsibilities(text: str) -> List[str]:
    """Extract general responsibilities."""
    responsibilities = []

    patterns = [
        r'(?:responsible for|responsibility to|in charge of)\s+([^\.]{20,150})',
        r'(?:duties include|responsible for)\s+([^\.]{20,150})',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            resp = match.group(1).strip()
            resp = re.sub(r'\s+', ' ', resp)
            if 10 < len(resp) < 200:
                responsibilities.append(resp)

    return responsibilities[:8]



