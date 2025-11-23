"""Clause data model."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ClauseType(str, Enum):
    """Types of contract clauses."""

    TERMINATION = "termination"
    LIABILITY = "liability"
    PAYMENT = "payment"
    CONFIDENTIALITY = "confidentiality"
    IP = "ip"
    NON_COMPETE = "non_compete"
    MISC = "misc"
    UNSURE = "unsure"


class Clause(BaseModel):
    """Represents a single clause in a contract."""

    id: str = Field(..., description="Unique identifier for the clause")
    contract_id: str = Field(..., description="ID of the parent contract")
    index: int = Field(..., description="Position index in the contract")
    text: str = Field(..., description="The actual clause text")
    clause_type: ClauseType = Field(
        default=ClauseType.UNSURE, description="Classification of the clause"
    )
    start_char: int | None = Field(
        default=None, description="Starting character position in original text"
    )
    end_char: int | None = Field(
        default=None, description="Ending character position in original text"
    )
    risk_score: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Risk score between 0-1"
    )
    risk_level: Literal["low", "medium", "high"] | None = Field(
        default=None, description="Categorical risk level"
    )
    embedding_id: str | None = Field(
        default=None, description="Reference to vector store embedding"
    )

    class Config:
        """Pydantic config."""

        use_enum_values = True



