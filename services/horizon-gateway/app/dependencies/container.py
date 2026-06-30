"""Gateway dependency container."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Request

from horizon_application import ApplicationService, InMemoryTimelineRepository
from horizon_catalog import load_vehicle_catalog
from horizon_collector import CatalogObservationMapper, ObservationSourceMapping
from horizon_storage import JsonStorageBootstrap

from app.config import GatewaySettings
from app.services import HorizonQueryService, LiveIngestionService


@dataclass(frozen=True, slots=True)
class GatewayContainer:
    """Composed dependencies for one Gateway app instance."""

    ingestion_service: LiveIngestionService
    query_service: HorizonQueryService
    storage_path: str


def build_container(settings: GatewaySettings) -> GatewayContainer:
    """Build the Gateway dependency graph."""
    bootstrap = JsonStorageBootstrap(settings.storage_path).bootstrap()
    timeline_repository = InMemoryTimelineRepository()
    for observation in bootstrap.observation_repository.list():
        timeline_repository.append_observation(observation)
    application = ApplicationService.create_with_repositories(
        repository=bootstrap.asset_repository,
        observation_repository=bootstrap.observation_repository,
        timeline_repository=timeline_repository,
    )
    catalog = load_vehicle_catalog()
    mapper = CatalogObservationMapper(
        catalog=catalog,
        source_mappings=(
            ObservationSourceMapping(
                external_key="engine.coolant.temperature",
                catalog_key="engine.temperature",
            ),
            ObservationSourceMapping(
                external_key="electrical.battery.voltage",
                catalog_key="electrical.battery_voltage",
            ),
        ),
    )
    return GatewayContainer(
        ingestion_service=LiveIngestionService(
            application=application,
            catalog=catalog,
            mapper=mapper,
        ),
        query_service=HorizonQueryService(application),
        storage_path=str(settings.storage_path),
    )


def get_ingestion_service(request: Request) -> LiveIngestionService:
    """Return the app-scoped ingestion service."""
    container: GatewayContainer = request.app.state.container
    return container.ingestion_service


def get_query_service(request: Request) -> HorizonQueryService:
    """Return the app-scoped query service."""
    container: GatewayContainer = request.app.state.container
    return container.query_service
