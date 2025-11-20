"""Data schema definitions for storage."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from lexguard.models.clause import Clause


class ContractMetadata(BaseModel):
    """Lightweight contract metadata for listings."""

    id: str
    title: str
    uploaded_at: datetime
    original_filename: str
    clause_count: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int

    class Config:
        """Pydantic config."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class ContractStorage(BaseModel):
    """Storage format for persisted contracts."""

    id: str
    title: str
    uploaded_at: datetime
    original_filename: str
    text: str
    clauses: List[Clause]

    class Config:
        """Pydantic config."""

        json_encoders = {datetime: lambda v: v.isoformat()}


