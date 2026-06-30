"""Observation catalog definition model."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ValueType(StrEnum):
    """Supported catalog value types."""

    NUMBER = "number"
    TEXT = "text"
    BOOLEAN = "boolean"
    ENUM = "enum"
    DATETIME = "datetime"


@dataclass(frozen=True, slots=True)
class ObservationDefinition:
    """Reusable definition for one official Observation."""

    id: str
    label: str
    category: str
    unit: str
    value_type: ValueType
    default_source: str
    description: str
    aliases: tuple[str, ...] = ()
    enabled: bool = True
    display_order: int = 0
    enum_values: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate definition shape."""
        _ensure_text(self.id, "id")
        _ensure_text(self.label, "label")
        _ensure_text(self.category, "category")
        _ensure_text(self.unit, "unit")
        _ensure_text(self.default_source, "default_source")
        _ensure_text(self.description, "description")
        if self.value_type is ValueType.ENUM and not self.enum_values:
            raise ValueError("enum definitions must provide enum_values.")
        if self.value_type is not ValueType.ENUM and self.enum_values:
            raise ValueError("enum_values are only allowed for enum definitions.")

    @property
    def runtime_observation_type(self) -> str:
        """Return the current runtime-compatible Observation type."""
        return self.aliases[0] if self.aliases else self.id

    def matches_alias(self, value: str) -> bool:
        """Return whether this definition matches an alias."""
        clean = value.strip().lower()
        return clean == self.id.lower() or clean in {alias.lower() for alias in self.aliases}


def _ensure_text(value: str, field: str) -> None:
    """Validate required text."""
    if not value.strip():
        raise ValueError(f"{field} cannot be blank.")
