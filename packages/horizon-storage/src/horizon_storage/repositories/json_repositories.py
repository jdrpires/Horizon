"""JSON-backed repositories for persisted Horizon facts."""

from __future__ import annotations

from horizon_domain import Asset, AssetId, Observation
from horizon_domain.observation import ObservationId
from horizon_storage.exceptions import StorageCorruptionError
from horizon_storage.json.adapter import ASSETS_FILE, OBSERVATIONS_FILE, JsonStorageAdapter
from horizon_storage.serializers import AssetSerializer, ObservationSerializer


class JsonAssetRepository:
    """JSON-backed Asset repository."""

    def __init__(self, adapter: JsonStorageAdapter, serializer: AssetSerializer) -> None:
        """Create the repository."""
        self._adapter = adapter
        self._serializer = serializer
        self._items = _load_assets(adapter, serializer)

    def save(self, asset: Asset) -> None:
        """Save an Asset and persist the facts file."""
        self._items[asset.asset_id.to_string()] = asset
        self._persist()

    def get(self, asset_id: AssetId) -> Asset | None:
        """Return an Asset by ID."""
        return self._items.get(asset_id.to_string())

    def list(self) -> tuple[Asset, ...]:
        """Return all Assets in persisted order."""
        return tuple(self._items.values())

    def _persist(self) -> None:
        """Persist all Asset facts."""
        self._adapter.write_json(
            ASSETS_FILE,
            [self._serializer.serialize(asset) for asset in self._items.values()],
        )


class JsonObservationRepository:
    """JSON-backed Observation repository."""

    def __init__(self, adapter: JsonStorageAdapter, serializer: ObservationSerializer) -> None:
        """Create the repository."""
        self._adapter = adapter
        self._serializer = serializer
        self._items = _load_observations(adapter, serializer)

    def save(self, observation: Observation) -> None:
        """Save an Observation and persist the facts file."""
        self._items[observation.observation_id.to_string()] = observation
        self._persist()

    def get(self, observation_id: ObservationId) -> Observation | None:
        """Return an Observation by ID."""
        return self._items.get(observation_id.to_string())

    def list(self) -> tuple[Observation, ...]:
        """Return all Observations in persisted order."""
        return tuple(self._items.values())

    def _persist(self) -> None:
        """Persist all Observation facts."""
        self._adapter.write_json(
            OBSERVATIONS_FILE,
            [
                self._serializer.serialize(observation)
                for observation in self._items.values()
            ],
        )


def _load_assets(
    adapter: JsonStorageAdapter,
    serializer: AssetSerializer,
) -> dict[str, Asset]:
    """Load Asset facts from JSON."""
    payload = adapter.read_json(ASSETS_FILE)
    if not isinstance(payload, list):
        raise StorageCorruptionError("assets.json must contain a list.")
    items: dict[str, Asset] = {}
    for item in payload:
        if not isinstance(item, dict):
            raise StorageCorruptionError("assets.json entries must be objects.")
        asset = serializer.deserialize(item)
        items[asset.asset_id.to_string()] = asset
    return items


def _load_observations(
    adapter: JsonStorageAdapter,
    serializer: ObservationSerializer,
) -> dict[str, Observation]:
    """Load Observation facts from JSON."""
    payload = adapter.read_json(OBSERVATIONS_FILE)
    if not isinstance(payload, list):
        raise StorageCorruptionError("observations.json must contain a list.")
    items: dict[str, Observation] = {}
    for item in payload:
        if not isinstance(item, dict):
            raise StorageCorruptionError("observations.json entries must be objects.")
        observation = serializer.deserialize(item)
        items[observation.observation_id.to_string()] = observation
    return items
