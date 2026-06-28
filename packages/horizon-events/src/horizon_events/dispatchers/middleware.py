"""Middleware pipeline components for event dispatch."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from horizon_events.envelopes import EventEnvelope

NextHandler = Callable[[EventEnvelope], None]


class EventMiddleware(Protocol):
    """Middleware contract for dispatch pipelines."""

    def handle(self, envelope: EventEnvelope, next_handler: NextHandler) -> None:
        """Handle an envelope and optionally call the next pipeline step."""


@dataclass(frozen=True, slots=True)
class LoggingMiddleware:
    """Middleware that emits a structured dispatch log message."""

    logger: Callable[[str], None]

    def handle(self, envelope: EventEnvelope, next_handler: NextHandler) -> None:
        """Log the event name and correlation identifier."""
        self.logger(f"{envelope.event_name.value}:{envelope.metadata.correlation_id}")
        next_handler(envelope)


@dataclass(slots=True)
class MetricsMiddleware:
    """Middleware that counts processed envelopes."""

    count: int = 0

    def handle(self, envelope: EventEnvelope, next_handler: NextHandler) -> None:
        """Increment the processed counter."""
        self.count += 1
        next_handler(envelope)


@dataclass(frozen=True, slots=True)
class ValidationMiddleware:
    """Middleware that validates envelope version fields."""

    def handle(self, envelope: EventEnvelope, next_handler: NextHandler) -> None:
        """Validate versions before dispatching."""
        if envelope.version.value < 1 or envelope.schema_version.value < 1:
            raise ValueError("Envelope versions must be positive.")
        next_handler(envelope)


@dataclass(frozen=True, slots=True)
class TracingMiddleware:
    """Middleware that validates trace fields are present."""

    def handle(self, envelope: EventEnvelope, next_handler: NextHandler) -> None:
        """Validate trace context before dispatching."""
        if not envelope.metadata.trace_id or not envelope.metadata.span_id:
            raise ValueError("Trace identifiers are required.")
        next_handler(envelope)


@dataclass(frozen=True, slots=True)
class RetryMiddleware:
    """Middleware that retries downstream dispatch on failure."""

    attempts: int = 1

    def __post_init__(self) -> None:
        """Validate retry attempts."""
        if self.attempts < 1:
            raise ValueError("Retry attempts must be greater than zero.")

    def handle(self, envelope: EventEnvelope, next_handler: NextHandler) -> None:
        """Retry the next handler up to the configured number of attempts."""
        remaining = self.attempts
        while True:
            try:
                next_handler(envelope)
                return
            except Exception:
                remaining -= 1
                if remaining == 0:
                    raise
