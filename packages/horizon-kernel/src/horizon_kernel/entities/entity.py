"""Base entity model."""

from __future__ import annotations

from datetime import datetime
from typing import Self

from horizon_kernel.exceptions import DomainException, ValidationError
from horizon_kernel.ids import UniqueId
from horizon_kernel.utils import Clock, SystemClock


class Entity:
    """Mutable domain object identified by a stable unique identifier."""

    __slots__ = ("_created_at", "_id", "_metadata", "_updated_at", "_version")

    def __init__(
        self,
        *,
        id: UniqueId | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        version: int = 1,
        metadata: dict[str, object] | None = None,
        clock: Clock | None = None,
    ) -> None:
        """Create an entity with identity and lifecycle metadata."""
        resolved_clock = SystemClock() if clock is None else clock
        now = resolved_clock.now()
        resolved_created_at = now if created_at is None else created_at
        resolved_updated_at = resolved_created_at if updated_at is None else updated_at
        self._validate_timestamp(resolved_created_at, "created_at")
        self._validate_timestamp(resolved_updated_at, "updated_at")
        if version < 1:
            raise DomainException(
                ValidationError("entity.version", "Entity version must be greater than zero.")
            )
        self._id = UniqueId.new() if id is None else id
        self._created_at = resolved_created_at
        self._updated_at = resolved_updated_at
        self._version = version
        self._metadata = {} if metadata is None else dict(metadata)

    @property
    def id(self) -> UniqueId:
        """Return the entity identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Return when the entity was created."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return when the entity was last updated."""
        return self._updated_at

    @property
    def version(self) -> int:
        """Return the entity version."""
        return self._version

    @property
    def metadata(self) -> dict[str, object]:
        """Return a defensive copy of entity metadata."""
        return dict(self._metadata)

    def touch(self, clock: Clock) -> None:
        """Update the last-modified timestamp using the supplied clock."""
        self._updated_at = clock.now()

    def increment_version(self) -> None:
        """Increment the entity version."""
        self._version += 1

    def set_metadata(self, key: str, value: object) -> None:
        """Set one metadata value."""
        self._metadata[key] = value

    def remove_metadata(self, key: str) -> None:
        """Remove one metadata value when present."""
        self._metadata.pop(key, None)

    def same_identity_as(self, other: Entity) -> bool:
        """Return whether another entity has the same concrete type and identity."""
        return type(self) is type(other) and self.id == other.id

    def __eq__(self, other: object) -> bool:
        """Compare entities by concrete type and identity."""
        if not isinstance(other, Entity):
            return NotImplemented
        return self.same_identity_as(other)

    def __hash__(self) -> int:
        """Hash entities by concrete type and identity."""
        return hash((type(self), self.id))

    @classmethod
    def _validate_timestamp(cls, value: datetime, field: str) -> None:
        """Validate a timezone-aware timestamp."""
        if value.tzinfo is None:
            raise DomainException(
                ValidationError("entity.timestamp_timezone", f"{field} must be timezone-aware.")
            )

    @classmethod
    def rehydrate(
        cls,
        *,
        id: UniqueId,
        created_at: datetime,
        updated_at: datetime,
        version: int,
        metadata: dict[str, object] | None = None,
    ) -> Self:
        """Rebuild an entity from persisted primitive state."""
        return cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            metadata=metadata,
        )
