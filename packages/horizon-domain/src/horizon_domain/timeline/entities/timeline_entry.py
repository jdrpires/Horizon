"""Timeline entry entity."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_domain.asset import AssetId
from horizon_domain.observation import (
    Observation,
    ObservationId,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
)


@dataclass(frozen=True, slots=True)
class TimelineEntry:
    """Immutable Observation-derived Timeline entry."""

    asset_id: AssetId
    observation_id: ObservationId
    observation_type: ObservationType
    value: ObservationValue
    unit: ObservationUnit
    source: ObservationSource
    timestamp: ObservationTimestamp
    quality: ObservationQuality
    sequence: int

    @classmethod
    def from_observation(cls, observation: Observation, sequence: int) -> TimelineEntry:
        """Create a Timeline entry from an Observation aggregate."""
        if sequence < 1:
            raise ValueError("Timeline entry sequence must be greater than zero.")
        return cls(
            asset_id=observation.asset_id,
            observation_id=observation.observation_id,
            observation_type=observation.observation_type,
            value=observation.value,
            unit=observation.unit,
            source=observation.source,
            timestamp=observation.timestamp,
            quality=observation.quality,
            sequence=sequence,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this Timeline entry."""
        return {
            "asset_id": self.asset_id.to_string(),
            "observation_id": self.observation_id.to_string(),
            "type": self.observation_type.value,
            "value": self.value.value,
            "unit": self.unit.value,
            "source": self.source.value,
            "timestamp": self.timestamp.value.isoformat(),
            "quality": self.quality.value,
            "sequence": self.sequence,
        }
