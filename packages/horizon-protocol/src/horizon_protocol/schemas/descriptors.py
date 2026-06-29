"""Schema descriptors for protocol messages."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from horizon_protocol.naming import NamingConvention
from horizon_protocol.versioning import SchemaVersion


@dataclass(frozen=True, slots=True)
class SchemaDescriptor:
    """Registered schema descriptor."""

    name: str
    version: SchemaVersion
    fields: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate schema descriptor fields."""
        NamingConvention.ensure_pascal_case(self.name)
        object.__setattr__(self, "fields", dict(self.fields))
