"""Register Asset use case."""

from __future__ import annotations

from horizon_application.commands import RegisterAssetCommand
from horizon_application.contracts import AssetRepository, UnitOfWork
from horizon_application.dto import AssetDTO, EventEnvelopeDTO, RegisterAssetResultDTO
from horizon_application.services.event_mapping import DomainEventEnvelopeMapper
from horizon_domain import (
    Asset,
    AssetClassification,
    AssetConfiguration,
    AssetIdentity,
    Ownership,
    RegisterAsset,
)
from horizon_events import InMemoryEventBus
from horizon_kernel import Clock


class RegisterAssetUseCase:
    """Coordinates the Register Asset vertical slice."""

    def __init__(
        self,
        *,
        repository: AssetRepository,
        unit_of_work: UnitOfWork,
        event_bus: InMemoryEventBus,
        event_mapper: DomainEventEnvelopeMapper,
        clock: Clock | None = None,
    ) -> None:
        """Create the use case."""
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus
        self._event_mapper = event_mapper
        self._clock = clock

    def execute(self, request: RegisterAssetCommand) -> RegisterAssetResultDTO:
        """Register an Asset and publish produced events."""
        try:
            asset = Asset.register(
                RegisterAsset(
                    identity=AssetIdentity(request.name, request.external_reference),
                    classification=AssetClassification(request.category, request.kind),
                    ownership=Ownership(request.owner_id, request.tenant_id),
                    configuration=AssetConfiguration(request.configuration),
                ),
                self._clock,
            )
            self._repository.save(asset)
            envelopes = self._event_mapper.map_all(asset.pull_events())
            self._event_bus.publish_many(envelopes)
            self._unit_of_work.commit()
            return RegisterAssetResultDTO(
                asset=AssetDTO.from_asset(asset),
                events=tuple(EventEnvelopeDTO.from_envelope(envelope) for envelope in envelopes),
            )
        except Exception:
            self._unit_of_work.rollback()
            raise
