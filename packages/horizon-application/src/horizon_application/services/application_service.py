"""Composed in-memory application service."""

from __future__ import annotations

from horizon_application.commands import RegisterAssetCommand, RegisterObservationCommand
from horizon_application.contracts import AssetRepository, ObservationRepository
from horizon_application.current_state import CurrentStateSnapshotDTO, GetCurrentStateQuery
from horizon_application.current_state.handlers import GetCurrentStateQueryHandler
from horizon_application.current_state.use_cases import GetCurrentStateUseCase
from horizon_application.dto import (
    AssetDTO,
    ObservationDTO,
    RegisterAssetResultDTO,
    RegisterObservationResultDTO,
)
from horizon_application.handlers import (
    ListAssetsQueryHandler,
    ListObservationsQueryHandler,
    RegisterAssetCommandHandler,
    RegisterObservationCommandHandler,
)
from horizon_application.mediator import CommandDispatcher, Mediator, QueryDispatcher
from horizon_application.pipelines import LoggingPipeline, Pipeline, ValidationPipeline
from horizon_application.queries import ListAssetsQuery, ListObservationsQuery
from horizon_application.services.event_mapping import DomainEventEnvelopeMapper
from horizon_application.services.in_memory import (
    InMemoryAssetRepository,
    InMemoryObservationRepository,
    InMemoryUnitOfWork,
)
from horizon_application.timeline import (
    GetTimelineQuery,
    InMemoryTimelineRepository,
    ReplayTimelineQuery,
    ReplayTimelineResultDTO,
    TimelineResultDTO,
)
from horizon_application.timeline.handlers import (
    GetTimelineQueryHandler,
    ReplayTimelineQueryHandler,
)
from horizon_application.timeline.use_cases import GetTimelineUseCase, ReplayTimelineUseCase
from horizon_domain.current_state import CurrentStateService
from horizon_application.use_cases import RegisterAssetUseCase, RegisterObservationUseCase
from horizon_domain.timeline import ReplayEngine, TimelineRepository
from horizon_events import EventSubscriber, InMemoryEventBus
from horizon_kernel import Clock


class ApplicationService:
    """In-memory application service facade."""

    def __init__(
        self,
        *,
        repository: AssetRepository,
        observation_repository: ObservationRepository,
        timeline_repository: TimelineRepository,
        unit_of_work: InMemoryUnitOfWork,
        event_bus: InMemoryEventBus,
        mediator: Mediator,
        logging_pipeline: LoggingPipeline,
    ) -> None:
        """Create the service."""
        self.repository = repository
        self.observation_repository = observation_repository
        self.timeline_repository = timeline_repository
        self.unit_of_work = unit_of_work
        self.event_bus = event_bus
        self.mediator = mediator
        self.logging_pipeline = logging_pipeline

    @classmethod
    def create_in_memory(
        cls,
        *,
        event_subscribers: tuple[EventSubscriber, ...] = (),
        clock: Clock | None = None,
    ) -> ApplicationService:
        """Create a fully wired in-memory application service."""
        repository = InMemoryAssetRepository()
        observation_repository = InMemoryObservationRepository()
        timeline_repository = InMemoryTimelineRepository()
        return cls.create_with_repositories(
            repository=repository,
            observation_repository=observation_repository,
            timeline_repository=timeline_repository,
            event_subscribers=event_subscribers,
            clock=clock,
        )

    @classmethod
    def create_with_repositories(
        cls,
        *,
        repository: AssetRepository,
        observation_repository: ObservationRepository,
        timeline_repository: TimelineRepository,
        event_subscribers: tuple[EventSubscriber, ...] = (),
        clock: Clock | None = None,
    ) -> ApplicationService:
        """Create an application service with externally supplied repositories."""
        unit_of_work = InMemoryUnitOfWork()
        event_bus = InMemoryEventBus()
        for subscriber in event_subscribers:
            event_bus.subscribe(subscriber)

        logging_pipeline = LoggingPipeline()
        pipeline = Pipeline((ValidationPipeline(), logging_pipeline))
        command_dispatcher = CommandDispatcher(pipeline)
        query_dispatcher = QueryDispatcher(pipeline)
        mediator = Mediator(command_dispatcher, query_dispatcher)

        register_asset_use_case = RegisterAssetUseCase(
            repository=repository,
            unit_of_work=unit_of_work,
            event_bus=event_bus,
            event_mapper=DomainEventEnvelopeMapper(source="asset.register"),
            clock=clock,
        )
        register_observation_use_case = RegisterObservationUseCase(
            asset_repository=repository,
            observation_repository=observation_repository,
            unit_of_work=unit_of_work,
            event_bus=event_bus,
            event_mapper=DomainEventEnvelopeMapper(source="observation.register"),
            timeline_repository=timeline_repository,
            clock=clock,
        )
        get_timeline_use_case = GetTimelineUseCase(timeline_repository)
        replay_timeline_use_case = ReplayTimelineUseCase(timeline_repository, ReplayEngine())
        get_current_state_use_case = GetCurrentStateUseCase(
            timeline_repository=timeline_repository,
            current_state_service=CurrentStateService(),
        )
        command_dispatcher.register(
            RegisterAssetCommand,
            RegisterAssetCommandHandler(register_asset_use_case),
        )
        command_dispatcher.register(
            RegisterObservationCommand,
            RegisterObservationCommandHandler(register_observation_use_case),
        )
        query_dispatcher.register(ListAssetsQuery, ListAssetsQueryHandler(repository))
        query_dispatcher.register(
            ListObservationsQuery,
            ListObservationsQueryHandler(observation_repository),
        )
        query_dispatcher.register(
            GetTimelineQuery,
            GetTimelineQueryHandler(get_timeline_use_case),
        )
        query_dispatcher.register(
            ReplayTimelineQuery,
            ReplayTimelineQueryHandler(replay_timeline_use_case),
        )
        query_dispatcher.register(
            GetCurrentStateQuery,
            GetCurrentStateQueryHandler(get_current_state_use_case),
        )

        return cls(
            repository=repository,
            observation_repository=observation_repository,
            timeline_repository=timeline_repository,
            unit_of_work=unit_of_work,
            event_bus=event_bus,
            mediator=mediator,
            logging_pipeline=logging_pipeline,
        )

    def register_asset(self, command: RegisterAssetCommand) -> RegisterAssetResultDTO:
        """Register an Asset."""
        return self.mediator.send(command)  # type: ignore[return-value]

    def list_assets(self) -> tuple[AssetDTO, ...]:
        """List registered Assets."""
        return self.mediator.ask(ListAssetsQuery())  # type: ignore[return-value]

    def register_observation(
        self,
        command: RegisterObservationCommand,
    ) -> RegisterObservationResultDTO:
        """Register an Observation."""
        return self.mediator.send(command)  # type: ignore[return-value]

    def list_observations(self) -> tuple[ObservationDTO, ...]:
        """List registered Observations."""
        return self.mediator.ask(ListObservationsQuery())  # type: ignore[return-value]

    def show_timeline(self, query: GetTimelineQuery | None = None) -> TimelineResultDTO:
        """Return Timeline entries."""
        return self.mediator.ask(query or GetTimelineQuery())  # type: ignore[return-value]

    def replay_timeline(
        self,
        query: ReplayTimelineQuery | None = None,
    ) -> ReplayTimelineResultDTO:
        """Replay Timeline entries."""
        return self.mediator.ask(query or ReplayTimelineQuery())  # type: ignore[return-value]

    def get_current_state(self, query: GetCurrentStateQuery) -> CurrentStateSnapshotDTO:
        """Return Current State for an Asset."""
        return self.mediator.ask(query)  # type: ignore[return-value]
