"""Chat/Q&A endpoints for contract analysis."""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from lexguard.llm import get_llm_client
from lexguard.llm.prompts import CONTRACT_QA_PROMPT
from lexguard.nlp import VectorStore
from lexguard.storage import load_contract

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    query: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    answer: str
    relevant_clauses: list[dict]


@router.post("/contracts/{contract_id}/chat", response_model=ChatResponse)
async def chat_with_contract(contract_id: str, request: ChatRequest):
    """
    Chat with a contract using RAG (Retrieval-Augmented Generation).

    Steps:
    1. Retrieve similar clauses from vector store
    2. Build context with relevant clauses
    3. Generate answer using LLM

    Args:
        contract_id: Contract ID
        request: Chat request with query

    Returns:
        Answer and relevant clauses
    """
    # Verify contract exists
    contract = load_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        # Retrieve similar clauses using vector search
        logger.info(f"Searching for relevant clauses: {request.query}")
        vector_store = VectorStore()
        search_results = vector_store.search_similar(
            contract_id=contract_id, query=request.query, k=5
        )

        if not search_results:
            return ChatResponse(
                answer="I couldn't find relevant clauses to answer your question. Try rephrasing or ask about specific topics like termination, liability, or payment.",
                relevant_clauses=[],
            )

        # Build context from search results
        context_parts = []
        relevant_clauses = []

        for i, result in enumerate(search_results, 1):
            clause_text = result["text"]
            metadata = result["metadata"]

            context_parts.append(
                f"Clause {i} [{metadata.get('clause_type', 'unknown')}]:\n{clause_text}\n"
            )

            relevant_clauses.append(
                {
                    "id": result["id"],
                    "text": clause_text[:200] + "..."
                    if len(clause_text) > 200
                    else clause_text,
                    "type": metadata.get("clause_type", "unknown"),
                    "risk_level": metadata.get("risk_level", "unknown"),
                }
            )

        context = "\n".join(context_parts)

        # Try LLM first, but always have rule-based fallback
        logger.info("Generating answer...")
        llm = get_llm_client()

        # Check if LLM is disabled
        use_llm = True
        try:
            # Try to use LLM
            prompt = CONTRACT_QA_PROMPT.format(context=context, question=request.query)

            messages = [
                {
                    "role": "system",
                    "content": "You are a legal contract assistant. Answer questions accurately based on the provided contract clauses.",
                },
                {"role": "user", "content": prompt},
            ]

            answer = llm.chat(messages, temperature=0.5, max_tokens=500)
            logger.info("Successfully generated answer with LLM")
            return ChatResponse(answer=answer, relevant_clauses=relevant_clauses)
        except (RuntimeError, Exception) as llm_error:
            # LLM disabled or failed - use rule-based answer
            logger.info("Using rule-based answer (LLM disabled or unavailable)")
            answer = _build_rule_based_chat_answer(request.query, relevant_clauses)
            return ChatResponse(answer=answer, relevant_clauses=relevant_clauses)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Error processing your question. Please try again."
        )


def _build_rule_based_chat_answer(question: str, clauses: list[dict]) -> str:
    """
    Provide an intelligent rule-based answer based on question patterns and retrieved clauses.
    """
    if not clauses:
        return (
            "I couldn't find relevant clauses to answer your question. "
            "Try rephrasing or ask about specific topics like termination, liability, payment, or obligations."
        )

    question_lower = question.lower()
    
    # Pattern matching for common question types
    answer_parts = []
    
    # Obligations questions
    if any(word in question_lower for word in ["obligation", "responsibilit", "duty", "must", "required", "deliverable"]):
        answer_parts.append("**Based on the contract clauses, here are the key obligations:**\n\n")
        obligation_clauses = [c for c in clauses if "obligation" in c.get("text", "").lower() or 
                             c.get("type", "") in ["payment", "termination", "confidentiality"]]
        if not obligation_clauses:
            obligation_clauses = clauses[:3]  # Fallback to first few
        
        for i, clause in enumerate(obligation_clauses[:5], 1):
            clause_type = clause.get("type", "clause").replace("_", " ").title()
            text = clause.get("text", "").strip()
            snippet = text[:300] + "..." if len(text) > 300 else text
            answer_parts.append(f"{i}. **{clause_type}**: {snippet}\n")
    
    # Payment questions
    elif any(word in question_lower for word in ["payment", "fee", "cost", "price", "amount", "due", "refund"]):
        answer_parts.append("**Payment and Financial Terms:**\n\n")
        payment_clauses = [c for c in clauses if c.get("type") == "payment" or 
                          any(word in c.get("text", "").lower() for word in ["payment", "fee", "cost", "amount", "$"])]
        if not payment_clauses:
            payment_clauses = clauses[:3]
        
        for i, clause in enumerate(payment_clauses[:5], 1):
            text = clause.get("text", "").strip()
            snippet = text[:350] + "..." if len(text) > 350 else text
            answer_parts.append(f"{i}. {snippet}\n")
    
    # Termination questions
    elif any(word in question_lower for word in ["terminat", "end", "cancel", "exit", "leave", "notice period"]):
        answer_parts.append("**Termination and Exit Conditions:**\n\n")
        term_clauses = [c for c in clauses if c.get("type") == "termination" or 
                       any(word in c.get("text", "").lower() for word in ["terminat", "cancel", "end", "notice"])]
        if not term_clauses:
            term_clauses = clauses[:3]
        
        for i, clause in enumerate(term_clauses[:5], 1):
            text = clause.get("text", "").strip()
            snippet = text[:350] + "..." if len(text) > 350 else text
            answer_parts.append(f"{i}. {snippet}\n")
    
    # Liability questions
    elif any(word in question_lower for word in ["liability", "indemnif", "damage", "risk", "responsible"]):
        answer_parts.append("**Liability and Risk Assessment:**\n\n")
        liability_clauses = [c for c in clauses if c.get("type") == "liability" or 
                            c.get("risk_level") in ["high", "medium"] or
                            any(word in c.get("text", "").lower() for word in ["liability", "indemnif", "damage"])]
        if not liability_clauses:
            liability_clauses = clauses[:3]
        
        for i, clause in enumerate(liability_clauses[:5], 1):
            clause_type = clause.get("type", "clause").replace("_", " ").title()
            risk = clause.get("risk_level", "unknown").upper()
            text = clause.get("text", "").strip()
            snippet = text[:300] + "..." if len(text) > 300 else text
            answer_parts.append(f"{i}. **{clause_type}** (Risk: {risk}): {snippet}\n")
    
    # Time/Date questions
    elif any(word in question_lower for word in ["date", "deadline", "duration", "term", "when", "time", "period"]):
        answer_parts.append("**Important Dates and Timeframes:**\n\n")
        date_clauses = [c for c in clauses if any(word in c.get("text", "").lower() for word in 
                          ["date", "deadline", "duration", "term", "period", "day", "month", "year"])]
        if not date_clauses:
            date_clauses = clauses[:3]
        
        for i, clause in enumerate(date_clauses[:5], 1):
            text = clause.get("text", "").strip()
            snippet = text[:350] + "..." if len(text) > 350 else text
            answer_parts.append(f"{i}. {snippet}\n")
    
    # IP questions
    elif any(word in question_lower for word in ["intellectual property", "ip", "copyright", "patent", "ownership"]):
        answer_parts.append("**Intellectual Property Terms:**\n\n")
        ip_clauses = [c for c in clauses if c.get("type") == "ip" or 
                     any(word in c.get("text", "").lower() for word in ["intellectual", "copyright", "patent", "ownership"])]
        if not ip_clauses:
            ip_clauses = clauses[:3]
        
        for i, clause in enumerate(ip_clauses[:5], 1):
            text = clause.get("text", "").strip()
            snippet = text[:350] + "..." if len(text) > 350 else text
            answer_parts.append(f"{i}. {snippet}\n")
    
    # Default: General answer
    else:
        answer_parts.append("**Relevant Contract Clauses:**\n\n")
        for i, clause in enumerate(clauses[:5], 1):
            clause_type = clause.get("type", "clause").replace("_", " ").title()
            risk = clause.get("risk_level", "unknown")
            text = clause.get("text", "").strip()
            snippet = text[:280] + "..." if len(text) > 280 else text
            answer_parts.append(f"{i}. **{clause_type}** ({risk} risk): {snippet}\n")
    
    # Add summary note
    answer_parts.append("\n---\n")
    answer_parts.append("💡 **Tip**: Review the full clause text in the 'Clause Analysis' tab for complete details. "
                        "Download the PDF report for a comprehensive analysis.")
    
    return "".join(answer_parts)



