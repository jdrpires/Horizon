"""Official Horizon Protocol contracts."""

from horizon_protocol.contracts.messages import Command, DomainEventReference, Message, Query
from horizon_protocol.contracts.metadata import MessageHeader, ProtocolMetadata
from horizon_protocol.contracts.references import (
    AggregateReference,
    CorrelationReference,
    EntityReference,
    EnvelopeReference,
)

__all__ = [
    "AggregateReference",
    "Command",
    "CorrelationReference",
    "DomainEventReference",
    "EntityReference",
    "EnvelopeReference",
    "Message",
    "MessageHeader",
    "ProtocolMetadata",
    "Query",
]
