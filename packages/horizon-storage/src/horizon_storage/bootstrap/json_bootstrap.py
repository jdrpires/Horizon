"""JSON storage bootstrap."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from horizon_storage.json import JsonStorageAdapter
from horizon_storage.repositories import JsonAssetRepository, JsonObservationRepository
from horizon_storage.serializers import AssetSerializer, ObservationSerializer


@dataclass(frozen=True, slots=True)
class StorageBootstrapResult:
    """Facts loaded from storage and ready for application composition."""

    asset_repository: JsonAssetRepository
    observation_repository: JsonObservationRepository
    assets_loaded: int
    observations_loaded: int
    storage_kind: str
    storage_path: Path


class JsonStorageBootstrap:
    """Prepare JSON storage and load persisted Horizon facts."""

    def __init__(self, root: Path | str) -> None:
        """Create the bootstrap service."""
        self._adapter = JsonStorageAdapter(root)

    def bootstrap(self) -> StorageBootstrapResult:
        """Ensure JSON storage exists and load repositories."""
        self._adapter.ensure_storage()
        asset_repository = JsonAssetRepository(self._adapter, AssetSerializer())
        observation_repository = JsonObservationRepository(self._adapter, ObservationSerializer())
        return StorageBootstrapResult(
            asset_repository=asset_repository,
            observation_repository=observation_repository,
            assets_loaded=len(asset_repository.list()),
            observations_loaded=len(observation_repository.list()),
            storage_kind="JSON",
            storage_path=self._adapter.root,
        )
