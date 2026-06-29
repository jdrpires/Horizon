"""Asset aggregate root."""

from __future__ import annotations

from datetime import datetime

from horizon_domain.asset.commands import (
    ActivateAsset,
    ArchiveAsset,
    DeactivateAsset,
    RegisterAsset,
    TransferOwnership,
    UpdateConfiguration,
)
from horizon_domain.asset.events import (
    AssetActivated,
    AssetArchived,
    AssetConfigurationChanged,
    AssetDeactivated,
    AssetDomainEvent,
    AssetRegistered,
    AssetTransferred,
)
from horizon_domain.asset.exceptions import asset_rule_violation
from horizon_domain.asset.value_objects import (
    AssetClassification,
    AssetConfiguration,
    AssetId,
    AssetIdentity,
    AssetStatus,
    Ownership,
)
from horizon_kernel import AggregateRoot, Clock, SystemClock, UniqueId


class Asset(AggregateRoot):
    """Root aggregate for universal Horizon assets."""

    __slots__ = ("_classification", "_configuration", "_identity", "_ownership", "_status")

    def __init__(
        self,
        *,
        asset_id: AssetId,
        identity: AssetIdentity,
        classification: AssetClassification,
        ownership: Ownership,
        configuration: AssetConfiguration,
        status: AssetStatus,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        version: int = 1,
        clock: Clock | None = None,
    ) -> None:
        """Create an Asset aggregate."""
        super().__init__(
            id=asset_id.value,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            clock=clock,
        )
        self._identity = identity
        self._classification = classification
        self._ownership = ownership
        self._configuration = configuration
        self._status = status

    @classmethod
    def register(cls, command: RegisterAsset, clock: Clock | None = None) -> Asset:
        """Register a new Asset and record the registration event."""
        resolved_clock = SystemClock() if clock is None else clock
        asset = cls(
            asset_id=command.asset_id,
            identity=command.identity,
            classification=command.classification,
            ownership=command.ownership,
            configuration=command.configuration,
            status=AssetStatus.REGISTERED,
            clock=resolved_clock,
        )
        asset.record_event(
            AssetRegistered.create(
                asset_id=asset.asset_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                occurred_at=resolved_clock.now(),
                version=asset.version,
                payload={
                    "identity": asset.identity.to_dict(),
                    "classification": asset.classification.to_dict(),
                    "ownership": asset.ownership.to_dict(),
                    "configuration": asset.configuration.to_dict(),
                    "status": asset.status.value,
                },
            )
        )
        return asset

    @property
    def asset_id(self) -> AssetId:
        """Return the stable Asset ID."""
        return AssetId(self.id)

    @property
    def identity(self) -> AssetIdentity:
        """Return Asset identity."""
        return self._identity

    @property
    def classification(self) -> AssetClassification:
        """Return Asset classification."""
        return self._classification

    @property
    def ownership(self) -> Ownership:
        """Return Asset ownership."""
        return self._ownership

    @property
    def configuration(self) -> AssetConfiguration:
        """Return Asset configuration."""
        return self._configuration

    @property
    def status(self) -> AssetStatus:
        """Return Asset lifecycle status."""
        return self._status

    def activate(self, command: ActivateAsset, clock: Clock | None = None) -> None:
        """Activate this Asset."""
        self._ensure_targets_this_asset(command.asset_id)
        if self.status is AssetStatus.ARCHIVED:
            raise asset_rule_violation("archived_activation", "Archived Asset cannot be activated.")
        if self.status is AssetStatus.ACTIVE:
            return
        self._change_status(
            status=AssetStatus.ACTIVE,
            event=AssetActivated,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            clock=clock,
        )

    def deactivate(self, command: DeactivateAsset, clock: Clock | None = None) -> None:
        """Deactivate this Asset."""
        self._ensure_targets_this_asset(command.asset_id)
        self._ensure_not_archived("Archived Asset cannot be deactivated.")
        if self.status is AssetStatus.INACTIVE:
            return
        self._change_status(
            status=AssetStatus.INACTIVE,
            event=AssetDeactivated,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            clock=clock,
            payload={"reason": command.reason},
        )

    def archive(self, command: ArchiveAsset, clock: Clock | None = None) -> None:
        """Archive this Asset without deleting it."""
        self._ensure_targets_this_asset(command.asset_id)
        if self.status is AssetStatus.ARCHIVED:
            return
        self._change_status(
            status=AssetStatus.ARCHIVED,
            event=AssetArchived,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            clock=clock,
            payload={"reason": command.reason},
        )

    def transfer_ownership(self, command: TransferOwnership, clock: Clock | None = None) -> None:
        """Transfer this Asset to new ownership."""
        self._ensure_targets_this_asset(command.asset_id)
        self._ensure_not_archived("Archived Asset cannot transfer ownership.")
        if command.ownership == self.ownership:
            return
        old_ownership = self.ownership
        self._ownership = command.ownership
        self._record_change(
            event=AssetTransferred,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            clock=clock,
            payload={
                "previous_ownership": old_ownership.to_dict(),
                "ownership": self.ownership.to_dict(),
            },
        )

    def update_configuration(self, command: UpdateConfiguration, clock: Clock | None = None) -> None:
        """Update this Asset's generic configuration."""
        self._ensure_targets_this_asset(command.asset_id)
        self._ensure_not_archived("Archived Asset cannot change configuration.")
        if command.configuration == self.configuration:
            return
        old_configuration = self.configuration
        self._configuration = command.configuration
        self._record_change(
            event=AssetConfigurationChanged,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            clock=clock,
            payload={
                "previous_configuration": old_configuration.to_dict(),
                "configuration": self.configuration.to_dict(),
            },
        )

    def _change_status(
        self,
        *,
        status: AssetStatus,
        event: type[AssetDomainEvent],
        correlation_id: UniqueId,
        causation_id: UniqueId,
        clock: Clock | None,
        payload: dict[str, object] | None = None,
    ) -> None:
        """Change status and emit the supplied event."""
        previous_status = self.status
        self._status = status
        event_payload = {"previous_status": previous_status.value, "status": self.status.value}
        if payload is not None:
            event_payload.update(payload)
        self._record_change(
            event=event,
            correlation_id=correlation_id,
            causation_id=causation_id,
            clock=clock,
            payload=event_payload,
        )

    def _record_change(
        self,
        *,
        event: type[AssetDomainEvent],
        correlation_id: UniqueId,
        causation_id: UniqueId,
        clock: Clock | None,
        payload: dict[str, object],
    ) -> None:
        """Touch the aggregate, increment version, and record an Asset event."""
        resolved_clock = SystemClock() if clock is None else clock
        self.touch(resolved_clock)
        self.increment_version()
        self.record_event(
            event.create(
                asset_id=self.asset_id,
                correlation_id=correlation_id,
                causation_id=causation_id,
                occurred_at=resolved_clock.now(),
                version=self.version,
                payload=payload,
            )
        )

    def _ensure_targets_this_asset(self, asset_id: AssetId) -> None:
        """Ensure a command targets this aggregate."""
        if asset_id != self.asset_id:
            raise asset_rule_violation("id_mismatch", "Command targets a different Asset.")

    def _ensure_not_archived(self, message: str) -> None:
        """Ensure archived Assets cannot be modified."""
        if self.status is AssetStatus.ARCHIVED:
            raise asset_rule_violation("archived", message)
