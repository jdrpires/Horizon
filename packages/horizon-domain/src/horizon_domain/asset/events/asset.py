"""Asset domain events."""

from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Self

from horizon_domain.asset.value_objects import AssetId
from horizon_kernel import DomainEvent, UniqueId


class AssetDomainEvent(DomainEvent):
    """Base class for Asset domain events."""

    event_name: ClassVar[str] = "AssetDomainEvent"

    @classmethod
    def create(
        cls,
        *,
        asset_id: AssetId,
        correlation_id: UniqueId,
        causation_id: UniqueId,
        occurred_at: datetime,
        version: int,
        payload: dict[str, object] | None = None,
    ) -> Self:
        """Create an Asset domain event."""
        return cls(
            event_id=UniqueId.new(),
            aggregate_id=asset_id.value,
            correlation_id=correlation_id,
            causation_id=causation_id,
            occurred_at=occurred_at,
            version=version,
            metadata={"event_name": cls.event_name},
            payload={} if payload is None else payload,
        )


class AssetRegistered(AssetDomainEvent):
    """Asset was registered."""

    event_name: ClassVar[str] = "AssetRegistered"


class AssetActivated(AssetDomainEvent):
    """Asset was activated."""

    event_name: ClassVar[str] = "AssetActivated"


class AssetDeactivated(AssetDomainEvent):
    """Asset was deactivated."""

    event_name: ClassVar[str] = "AssetDeactivated"


class AssetArchived(AssetDomainEvent):
    """Asset was archived."""

    event_name: ClassVar[str] = "AssetArchived"


class AssetTransferred(AssetDomainEvent):
    """Asset ownership changed."""

    event_name: ClassVar[str] = "AssetTransferred"


class AssetConfigurationChanged(AssetDomainEvent):
    """Asset configuration changed."""

    event_name: ClassVar[str] = "AssetConfigurationChanged"
