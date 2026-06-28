"""Event and schema versioning primitives."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class VersionCompatibility(StrEnum):
    """Compatibility relationship between two versions."""

    SAME = "same"
    BACKWARD_COMPATIBLE = "backward_compatible"
    FORWARD_ONLY = "forward_only"
    INCOMPATIBLE = "incompatible"


@dataclass(frozen=True, order=True, slots=True)
class EventVersion:
    """Positive integer event version."""

    value: int

    def __post_init__(self) -> None:
        """Validate event version."""
        if self.value < 1:
            raise ValueError("Event version must be greater than zero.")

    def is_compatible_with(self, other: EventVersion) -> VersionCompatibility:
        """Return the compatibility relationship with another event version."""
        if self.value == other.value:
            return VersionCompatibility.SAME
        if self.value > other.value:
            return VersionCompatibility.BACKWARD_COMPATIBLE
        return VersionCompatibility.FORWARD_ONLY


@dataclass(frozen=True, order=True, slots=True)
class SchemaVersion:
    """Positive integer schema version."""

    value: int

    def __post_init__(self) -> None:
        """Validate schema version."""
        if self.value < 1:
            raise ValueError("Schema version must be greater than zero.")

    def is_compatible_with(self, other: SchemaVersion) -> VersionCompatibility:
        """Return the compatibility relationship with another schema version."""
        if self.value == other.value:
            return VersionCompatibility.SAME
        if self.value > other.value:
            return VersionCompatibility.BACKWARD_COMPATIBLE
        return VersionCompatibility.FORWARD_ONLY
