"""Live ingestion orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any

from horizon_application import (
    ApplicationService,
    GetCurrentStateQuery,
    GetTimelineQuery,
    RegisterObservationCommand,
)
from horizon_catalog import ObservationCatalogRegistry
from horizon_collector import CatalogObservationMapper, RawObservation
from horizon_collector.collector import CanonicalObservation

from app.schemas import (
    IngestedObservation,
    ObservationIngestionRequest,
    ObservationIngestionResponse,
    ObservationItem,
)
from app.validation import validate_catalog_item


@dataclass(frozen=True, slots=True)
class AssetReference:
    """Resolved Asset reference for gateway ingestion."""

    requested: str
    asset_id: str


class AssetReferenceResolver:
    """Resolve gateway Asset references without creating Assets."""

    def __init__(self, application: ApplicationService) -> None:
        self._application = application

    def resolve(self, reference: str) -> AssetReference:
        """Resolve an Asset ID or external reference against existing Assets."""
        clean = reference.strip()
        for asset in self._application.list_assets():
            if asset.asset_id == clean or asset.external_reference == clean:
                return AssetReference(requested=clean, asset_id=asset.asset_id)
        raise ValueError(f"asset_id does not reference an existing Asset: {clean}")


class ApplicationObservationPublisher:
    """Publish canonical observations into Horizon Application."""

    def __init__(
        self,
        *,
        application: ApplicationService,
        asset: AssetReference,
    ) -> None:
        self._application = application
        self._asset = asset
        self._published: list[Any] = []

    @property
    def published(self) -> tuple[Any, ...]:
        """Return application results produced by publication."""
        return tuple(self._published)

    def publish(self, observation: CanonicalObservation) -> None:
        """Publish one canonical Observation through the Application Layer."""
        result = self._application.register_observation(
            RegisterObservationCommand(
                asset_id=self._asset.asset_id,
                observation_type=observation.observation_type,
                value=float(observation.value),
                unit=observation.unit,
                source=observation.source,
                timestamp=observation.observed_at.isoformat(),
                quality=str(observation.metadata.get("quality", "good")),
            )
        )
        self._published.append(result)

    def publish_many(self, observations: tuple[CanonicalObservation, ...]) -> None:
        """Publish many canonical Observations."""
        for observation in observations:
            self.publish(observation)


class LiveIngestionService:
    """Gateway boundary that validates and forwards live observations."""

    def __init__(
        self,
        *,
        application: ApplicationService,
        catalog: ObservationCatalogRegistry,
        mapper: CatalogObservationMapper,
    ) -> None:
        self._application = application
        self._catalog = catalog
        self._mapper = mapper
        self._lock = Lock()

    def ingest(self, request: ObservationIngestionRequest) -> ObservationIngestionResponse:
        """Validate, map, publish, and summarize one live ingestion payload."""
        with self._lock:
            asset = AssetReferenceResolver(self._application).resolve(request.asset_id)
            raw_observations = tuple(
                self._to_raw_observation(request, item) for item in request.observations
            )
            canonical = self._mapper.map_many(raw_observations)
            publisher = ApplicationObservationPublisher(
                application=self._application,
                asset=asset,
            )
            publisher.publish_many(canonical)
            timeline = self._application.show_timeline(GetTimelineQuery(asset_id=asset.asset_id))
            current_state = self._application.get_current_state(
                GetCurrentStateQuery(asset_id=asset.asset_id)
            )
            ingested = tuple(
                IngestedObservation(
                    definition_id=canonical_item.definition.id,
                    observation_id=result.observation.observation_id,
                    observation_type=result.observation.observation_type,
                    value=result.observation.value,
                    unit=result.observation.unit,
                    timestamp=result.observation.timestamp,
                )
                for canonical_item, result in zip(canonical, publisher.published, strict=True)
            )
            return ObservationIngestionResponse(
                status="accepted",
                source=request.source,
                asset_id=asset.asset_id,
                accepted=len(ingested),
                observations=ingested,
                event_count=sum(len(result.events) for result in publisher.published),
                timeline_entries=len(timeline.entries),
                current_state_values=len(current_state.values),
            )

    def _to_raw_observation(
        self,
        request: ObservationIngestionRequest,
        item: ObservationItem,
    ) -> RawObservation:
        """Convert one HTTP item into a Collector Framework raw observation."""
        value = validate_catalog_item(catalog=self._catalog, item=item)
        return RawObservation(
            key=item.definition_id,
            value=value,
            observed_at=item.timestamp,
            source=request.source,
            metadata={
                "asset_id": request.asset_id,
                "quality": item.quality,
                "unit": item.unit,
            },
        )
