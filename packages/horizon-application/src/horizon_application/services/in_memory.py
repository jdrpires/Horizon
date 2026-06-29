"""In-memory application adapters."""

from __future__ import annotations

from horizon_domain import Asset, AssetId


class InMemoryAssetRepository:
    """In-memory Asset repository for playground and tests."""

    def __init__(self) -> None:
        """Create an empty repository."""
        self._items: dict[str, Asset] = {}

    def save(self, asset: Asset) -> None:
        """Save an Asset aggregate."""
        self._items[asset.asset_id.to_string()] = asset

    def get(self, asset_id: AssetId) -> Asset | None:
        """Return an Asset by ID."""
        return self._items.get(asset_id.to_string())

    def list(self) -> tuple[Asset, ...]:
        """Return all Assets in insertion order."""
        return tuple(self._items.values())


class InMemoryUnitOfWork:
    """No-op Unit of Work for in-memory execution."""

    committed: bool
    rolled_back: bool

    def __init__(self) -> None:
        """Create a unit of work state tracker."""
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        """Mark work as committed."""
        self.committed = True

    def rollback(self) -> None:
        """Mark work as rolled back."""
        self.rolled_back = True
