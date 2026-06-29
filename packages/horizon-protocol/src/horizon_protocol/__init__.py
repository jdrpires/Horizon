"""Horizon Protocol public API."""

from horizon_protocol.commands import CommandDescriptor
from horizon_protocol.contracts import (
    AggregateReference,
    Command,
    CorrelationReference,
    DomainEventReference,
    EntityReference,
    EnvelopeReference,
    Message,
    MessageHeader,
    ProtocolMetadata,
    Query,
)
from horizon_protocol.events import EventReferenceDescriptor
from horizon_protocol.identifiers import (
    AssetId,
    CausationId,
    CorrelationId,
    EventId,
    InsightId,
    JourneyId,
    MaintenanceId,
    ModuleId,
    ObservationId,
    ProtocolIdentifier,
    RecommendationId,
    TenantId,
    UserId,
)
from horizon_protocol.naming import NamingConvention
from horizon_protocol.queries import QueryDescriptor
from horizon_protocol.registry import (
    CategoryRegistry,
    CommandRegistry,
    EventRegistry,
    IdentifierRegistration,
    IdentifierRegistry,
    QueryRegistry,
    SchemaRegistry,
)
from horizon_protocol.schemas import SchemaDescriptor
from horizon_protocol.shared import MessageKind, ProtocolError, ProtocolValidationError
from horizon_protocol.versioning import Compatibility, ProtocolVersion, SchemaVersion

__all__ = [
    "AggregateReference",
    "AssetId",
    "CategoryRegistry",
    "CausationId",
    "Command",
    "CommandDescriptor",
    "CommandRegistry",
    "Compatibility",
    "CorrelationId",
    "CorrelationReference",
    "DomainEventReference",
    "EntityReference",
    "EnvelopeReference",
    "EventId",
    "EventReferenceDescriptor",
    "EventRegistry",
    "IdentifierRegistration",
    "IdentifierRegistry",
    "InsightId",
    "JourneyId",
    "MaintenanceId",
    "Message",
    "MessageHeader",
    "MessageKind",
    "ModuleId",
    "NamingConvention",
    "ObservationId",
    "ProtocolError",
    "ProtocolIdentifier",
    "ProtocolMetadata",
    "ProtocolValidationError",
    "ProtocolVersion",
    "Query",
    "QueryDescriptor",
    "QueryRegistry",
    "RecommendationId",
    "SchemaDescriptor",
    "SchemaRegistry",
    "SchemaVersion",
    "TenantId",
    "UserId",
]
