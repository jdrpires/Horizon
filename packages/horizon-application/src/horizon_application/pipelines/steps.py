"""Built-in application pipeline steps."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol


class Validatable(Protocol):
    """Request contract for optional validation."""

    def validate(self) -> None:
        """Validate the request."""


class ValidationPipeline:
    """Validates requests before handler execution."""

    def handle(self, request: object, next_handler: Callable[[object], object]) -> object:
        """Validate a request and call the next handler."""
        if request is None:
            raise ValueError("request is required.")
        validate = getattr(request, "validate", None)
        if callable(validate):
            validate()
        return next_handler(request)


class LoggingPipeline:
    """In-memory logging pipeline for local application execution."""

    def __init__(self) -> None:
        """Create an empty log collector."""
        self.messages: list[str] = []

    def handle(self, request: object, next_handler: Callable[[object], object]) -> object:
        """Record before/after messages around handler execution."""
        request_name = type(request).__name__
        self.messages.append(f"handling:{request_name}")
        response = next_handler(request)
        self.messages.append(f"handled:{request_name}")
        return response
