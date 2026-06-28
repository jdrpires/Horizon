"""Immutable metadata carried by every event envelope."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from uuid import uuid4

from horizon_events.context import current_context
from horizon_events.shared import EventId


def _new_token() -> str:
    """Create an opaque correlation token."""
    return str(uuid4())


def _string_mapping(value: object) -> dict[str, str]:
    """Convert a primitive mapping object to a string mapping."""
    if not isinstance(value, Mapping):
        return {}
    return {str(key): str(item) for key, item in value.items()}


@dataclass(frozen=True, slots=True)
class EventMetadata:
    """Immutable metadata describing event identity, origin, and trace context."""

    event_id: EventId
    aggregate_id: str
    correlation_id: str
    causation_id: str
    occurred_at: datetime
    created_at: datetime
    producer: str
    source: str
    trace_id: str
    span_id: str
    request_id: str
    environment: str
    user_id: str | None = None
    tags: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metadata and freeze tags."""
        if not self.aggregate_id:
            raise ValueError("aggregate_id cannot be empty.")
        if not self.producer:
            raise ValueError("producer cannot be empty.")
        if not self.source:
            raise ValueError("source cannot be empty.")
        if self.occurred_at.tzinfo is None or self.created_at.tzinfo is None:
            raise ValueError("metadata timestamps must be timezone-aware.")
        object.__setattr__(self, "tags", MappingProxyType(dict(self.tags)))

    @classmethod
    def create(
        cls,
        *,
        aggregate_id: str,
        producer: str,
        source: str,
        environment: str,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        request_id: str | None = None,
        occurred_at: datetime | None = None,
        created_at: datetime | None = None,
        user_id: str | None = None,
        tags: Mapping[str, str] | None = None,
    ) -> EventMetadata:
        """Create metadata with generated identifiers where absent."""
        now = datetime.now(UTC)
        resolved_correlation_id = correlation_id or _new_token()
        return cls(
            event_id=EventId.new(),
            aggregate_id=aggregate_id,
            correlation_id=resolved_correlation_id,
            causation_id=causation_id or resolved_correlation_id,
            occurred_at=occurred_at or now,
            created_at=created_at or now,
            producer=producer,
            source=source,
            user_id=user_id,
            trace_id=trace_id or _new_token(),
            span_id=span_id or _new_token(),
            request_id=request_id or _new_token(),
            environment=environment,
            tags={} if tags is None else tags,
        )

    @classmethod
    def from_current_context(
        cls,
        *,
        aggregate_id: str,
        producer: str,
        source: str,
        environment: str,
        occurred_at: datetime | None = None,
        created_at: datetime | None = None,
        user_id: str | None = None,
        tags: Mapping[str, str] | None = None,
    ) -> EventMetadata:
        """Create metadata using the active correlation context."""
        context = current_context()
        return cls.create(
            aggregate_id=aggregate_id,
            producer=producer,
            source=source,
            environment=environment,
            correlation_id=context.correlation_id,
            causation_id=context.causation_id,
            trace_id=context.trace_id,
            request_id=context.request_id,
            occurred_at=occurred_at,
            created_at=created_at,
            user_id=user_id,
            tags=tags,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize metadata to primitive values."""
        return {
            "event_id": self.event_id.to_string(),
            "aggregate_id": self.aggregate_id,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "occurred_at": self.occurred_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "producer": self.producer,
            "source": self.source,
            "user_id": self.user_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "request_id": self.request_id,
            "environment": self.environment,
            "tags": dict(self.tags),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> EventMetadata:
        """Deserialize metadata from primitive values."""
        return cls(
            event_id=EventId.from_string(str(data["event_id"])),
            aggregate_id=str(data["aggregate_id"]),
            correlation_id=str(data["correlation_id"]),
            causation_id=str(data["causation_id"]),
            occurred_at=datetime.fromisoformat(str(data["occurred_at"])),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            producer=str(data["producer"]),
            source=str(data["source"]),
            user_id=None if data.get("user_id") is None else str(data["user_id"]),
            trace_id=str(data["trace_id"]),
            span_id=str(data["span_id"]),
            request_id=str(data["request_id"]),
            environment=str(data["environment"]),
            tags=_string_mapping(data.get("tags", {})),
        )
