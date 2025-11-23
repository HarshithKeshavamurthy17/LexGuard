"""Contract data model."""

from datetime import datetime

from pydantic import BaseModel, Field

from lexguard.models.clause import Clause


class Contract(BaseModel):
    """Represents a legal contract document."""

    id: str = Field(..., description="Unique identifier for the contract")
    title: str = Field(..., description="Contract title or name")
    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow, description="Upload timestamp"
    )
    original_filename: str = Field(..., description="Original file name")
    text: str = Field(..., description="Full extracted text of the contract")
    clauses: list[Clause] = Field(default_factory=list, description="List of clauses")

    class Config:
        """Pydantic config."""

        json_encoders = {datetime: lambda v: v.isoformat()}



