"""
Pydantic schemas for data validation and API serialization.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ObservationSchema(BaseModel):
    country_code: str = Field(..., min_length=2, max_length=5, description="ISO-3 or Eurostat country code")
    indicator_id: str = Field(..., min_length=2, max_length=50)
    period: int = Field(..., ge=1900, le=2100, description="Observation year")
    value: float = Field(..., description="Numerical value")
    unit: str
    frequency: str = "Annual"
    dataset_code: str

    @field_validator("country_code")
    @classmethod
    def clean_country_code(cls, v: str) -> str:
        return v.strip().upper()

class IngestionLogSchema(BaseModel):
    provider: str
    dataset_code: str
    status: str
    records_ingested: int
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
