"""References shared across protocol messages."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_protocol.identifiers import CorrelationId, EventId, ProtocolIdentifier
from horizon_protocol.versioning import SchemaVersion


@dataclass(frozen=True, slots=True)
class CorrelationReference:
    """Reference that carries correlation and optional causation identity."""

    correlation_id: CorrelationId
    causation_id: ProtocolIdentifier | None = None


@dataclass(frozen=True, slots=True)
class AggregateReference:
    """Reference to an aggregate without importing its domain model."""

    aggregate_type: str
    aggregate_id: ProtocolIdentifier


@dataclass(frozen=True, slots=True)
class EntityReference:
    """Reference to an entity without importing its domain model."""

    entity_type: str
    entity_id: ProtocolIdentifier


@dataclass(frozen=True, slots=True)
class EnvelopeReference:
    """Reference to a message envelope."""

    envelope_id: EventId
    message_name: str
    schema_version: SchemaVersion
