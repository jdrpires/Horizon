"""Protocol metadata and message header contracts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime

from horizon_protocol.identifiers import CausationId, CorrelationId, ModuleId, TenantId, UserId
from horizon_protocol.naming import NamingConvention
from horizon_protocol.shared import MessageKind
from horizon_protocol.versioning import ProtocolVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class ProtocolMetadata:
    """Metadata attached to any protocol message."""

    tenant_id: TenantId | None = None
    user_id: UserId | None = None
    module_id: ModuleId | None = None
    attributes: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze metadata attributes as a plain dictionary copy."""
        object.__setattr__(self, "attributes", dict(self.attributes))


@dataclass(frozen=True, slots=True)
class MessageHeader:
    """Official header for Horizon Protocol messages."""

    message_name: str
    message_kind: MessageKind
    protocol_version: ProtocolVersion
    schema_version: SchemaVersion
    correlation_id: CorrelationId
    causation_id: CausationId | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: ProtocolMetadata = field(default_factory=ProtocolMetadata)

    def __post_init__(self) -> None:
        """Validate message header naming and time shape."""
        NamingConvention.ensure_message(self.message_kind, self.message_name)
        if self.occurred_at.tzinfo is None:
            raise ValueError("Message header timestamp must be timezone-aware.")
