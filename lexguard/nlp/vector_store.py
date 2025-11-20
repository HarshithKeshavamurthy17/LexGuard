"""Vector store interface for semantic search."""

import logging
from typing import List, Optional

from lexguard.models.clause import Clause
from lexguard.nlp.embedders import get_embedding, get_embeddings_batch

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Vector store for clause embeddings and semantic search.

    Uses ChromaDB for local storage and retrieval.
    """

    def __init__(self, collection_name: str = "clauses"):
        """
        Initialize vector store.

        Args:
            collection_name: Name of the ChromaDB collection
        """
        from lexguard.storage.chroma_store import get_chroma_client

        self.client = get_chroma_client()
        self.collection_name = collection_name

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Legal contract clauses"},
        )

        logger.info(f"Initialized vector store with collection: {collection_name}")

    def upsert_clauses(self, contract_id: str, clauses: List[Clause]) -> None:
        """
        Add or update clauses in the vector store.

        Args:
            contract_id: ID of the parent contract
            clauses: List of clauses to store
        """
        if not clauses:
            logger.warning("No clauses to upsert")
            return

        logger.info(f"Upserting {len(clauses)} clauses for contract {contract_id}")

        # Generate embeddings for all clauses
        texts = [clause.text for clause in clauses]
        embeddings = get_embeddings_batch(texts)

        # Prepare data for ChromaDB
        ids = [clause.id for clause in clauses]
        metadatas = [
            {
                "contract_id": clause.contract_id,
                "clause_type": clause.clause_type if isinstance(clause.clause_type, str) else clause.clause_type.value,
                "index": clause.index,
                "risk_level": clause.risk_level or "unknown",
            }
            for clause in clauses
        ]

        # Upsert to ChromaDB
        self.collection.upsert(
            ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas
        )

        logger.info(f"Successfully upserted {len(clauses)} clauses")

    def search_similar(
        self, contract_id: str, query: str, k: int = 5
    ) -> List[dict]:
        """
        Search for similar clauses using semantic search.

        Args:
            contract_id: Filter by contract ID
            query: Search query
            k: Number of results to return

        Returns:
            List of search results with clause data
        """
        logger.info(f"Searching for similar clauses: '{query[:50]}...'")

        # Generate query embedding
        query_embedding = get_embedding(query)

        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={"contract_id": contract_id},
        )

        # Format results
        search_results = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                search_results.append(
                    {
                        "id": results["ids"][0][i],
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i]
                        if "distances" in results
                        else None,
                    }
                )

        logger.info(f"Found {len(search_results)} similar clauses")
        return search_results

    def delete_contract_clauses(self, contract_id: str) -> None:
        """
        Delete all clauses for a specific contract.

        Args:
            contract_id: Contract ID to delete
        """
        logger.info(f"Deleting clauses for contract {contract_id}")

        # Query all clause IDs for this contract
        results = self.collection.get(where={"contract_id": contract_id})

        if results["ids"]:
            self.collection.delete(ids=results["ids"])
            logger.info(f"Deleted {len(results['ids'])} clauses")
        else:
            logger.info("No clauses found to delete")

    def get_clause_by_id(self, clause_id: str) -> Optional[dict]:
        """
        Retrieve a specific clause by ID.

        Args:
            clause_id: Clause ID

        Returns:
            Clause data or None if not found
        """
        results = self.collection.get(ids=[clause_id])

        if results["ids"]:
            return {
                "id": results["ids"][0],
                "text": results["documents"][0],
                "metadata": results["metadatas"][0],
            }

        return None

