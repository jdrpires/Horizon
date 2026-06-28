"""Structured errors for explicit domain outcomes."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class Error:
    """Base immutable error value."""

    code: str
    message: str
    details: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze error details."""
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))

    def to_dict(self) -> dict[str, object]:
        """Serialize the error to primitive values."""
        return {"code": self.code, "message": self.message, "details": dict(self.details)}


@dataclass(frozen=True, slots=True)
class ValidationError(Error):
    """Error raised by invalid input or invalid value object state."""


@dataclass(frozen=True, slots=True)
class BusinessError(Error):
    """Error raised when an application or domain operation cannot proceed."""


@dataclass(frozen=True, slots=True)
class InfrastructureError(Error):
    """Error representing an external system or infrastructure failure."""


@dataclass(frozen=True, slots=True)
class UnexpectedError(Error):
    """Error representing an unexpected condition."""


@dataclass(frozen=True, slots=True)
class DomainRuleViolation(BusinessError):
    """Error raised when a domain invariant would be violated."""
