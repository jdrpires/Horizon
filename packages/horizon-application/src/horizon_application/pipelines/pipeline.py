"""Application pipeline implementation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")
Handler = Callable[[RequestT], ResponseT]


class PipelineStep(Protocol[RequestT, ResponseT]):
    """Pipeline step contract."""

    def handle(self, request: RequestT, next_handler: Handler[RequestT, ResponseT]) -> ResponseT:
        """Handle the request or delegate to the next handler."""


class Pipeline:
    """Builds an in-process application pipeline."""

    def __init__(self, steps: tuple[PipelineStep[object, object], ...] = ()) -> None:
        """Create a pipeline with ordered steps."""
        self._steps = steps

    def execute(self, request: RequestT, terminal: Handler[RequestT, ResponseT]) -> ResponseT:
        """Execute the request through all steps."""
        next_handler: Handler[object, object] = terminal  # type: ignore[assignment]
        for step in reversed(self._steps):
            current = next_handler

            def wrapped(
                value: object,
                step: PipelineStep[object, object] = step,
                current: Handler[object, object] = current,
            ) -> object:
                return step.handle(value, current)

            next_handler = wrapped
        return next_handler(request)  # type: ignore[return-value]
