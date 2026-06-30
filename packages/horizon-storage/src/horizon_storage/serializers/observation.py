"""Observation JSON serializer."""

from __future__ import annotations

from datetime import datetime

from horizon_domain import AssetId, Observation
from horizon_domain.observation import (
    ObservationId,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
)


class ObservationSerializer:
    """Serialize and deserialize Observation facts."""

    def serialize(self, value: Observation) -> dict[str, object]:
        """Serialize an Observation aggregate."""
        return {
            "observation_id": value.observation_id.to_string(),
            "asset_id": value.asset_id.to_string(),
            "type": value.observation_type.value,
            "value": value.value.value,
            "unit": value.unit.value,
            "source": value.source.value,
            "timestamp": value.timestamp.value.isoformat(),
            "quality": value.quality.value,
            "version": value.version,
            "created_at": value.created_at.isoformat(),
            "updated_at": value.updated_at.isoformat(),
        }

    def deserialize(self, payload: dict[str, object]) -> Observation:
        """Deserialize an Observation aggregate without producing domain events."""
        return Observation(
            observation_id=ObservationId.from_string(str(payload["observation_id"])),
            asset_id=AssetId.from_string(str(payload["asset_id"])),
            observation_type=ObservationType(str(payload["type"])),
            value=ObservationValue(float(payload["value"])),
            unit=ObservationUnit(str(payload["unit"])),
            source=ObservationSource(str(payload["source"])),
            timestamp=ObservationTimestamp(datetime.fromisoformat(str(payload["timestamp"]))),
            quality=ObservationQuality(str(payload["quality"])),
            created_at=datetime.fromisoformat(str(payload["created_at"])),
            updated_at=datetime.fromisoformat(str(payload["updated_at"])),
            version=int(payload["version"]),
        )
