"""Query descriptors for the Horizon Protocol registry."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_protocol.naming import NamingConvention
from horizon_protocol.shared import MessageKind
from horizon_protocol.versioning import ProtocolVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class QueryDescriptor:
    """Registered query contract descriptor."""

    name: str
    protocol_version: ProtocolVersion
    schema_version: SchemaVersion
    category: str

    def __post_init__(self) -> None:
        """Validate query descriptor fields."""
        NamingConvention.ensure_query(self.name)
        NamingConvention.ensure_category(self.category)

    @property
    def kind(self) -> MessageKind:
        """Return query message kind."""
        return MessageKind.QUERY
