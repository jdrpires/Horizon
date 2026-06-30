"""Storage adapter contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class StorageAdapter(Protocol):
    """Low-level storage adapter contract."""

    root: Path

    def ensure_storage(self) -> None:
        """Create missing storage resources."""

    def read_json(self, filename: str) -> object:
        """Read a JSON document."""

    def write_json(self, filename: str, payload: object) -> None:
        """Write a JSON document."""


class StorageSerializer[T](Protocol):
    """Serializer contract for persisted domain facts."""

    def serialize(self, value: T) -> dict[str, object]:
        """Serialize a value."""

    def deserialize(self, payload: dict[str, object]) -> T:
        """Deserialize a value."""


class StorageBootstrap(Protocol):
    """Storage bootstrap contract."""

    def bootstrap(self) -> object:
        """Prepare storage and load persisted facts."""
