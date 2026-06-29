"""Validation functions for Horizon Protocol values."""

from __future__ import annotations

from uuid import UUID

from horizon_protocol.naming import NamingConvention
from horizon_protocol.shared import MessageKind, ProtocolValidationError
from horizon_protocol.versioning import ProtocolVersion, SchemaVersion


def validate_protocol_version(value: ProtocolVersion | str) -> ProtocolVersion:
    """Validate and return a protocol version."""
    return value if isinstance(value, ProtocolVersion) else ProtocolVersion.parse(value)


def validate_schema_version(value: SchemaVersion | str) -> SchemaVersion:
    """Validate and return a schema version."""
    return value if isinstance(value, SchemaVersion) else SchemaVersion.parse(value)


def validate_message_name(kind: MessageKind, value: str) -> str:
    """Validate a protocol message name."""
    return NamingConvention.ensure_message(kind, value)


def validate_identifier_name(value: str) -> str:
    """Validate an identifier type name."""
    return NamingConvention.ensure_identifier_name(value)


def validate_category_name(value: str) -> str:
    """Validate a registry category name."""
    return NamingConvention.ensure_category(value)


def validate_identifier_format(value: str) -> str:
    """Validate the canonical UUID identifier value."""
    try:
        UUID(value)
    except ValueError as exc:
        raise ProtocolValidationError("Identifiers must use canonical UUID format.") from exc
    return value
