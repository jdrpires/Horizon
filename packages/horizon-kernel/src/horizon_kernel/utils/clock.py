"""Clock abstractions for time-aware domain behavior."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime


class Clock(ABC):
    """Abstract clock used to avoid direct system time access."""

    @abstractmethod
    def now(self) -> datetime:
        """Return the current timezone-aware instant."""


@dataclass(frozen=True, slots=True)
class SystemClock(Clock):
    """Clock backed by the system UTC time."""

    def now(self) -> datetime:
        """Return the current UTC instant."""
        return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class FrozenClock(Clock):
    """Clock returning a fixed instant for deterministic tests."""

    instant: datetime

    def __post_init__(self) -> None:
        """Ensure the frozen instant is timezone-aware."""
        if self.instant.tzinfo is None:
            raise ValueError("FrozenClock requires a timezone-aware datetime.")

    def now(self) -> datetime:
        """Return the configured fixed instant."""
        return self.instant
