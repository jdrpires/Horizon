"""Immutable envelope used to move events through the platform."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from horizon_events.metadata import EventMetadata
from horizon_events.shared import EventName, EventVersion, SchemaVersion


def _string_mapping(value: object) -> dict[str, str]:
    """Convert a primitive mapping object to a string mapping."""
    if not isinstance(value, Mapping):
        return {}
    return {str(key): str(item) for key, item in value.items()}


def _required_int(data: Mapping[str, object], key: str) -> int:
    """Read an integer-like value from primitive data."""
    value = data[key]
    if not isinstance(value, int | str):
        raise ValueError(f"{key} must be an integer.")
    return int(value)


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Immutable transport envelope for one platform event."""

    event_name: EventName
    event: Mapping[str, object]
    metadata: EventMetadata
    headers: Mapping[str, str] = field(default_factory=dict)
    trace: Mapping[str, str] = field(default_factory=dict)
    correlation: Mapping[str, str] = field(default_factory=dict)
    causation: Mapping[str, str] = field(default_factory=dict)
    tenant: str | None = None
    version: EventVersion = field(default_factory=lambda: EventVersion(1))
    schema_version: SchemaVersion = field(default_factory=lambda: SchemaVersion(1))

    def __post_init__(self) -> None:
        """Freeze mutable mappings carried by the envelope."""
        object.__setattr__(self, "event", MappingProxyType(dict(self.event)))
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))
        object.__setattr__(self, "trace", MappingProxyType(dict(self.trace)))
        object.__setattr__(self, "correlation", MappingProxyType(dict(self.correlation)))
        object.__setattr__(self, "causation", MappingProxyType(dict(self.causation)))

    @classmethod
    def create(
        cls,
        *,
        event_name: str,
        event: Mapping[str, object],
        metadata: EventMetadata,
        headers: Mapping[str, str] | None = None,
        tenant: str | None = None,
        version: int = 1,
        schema_version: int = 1,
    ) -> EventEnvelope:
        """Create an envelope and derive trace, correlation, and causation fields."""
        return cls(
            event_name=EventName(event_name),
            event=event,
            metadata=metadata,
            headers={} if headers is None else headers,
            trace={"trace_id": metadata.trace_id, "span_id": metadata.span_id},
            correlation={"correlation_id": metadata.correlation_id},
            causation={"causation_id": metadata.causation_id},
            tenant=tenant,
            version=EventVersion(version),
            schema_version=SchemaVersion(schema_version),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this envelope to primitive values."""
        return {
            "event_name": self.event_name.value,
            "event": dict(self.event),
            "metadata": self.metadata.to_dict(),
            "headers": dict(self.headers),
            "trace": dict(self.trace),
            "correlation": dict(self.correlation),
            "causation": dict(self.causation),
            "tenant": self.tenant,
            "version": self.version.value,
            "schema_version": self.schema_version.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> EventEnvelope:
        """Deserialize an envelope from primitive values."""
        event = data.get("event")
        metadata = data.get("metadata")
        if not isinstance(event, Mapping) or not isinstance(metadata, Mapping):
            raise ValueError("event and metadata are required mappings.")
        return cls(
            event_name=EventName(str(data["event_name"])),
            event=dict(event),
            metadata=EventMetadata.from_dict(metadata),
            headers=_string_mapping(data.get("headers", {})),
            trace=_string_mapping(data.get("trace", {})),
            correlation=_string_mapping(data.get("correlation", {})),
            causation=_string_mapping(data.get("causation", {})),
            tenant=None if data.get("tenant") is None else str(data["tenant"]),
            version=EventVersion(_required_int(data, "version")),
            schema_version=SchemaVersion(_required_int(data, "schema_version")),
        )
