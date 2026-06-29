"""Observation application DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_application.dto.asset import EventEnvelopeDTO
from horizon_domain import Observation


@dataclass(frozen=True, slots=True)
class ObservationDTO:
    """Serializable view of an Observation aggregate."""

    observation_id: str
    asset_id: str
    observation_type: str
    value: float
    unit: str
    source: str
    timestamp: str
    quality: str
    version: int

    @classmethod
    def from_observation(cls, observation: Observation) -> ObservationDTO:
        """Map an Observation aggregate to a DTO."""
        return cls(
            observation_id=observation.observation_id.to_string(),
            asset_id=observation.asset_id.to_string(),
            observation_type=observation.observation_type.value,
            value=observation.value.value,
            unit=observation.unit.value,
            source=observation.source.value,
            timestamp=observation.timestamp.value.isoformat(),
            quality=observation.quality.value,
            version=observation.version,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the DTO."""
        return {
            "observation_id": self.observation_id,
            "asset_id": self.asset_id,
            "type": self.observation_type,
            "value": self.value,
            "unit": self.unit,
            "source": self.source,
            "timestamp": self.timestamp,
            "quality": self.quality,
            "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class RegisterObservationResultDTO:
    """Result returned by the Register Observation use case."""

    observation: ObservationDTO
    events: tuple[EventEnvelopeDTO, ...]
