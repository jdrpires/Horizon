"""Register Observation use case."""

from __future__ import annotations

from datetime import UTC, datetime

from horizon_application.commands import RegisterObservationCommand
from horizon_application.contracts import AssetRepository, ObservationRepository, UnitOfWork
from horizon_application.dto import EventEnvelopeDTO, ObservationDTO, RegisterObservationResultDTO
from horizon_application.services.event_mapping import DomainEventEnvelopeMapper
from horizon_domain import AssetId
from horizon_domain.observation import (
    Observation,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
    RegisterObservation,
)
from horizon_domain.timeline import TimelineRepository
from horizon_events import InMemoryEventBus
from horizon_kernel import Clock


class RegisterObservationUseCase:
    """Coordinates the Register Observation vertical slice."""

    def __init__(
        self,
        *,
        asset_repository: AssetRepository,
        observation_repository: ObservationRepository,
        unit_of_work: UnitOfWork,
        event_bus: InMemoryEventBus,
        event_mapper: DomainEventEnvelopeMapper,
        timeline_repository: TimelineRepository | None = None,
        clock: Clock | None = None,
    ) -> None:
        """Create the use case."""
        self._asset_repository = asset_repository
        self._observation_repository = observation_repository
        self._unit_of_work = unit_of_work
        self._event_bus = event_bus
        self._event_mapper = event_mapper
        self._timeline_repository = timeline_repository
        self._clock = clock

    def execute(self, request: RegisterObservationCommand) -> RegisterObservationResultDTO:
        """Register an Observation and publish produced events."""
        try:
            asset_id = AssetId.from_string(request.asset_id)
            if self._asset_repository.get(asset_id) is None:
                raise ValueError("asset_id does not reference an existing Asset.")
            observation = Observation.register(
                RegisterObservation(
                    asset_id=asset_id,
                    observation_type=ObservationType(request.observation_type),
                    value=ObservationValue(request.value),
                    unit=ObservationUnit(request.unit),
                    source=ObservationSource(request.source),
                    timestamp=ObservationTimestamp(_parse_timestamp(request.timestamp)),
                    quality=ObservationQuality(request.quality),
                ),
                self._clock,
            )
            self._observation_repository.save(observation)
            if self._timeline_repository is not None:
                self._timeline_repository.append_observation(observation)
            envelopes = self._event_mapper.map_all(observation.pull_events())
            self._event_bus.publish_many(envelopes)
            self._unit_of_work.commit()
            return RegisterObservationResultDTO(
                observation=ObservationDTO.from_observation(observation),
                events=tuple(EventEnvelopeDTO.from_envelope(envelope) for envelope in envelopes),
            )
        except Exception:
            self._unit_of_work.rollback()
            raise


def _parse_timestamp(value: str | None) -> datetime:
    """Parse an optional ISO timestamp."""
    if value is None or not value.strip():
        return datetime.now(UTC)
    parsed = datetime.fromisoformat(value.strip())
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed
