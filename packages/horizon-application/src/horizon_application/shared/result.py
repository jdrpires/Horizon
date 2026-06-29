"""Application result mapping."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ApplicationResult(Generic[T]):
    """Explicit application result."""

    success: bool
    value: T | None = None
    error: str | None = None

    @classmethod
    def ok(cls, value: T) -> ApplicationResult[T]:
        """Create a successful result."""
        return cls(success=True, value=value)

    @classmethod
    def fail(cls, error: str) -> ApplicationResult[T]:
        """Create a failed result."""
        return cls(success=False, error=error)
