"""Unit of Work interface."""

from __future__ import annotations

from typing import Protocol


class UnitOfWork(Protocol):
    """Unit of Work boundary for future transactional adapters."""

    def commit(self) -> None:
        """Commit work."""

    def rollback(self) -> None:
        """Rollback work."""
