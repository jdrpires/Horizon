"""In-memory dispatcher implementation."""

from __future__ import annotations

from collections.abc import Callable

from horizon_events.envelopes import EventEnvelope
from horizon_events.subscribers import EventSubscriber

from .middleware import EventMiddleware


class InMemoryEventDispatcher:
    """Dispatches envelopes to matching subscribers in the current process."""

    def __init__(self, middlewares: tuple[EventMiddleware, ...] = ()) -> None:
        """Create a dispatcher with an optional middleware pipeline."""
        self._middlewares = middlewares

    def dispatch(self, envelope: EventEnvelope, subscribers: tuple[EventSubscriber, ...]) -> None:
        """Dispatch an envelope to matching subscribers."""

        def invoke(target: EventEnvelope) -> None:
            for subscriber in subscribers:
                if subscriber.matches(target):
                    subscriber.handle(target)

        pipeline = self._build_pipeline(invoke)
        pipeline(envelope)

    def _build_pipeline(
        self, terminal: Callable[[EventEnvelope], None]
    ) -> Callable[[EventEnvelope], None]:
        """Build a middleware pipeline around the terminal dispatch step."""
        next_handler = terminal
        for middleware in reversed(self._middlewares):
            current = next_handler

            def wrapped(
                envelope: EventEnvelope,
                middleware: EventMiddleware = middleware,
                current: Callable[[EventEnvelope], None] = current,
            ) -> None:
                middleware.handle(envelope, current)

            next_handler = wrapped
        return next_handler
