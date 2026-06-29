"""Observation aggregate root."""

from __future__ import annotations

from datetime import datetime

from horizon_domain.asset import AssetId
from horizon_domain.observation.commands import RegisterObservation
from horizon_domain.observation.events import ObservationRegistered
from horizon_domain.observation.validators import ensure_asset_id
from horizon_domain.observation.value_objects import (
    ObservationId,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
)
from horizon_kernel import AggregateRoot, Clock, SystemClock


class Observation(AggregateRoot):
    """Aggregate representing one factual observation over an Asset."""

    __slots__ = ("_asset_id", "_quality", "_source", "_timestamp", "_type", "_unit", "_value")

    def __init__(
        self,
        *,
        observation_id: ObservationId,
        asset_id: AssetId,
        observation_type: ObservationType,
        value: ObservationValue,
        unit: ObservationUnit,
        source: ObservationSource,
        timestamp: ObservationTimestamp,
        quality: ObservationQuality,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        version: int = 1,
        clock: Clock | None = None,
    ) -> None:
        """Create an Observation aggregate."""
        super().__init__(
            id=observation_id.value,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            clock=clock,
        )
        self._asset_id = ensure_asset_id(asset_id)
        self._type = observation_type
        self._value = value
        self._unit = unit
        self._source = source
        self._timestamp = timestamp
        self._quality = quality

    @classmethod
    def register(cls, command: RegisterObservation, clock: Clock | None = None) -> Observation:
        """Register an Observation and record its domain event."""
        resolved_clock = SystemClock() if clock is None else clock
        command.timestamp.ensure_not_future(resolved_clock.now())
        observation = cls(
            observation_id=command.observation_id,
            asset_id=command.asset_id,
            observation_type=command.observation_type,
            value=command.value,
            unit=command.unit,
            source=command.source,
            timestamp=command.timestamp,
            quality=command.quality,
            clock=resolved_clock,
        )
        observation.record_event(
            ObservationRegistered.create(
                observation_id=observation.observation_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                occurred_at=resolved_clock.now(),
                version=observation.version,
                payload=observation.to_dict(),
            )
        )
        return observation

    @property
    def observation_id(self) -> ObservationId:
        """Return the Observation ID."""
        return ObservationId(self.id)

    @property
    def asset_id(self) -> AssetId:
        """Return referenced Asset ID."""
        return self._asset_id

    @property
    def observation_type(self) -> ObservationType:
        """Return Observation type."""
        return self._type

    @property
    def value(self) -> ObservationValue:
        """Return Observation value."""
        return self._value

    @property
    def unit(self) -> ObservationUnit:
        """Return Observation unit."""
        return self._unit

    @property
    def source(self) -> ObservationSource:
        """Return Observation source."""
        return self._source

    @property
    def timestamp(self) -> ObservationTimestamp:
        """Return Observation timestamp."""
        return self._timestamp

    @property
    def quality(self) -> ObservationQuality:
        """Return Observation quality."""
        return self._quality

    def to_dict(self) -> dict[str, object]:
        """Serialize this Observation to primitive values."""
        return {
            "observation_id": self.observation_id.to_string(),
            "asset_id": self.asset_id.to_string(),
            "type": self.observation_type.value,
            "value": self.value.value,
            "unit": self.unit.value,
            "source": self.source.value,
            "timestamp": self.timestamp.value.isoformat(),
            "quality": self.quality.value,
            "version": self.version,
        }
