"""In-memory application adapters."""

from __future__ import annotations

from horizon_domain import Asset, AssetId, Observation
from horizon_domain.observation import ObservationId


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


class InMemoryObservationRepository:
    """In-memory Observation repository for playground and tests."""

    def __init__(self) -> None:
        """Create an empty repository."""
        self._items: dict[str, Observation] = {}

    def save(self, observation: Observation) -> None:
        """Save an Observation aggregate."""
        self._items[observation.observation_id.to_string()] = observation

    def get(self, observation_id: ObservationId) -> Observation | None:
        """Return an Observation by ID."""
        return self._items.get(observation_id.to_string())

    def list(self) -> tuple[Observation, ...]:
        """Return all Observations in insertion order."""
        return tuple(self._items.values())
