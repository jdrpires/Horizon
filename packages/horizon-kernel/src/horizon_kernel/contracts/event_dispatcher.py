"""Event dispatcher interface."""

from __future__ import annotations

from typing import Protocol

from horizon_kernel.events import DomainEvent


class EventDispatcher(Protocol):
    """Synchronous dispatcher for domain events inside a process."""

    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch a single domain event."""

    def dispatch_all(self, events: tuple[DomainEvent, ...]) -> None:
        """Dispatch multiple domain events."""
