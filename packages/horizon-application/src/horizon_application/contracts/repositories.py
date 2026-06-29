"""Repository interfaces."""

from __future__ import annotations

from typing import Protocol

from horizon_domain import Asset, AssetId, Observation
from horizon_domain.observation import ObservationId


class AssetRepository(Protocol):
    """Repository interface for Asset aggregates."""

    def save(self, asset: Asset) -> None:
        """Save an Asset aggregate."""

    def get(self, asset_id: AssetId) -> Asset | None:
        """Return an Asset by ID."""

    def list(self) -> tuple[Asset, ...]:
        """Return all Assets."""


class ObservationRepository(Protocol):
    """Repository interface for Observation aggregates."""

    def save(self, observation: Observation) -> None:
        """Save an Observation aggregate."""

    def get(self, observation_id: ObservationId) -> Observation | None:
        """Return an Observation by ID."""

    def list(self) -> tuple[Observation, ...]:
        """Return all Observations."""
