"""Prompt templates for LLM tasks."""

# Clause classification prompt
CLAUSE_CLASSIFICATION_PROMPT = """Analyze the following contract clause and classify it into one of these categories:
- termination (clauses about ending the agreement)
- liability (clauses about legal responsibility, indemnification, damages)
- payment (clauses about compensation, fees, salary)
- confidentiality (clauses about non-disclosure, trade secrets)
- ip (intellectual property ownership, copyright, patents)
- non_compete (non-compete, non-solicitation agreements)
- misc (miscellaneous or general clauses)

Clause text:
{clause_text}

Respond with just the category name (lowercase, use underscores).
"""

# Contract summary prompt
CONTRACT_SUMMARY_PROMPT = """You are a legal expert. Analyze the following contract and provide a clear, plain-English summary.

Your summary should include:
1. Type of contract and parties involved (if identifiable)
2. Main purpose and obligations
3. Key terms (duration, payment, etc.)
4. Notable rights and restrictions
5. Important risks or concerns

Contract text:
{contract_text}

Provide a comprehensive but concise summary (2-3 paragraphs).
"""

# Risk explanation prompt
RISK_EXPLANATION_PROMPT = """Explain the potential risks in this contract clause in plain English.

Clause type: {clause_type}
Clause text:
{clause_text}

Provide:
1. Why this clause might be risky
2. Potential negative consequences
3. What to watch out for

Be specific and practical.
"""

# Negotiation suggestions prompt
NEGOTIATION_SUGGESTIONS_PROMPT = """You are a contract negotiation advisor. Review this clause and suggest specific negotiation points.

Clause type: {clause_type}
Risk level: {risk_level}
Clause text:
{clause_text}

Provide 3-5 specific, actionable negotiation suggestions that could reduce risk or improve terms.
Format as a JSON array of strings.
"""

# Chat/QA prompt
CONTRACT_QA_PROMPT = """You are a legal contract assistant. Answer the user's question about their contract based on the relevant clauses provided.

Relevant clauses:
{context}

User question: {question}

Provide a clear, accurate answer. If the answer isn't in the provided context, say so.
Be specific and cite relevant clause details when possible.
"""

# Risk scoring prompt (for LLM-enhanced scoring)
RISK_SCORING_PROMPT = """Analyze this contract clause and assign a risk score from 0.0 (no risk) to 1.0 (high risk).

Clause type: {clause_type}
Clause text:
{clause_text}

Consider:
- Unfavorable terms
- Lack of protections
- Ambiguous language
- Potential for disputes
- One-sided obligations

Respond with a JSON object:
{{
    "score": <float between 0.0 and 1.0>,
    "reasons": [<list of reasons for this score>]
}}
"""


