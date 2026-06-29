"""Immutable semantic versions used by the Horizon Protocol."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from horizon_protocol.shared import ProtocolValidationError
from horizon_protocol.versioning.compatibility import Compatibility


@dataclass(frozen=True, order=True, slots=True)
class SemanticVersion:
    """Immutable major.minor.patch version."""

    major: int
    minor: int
    patch: int = 0

    def __post_init__(self) -> None:
        """Validate semantic version components."""
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise ProtocolValidationError("Version components must be non-negative.")
        if self.major == 0:
            raise ProtocolValidationError("Major version must be greater than zero.")

    @classmethod
    def parse(cls, value: str) -> Self:
        """Parse a semantic version string."""
        parts = value.split(".")
        if len(parts) not in {2, 3}:
            raise ProtocolValidationError("Version must use major.minor or major.minor.patch.")
        try:
            numbers = tuple(int(part) for part in parts)
        except ValueError as exc:
            raise ProtocolValidationError("Version components must be integers.") from exc
        if len(numbers) == 2:
            return cls(numbers[0], numbers[1], 0)
        return cls(numbers[0], numbers[1], numbers[2])

    def compatibility_with(self, supported: SemanticVersion) -> Compatibility:
        """Return compatibility when this version is compared with a supported version."""
        if self == supported:
            return Compatibility.SAME
        if self.major != supported.major:
            return Compatibility.INCOMPATIBLE
        if self > supported:
            return Compatibility.BACKWARD_COMPATIBLE
        return Compatibility.FUTURE_COMPATIBLE

    def is_backward_compatible_with(self, supported: SemanticVersion) -> bool:
        """Return whether this version can be read by a component supporting an older version."""
        return self.compatibility_with(supported) in {
            Compatibility.SAME,
            Compatibility.BACKWARD_COMPATIBLE,
        }

    def is_future_compatible_with(self, supported: SemanticVersion) -> bool:
        """Return whether this version is older but still within the same major line."""
        return self.compatibility_with(supported) in {
            Compatibility.SAME,
            Compatibility.FUTURE_COMPATIBLE,
        }

    def to_string(self) -> str:
        """Serialize the version."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __str__(self) -> str:
        """Return the version string."""
        return self.to_string()


class ProtocolVersion(SemanticVersion):
    """Official Horizon Protocol version."""


class SchemaVersion(SemanticVersion):
    """Schema version for protocol messages."""
