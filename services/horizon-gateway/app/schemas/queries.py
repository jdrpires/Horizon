"""HTTP schemas for Horizon query endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class AssetSummary(BaseModel):
    """Asset summary exposed to Horizon clients."""

    asset_id: str
    name: str
    external_reference: str | None
    category: str
    status: str


class AssetListResponse(BaseModel):
    """List of Assets visible to the Gateway."""

    assets: tuple[AssetSummary, ...]


class CurrentStateValueResponse(BaseModel):
    """One Current State value."""

    type: str
    value: float
    unit: str
    source: str
    timestamp: str
    observation_id: str
    sequence: int


class CurrentStateResponse(BaseModel):
    """Current State response for one Asset."""

    asset_id: str
    last_updated_at: str | None
    observation_count: int
    values: tuple[CurrentStateValueResponse, ...]


class TimelineEntryResponse(BaseModel):
    """One Timeline entry."""

    asset_id: str
    observation_id: str
    type: str
    value: float
    unit: str
    source: str
    timestamp: str
    quality: str
    sequence: int


class TimelineResponse(BaseModel):
    """Timeline response for one Asset."""

    asset_id: str
    entries: tuple[TimelineEntryResponse, ...]

