"""Collector data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4

from horizon_catalog import ObservationDefinition


class CollectorSessionState(StrEnum):
    """Lifecycle state for one collector session."""

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class RawObservation:
    """Raw external observation before Horizon catalog mapping."""

    key: str
    value: object
    observed_at: datetime | None = None
    source: str = "collector"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate raw observation shape."""
        if not self.key.strip():
            raise ValueError("raw observation key cannot be blank.")
        if not self.source.strip():
            raise ValueError("raw observation source cannot be blank.")
        if self.observed_at is not None and self.observed_at.tzinfo is None:
            raise ValueError("raw observation timestamp must be timezone-aware.")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class CanonicalObservation:
    """Catalog-backed Observation ready to be published into Horizon."""

    definition: ObservationDefinition
    value: object
    observed_at: datetime
    source: str
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate canonical observation shape."""
        if not self.source.strip():
            raise ValueError("canonical observation source cannot be blank.")
        if self.observed_at.tzinfo is None:
            raise ValueError("canonical observation timestamp must be timezone-aware.")
        if not self.correlation_id.strip():
            raise ValueError("correlation_id cannot be blank.")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @property
    def observation_type(self) -> str:
        """Return the runtime Observation type for the definition."""
        return self.definition.runtime_observation_type

    @property
    def unit(self) -> str:
        """Return the unit declared by the catalog definition."""
        return self.definition.unit


def utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(UTC)
