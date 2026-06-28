"""Snapshot store contract without implementation."""

from __future__ import annotations

from typing import Protocol


class SnapshotStore(Protocol):
    """Persistence boundary for aggregate snapshots."""

    def save(self, stream_name: str, version: int, snapshot: dict[str, object]) -> None:
        """Save a snapshot for a stream version."""

    def load(self, stream_name: str) -> dict[str, object] | None:
        """Load the latest snapshot for a stream."""
