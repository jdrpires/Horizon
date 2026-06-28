"""Repository interface for aggregate persistence boundaries."""

from __future__ import annotations

from typing import Protocol, TypeVar

from horizon_kernel.entities import Entity
from horizon_kernel.ids import UniqueId

TEntity = TypeVar("TEntity", bound=Entity)


class Repository(Protocol[TEntity]):
    """Persistence boundary for entities and aggregate roots."""

    def get(self, id: UniqueId) -> TEntity | None:
        """Return an entity by identifier when it exists."""

    def save(self, entity: TEntity) -> None:
        """Persist an entity."""

    def delete(self, entity: TEntity) -> None:
        """Delete an entity."""
