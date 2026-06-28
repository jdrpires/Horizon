"""Event publisher interface."""

from __future__ import annotations

from typing import Protocol

from horizon_kernel.events import DomainEvent


class EventPublisher(Protocol):
    """Publisher boundary for domain events."""

    def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event."""

    def publish_all(self, events: tuple[DomainEvent, ...]) -> None:
        """Publish multiple domain events."""
