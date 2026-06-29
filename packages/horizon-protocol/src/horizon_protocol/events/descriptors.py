"""Domain event reference descriptors for the Horizon Protocol registry."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_protocol.naming import NamingConvention
from horizon_protocol.shared import MessageKind
from horizon_protocol.versioning import ProtocolVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class EventReferenceDescriptor:
    """Registered domain event reference descriptor."""

    name: str
    protocol_version: ProtocolVersion
    schema_version: SchemaVersion
    category: str

    def __post_init__(self) -> None:
        """Validate event reference descriptor fields."""
        NamingConvention.ensure_event(self.name)
        NamingConvention.ensure_category(self.category)

    @property
    def kind(self) -> MessageKind:
        """Return event message kind."""
        return MessageKind.EVENT
