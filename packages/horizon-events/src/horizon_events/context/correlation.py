"""ContextVar-based correlation propagation."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class CorrelationContext:
    """Correlation values propagated across event platform calls."""

    correlation_id: str
    trace_id: str
    causation_id: str
    request_id: str

    @classmethod
    def new(cls, *, causation_id: str | None = None) -> CorrelationContext:
        """Create a new correlation context."""
        correlation_id = str(uuid4())
        return cls(
            correlation_id=correlation_id,
            trace_id=str(uuid4()),
            causation_id=causation_id or correlation_id,
            request_id=str(uuid4()),
        )


_context: ContextVar[CorrelationContext | None] = ContextVar(
    "horizon_event_correlation_context",
    default=None,
)


def current_context() -> CorrelationContext:
    """Return the current correlation context, creating one when absent."""
    context = _context.get()
    if context is None:
        context = CorrelationContext.new()
        _context.set(context)
    return context


@contextmanager
def use_context(context: CorrelationContext) -> Iterator[CorrelationContext]:
    """Temporarily bind a correlation context."""
    token = _context.set(context)
    try:
        yield context
    finally:
        _context.reset(token)
