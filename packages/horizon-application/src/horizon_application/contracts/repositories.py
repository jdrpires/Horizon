"""Repository interfaces."""

from __future__ import annotations

from typing import Protocol

from horizon_domain import Asset, AssetId


class AssetRepository(Protocol):
    """Repository interface for Asset aggregates."""

    def save(self, asset: Asset) -> None:
        """Save an Asset aggregate."""

    def get(self, asset_id: AssetId) -> Asset | None:
        """Return an Asset by ID."""

    def list(self) -> tuple[Asset, ...]:
        """Return all Assets."""
