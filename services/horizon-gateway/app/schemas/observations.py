"""HTTP schemas for live Observation ingestion."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ObservationItem(BaseModel):
    """One Observation entry received from a collector payload."""

    definition_id: str = Field(min_length=1)
    value: Any
    unit: str = Field(min_length=1)
    timestamp: datetime
    quality: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")

    @field_validator("definition_id", "unit", "quality")
    @classmethod
    def _strip_required_text(cls, value: str) -> str:
        clean = value.strip()
        if not clean:
            raise ValueError("field cannot be blank")
        return clean

    @field_validator("timestamp")
    @classmethod
    def _require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        return value


class ObservationIngestionRequest(BaseModel):
    """Collector payload accepted by the Live Ingestion Gateway."""

    source: str = Field(min_length=1)
    asset_id: str = Field(min_length=1)
    observations: list[ObservationItem] = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")

    @field_validator("source", "asset_id")
    @classmethod
    def _strip_required_text(cls, value: str) -> str:
        clean = value.strip()
        if not clean:
            raise ValueError("field cannot be blank")
        return clean


class IngestedObservation(BaseModel):
    """One successfully ingested Observation."""

    definition_id: str
    observation_id: str
    observation_type: str
    value: float
    unit: str
    timestamp: str


class ObservationIngestionResponse(BaseModel):
    """Gateway ingestion result."""

    status: str
    source: str
    asset_id: str
    accepted: int
    observations: tuple[IngestedObservation, ...]
    event_count: int
    timeline_entries: int
    current_state_values: int

