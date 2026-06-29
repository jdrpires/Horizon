"""Structural contracts for protocol messages."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from horizon_protocol.shared import MessageKind


class Message(Protocol):
    """Base structural contract for all protocol messages."""

    @property
    def name(self) -> str:
        """Return the official message name."""
        ...

    @property
    def kind(self) -> MessageKind:
        """Return the message kind."""
        ...

    def payload(self) -> Mapping[str, object]:
        """Return immutable message payload data."""
        ...


class Command(Message, Protocol):
    """Contract for command messages."""


class Query(Message, Protocol):
    """Contract for query messages."""


class DomainEventReference(Message, Protocol):
    """Contract for references to domain events without defining concrete events."""
