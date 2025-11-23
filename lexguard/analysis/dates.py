"""Extract important dates from contracts."""

import re
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


def extract_important_dates(text: str) -> List[Dict[str, str]]:
    """
    Extract important dates and deadlines from contract.

    Args:
        text: Contract text

    Returns:
        List of dates with context
    """
    logger.info("Extracting important dates from contract")

    dates = []

    # Date patterns
    patterns = [
        # MM/DD/YYYY or DD/MM/YYYY
        (r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', 'date'),
        # Month DD, YYYY
        (r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})', 'date'),
        # Effective date
        (r'effective\s+(?:date|as of)\s*[:]?\s*([^,\.]+)', 'effective_date'),
        # Term duration
        (r'term of\s+(\d+\s+(?:day|week|month|year)s?)', 'term'),
        # Expiration
        (r'expir(?:e|ation|y)\s+(?:date|on)?\s*[:]?\s*([^,\.]+)', 'expiration'),
        # Renewal
        (r'renew(?:al)?\s+(?:date|on)?\s*[:]?\s*([^,\.]+)', 'renewal'),
        # Deadline
        (r'deadline\s+(?:of|for|is)?\s*[:]?\s*([^,\.]+)', 'deadline'),
    ]

    for pattern, date_type in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            date_str = match.group(1).strip()
            
            # Get context (20 chars before and after)
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 30)
            context = text[start:end].replace('\n', ' ')

            dates.append({
                "date": date_str,
                "type": date_type,
                "context": context.strip()
            })

    return dates[:10]  # Top 10 most important


def parse_date(date_str: str) -> datetime:
    """
    Try to parse a date string into datetime.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime object or None if can't parse
    """
    formats = [
        '%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y', '%d-%m-%Y',
        '%B %d, %Y', '%b %d, %Y',
        '%Y-%m-%d'
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    return None



