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

        # RAG-Only Mode: Construct answer directly from retrieved clauses
        logger.info("RAG-Only Mode V2 ACTIVATED: Constructing answer from retrieved clauses...")
        
        intro = f"**Based on the document, here are the relevant sections regarding '{request.query}':**\n\n"
        
        highlights = []
        for result in search_results:
            clause_text = result["text"].strip()
            metadata = result["metadata"]
            clause_type = metadata.get("clause_type", "Clause").replace("_", " ").title()
            
            # Format each clause as a distinct block
            highlights.append(f"**{clause_type}**\n> {clause_text}")

        answer = intro + "\n\n".join(highlights)
        
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
    Provide a deterministic fallback answer based on retrieved clauses when the LLM fails.
    """
    if not clauses:
        return (
            "I couldn't reach the AI model, and there were no relevant clauses to reference. "
            "Please try rephrasing your question or re-running the analysis."
        )

    intro = (
        "I couldn't reach the AI model, so here's a quick summary based on the clauses I found:\n"
    )
    highlights = []
    for clause in clauses:
        clause_type = clause.get("type", "clause").replace("_", " ").title()
        text = clause.get("text", "").strip()
        snippet = text if len(text) <= 280 else text[:280].rstrip() + "..."
        highlights.append(f"- {clause_type}: {snippet}")

    outro = (
        "\nIf you need more detail, try refining the question or download the report for the full text."
    )

    return intro + "\n".join(highlights) + outro



