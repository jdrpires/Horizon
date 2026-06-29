"""Composed in-memory application service."""

from __future__ import annotations

from horizon_application.commands import RegisterAssetCommand
from horizon_application.dto import AssetDTO, RegisterAssetResultDTO
from horizon_application.handlers import ListAssetsQueryHandler, RegisterAssetCommandHandler
from horizon_application.mediator import CommandDispatcher, Mediator, QueryDispatcher
from horizon_application.pipelines import LoggingPipeline, Pipeline, ValidationPipeline
from horizon_application.queries import ListAssetsQuery
from horizon_application.services.event_mapping import DomainEventEnvelopeMapper
from horizon_application.services.in_memory import InMemoryAssetRepository, InMemoryUnitOfWork
from horizon_application.use_cases import RegisterAssetUseCase
from horizon_events import EventSubscriber, InMemoryEventBus
from horizon_kernel import Clock


class ApplicationService:
    """In-memory application service facade."""

    def __init__(
        self,
        *,
        repository: InMemoryAssetRepository,
        unit_of_work: InMemoryUnitOfWork,
        event_bus: InMemoryEventBus,
        mediator: Mediator,
        logging_pipeline: LoggingPipeline,
    ) -> None:
        """Create the service."""
        self.repository = repository
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
        command_dispatcher.register(
            RegisterAssetCommand,
            RegisterAssetCommandHandler(register_asset_use_case),
        )
        query_dispatcher.register(ListAssetsQuery, ListAssetsQueryHandler(repository))

        return cls(
            repository=repository,
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
