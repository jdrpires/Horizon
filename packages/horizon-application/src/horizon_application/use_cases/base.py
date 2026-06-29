"""Use case base contract."""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class UseCase(Protocol, Generic[RequestT, ResponseT]):
    """Application use case contract."""

    def execute(self, request: RequestT) -> ResponseT:
        """Execute the use case."""
