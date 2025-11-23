"""Risk assessment models."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk level categories."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ClauseRisk(BaseModel):
    """Risk assessment for a single clause."""

    clause_id: str = Field(..., description="ID of the clause being assessed")
    score: float = Field(..., ge=0.0, le=1.0, description="Numerical risk score (0-1)")
    level: Literal["low", "medium", "high"] = Field(..., description="Risk category")
    reasons: list[str] = Field(
        default_factory=list, description="Reasons for the risk assessment"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Suggested actions or negotiation points"
    )

    class Config:
        """Pydantic config."""

        use_enum_values = True



