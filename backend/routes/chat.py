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

        # Generate answer using LLM
        logger.info("Generating answer with LLM...")
        llm = get_llm_client()

        prompt = CONTRACT_QA_PROMPT.format(context=context, question=request.query)

        messages = [
            {
                "role": "system",
                "content": "You are a legal contract assistant. Answer questions accurately based on the provided contract clauses.",
            },
            {"role": "user", "content": prompt},
        ]

        answer = llm.chat(messages, temperature=0.5, max_tokens=500)

        logger.info("Successfully generated answer")

        return ChatResponse(answer=answer, relevant_clauses=relevant_clauses)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Error processing your question. Please try again."
        )


