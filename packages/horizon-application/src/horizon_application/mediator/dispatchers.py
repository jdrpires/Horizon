"""Command and query dispatchers."""

from __future__ import annotations

from typing import Protocol, TypeVar

from horizon_application.exceptions import HandlerNotFoundError
from horizon_application.pipelines import Pipeline

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class RequestHandler(Protocol[RequestT, ResponseT]):
    """Request handler contract."""

    def handle(self, request: RequestT) -> ResponseT:
        """Handle a request."""


class Dispatcher:
    """Base dispatcher for commands and queries."""

    def __init__(self, pipeline: Pipeline | None = None) -> None:
        """Create a dispatcher."""
        self._pipeline = Pipeline() if pipeline is None else pipeline
        self._handlers: dict[type[object], RequestHandler[object, object]] = {}

    def register(
        self,
        request_type: type[RequestT],
        handler: RequestHandler[RequestT, ResponseT],
    ) -> None:
        """Register a handler for one request type."""
        self._handlers[request_type] = handler  # type: ignore[assignment]

    def dispatch(self, request: RequestT) -> ResponseT:
        """Dispatch a request to its registered handler."""
        handler = self._handlers.get(type(request))
        if handler is None:
            raise HandlerNotFoundError(f"No handler registered for {type(request).__name__}.")
        return self._pipeline.execute(request, handler.handle)  # type: ignore[return-value]


class CommandDispatcher(Dispatcher):
    """Dispatcher for application commands."""


class QueryDispatcher(Dispatcher):
    """Dispatcher for application queries."""
