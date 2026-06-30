"""Query orchestration for Horizon clients."""

from __future__ import annotations

from horizon_application import ApplicationService, GetCurrentStateQuery, GetTimelineQuery

from app.services.ingestion import AssetReferenceResolver
from app.schemas import (
    AssetListResponse,
    AssetSummary,
    CurrentStateResponse,
    CurrentStateValueResponse,
    TimelineEntryResponse,
    TimelineResponse,
)


class HorizonQueryService:
    """Read-only Gateway boundary for Horizon client projections."""

    def __init__(self, application: ApplicationService) -> None:
        self._application = application

    def list_assets(self) -> AssetListResponse:
        """Return all known Assets."""
        return AssetListResponse(
            assets=tuple(
                AssetSummary(
                    asset_id=asset.asset_id,
                    name=asset.name,
                    external_reference=asset.external_reference,
                    category=asset.category,
                    status=asset.status,
                )
                for asset in self._application.list_assets()
            )
        )

    def get_current_state(self, asset_reference: str) -> CurrentStateResponse:
        """Return Current State for an existing Asset."""
        asset = AssetReferenceResolver(self._application).resolve(asset_reference)
        snapshot = self._application.get_current_state(
            GetCurrentStateQuery(asset_id=asset.asset_id)
        )
        return CurrentStateResponse(
            asset_id=snapshot.asset_id,
            last_updated_at=snapshot.last_updated_at,
            observation_count=snapshot.observation_count,
            values=tuple(
                CurrentStateValueResponse(
                    type=value.observation_type,
                    value=value.value,
                    unit=value.unit,
                    source=value.source,
                    timestamp=value.timestamp,
                    observation_id=value.observation_id,
                    sequence=value.sequence,
                )
                for value in snapshot.values
            ),
        )

    def get_timeline(self, asset_reference: str) -> TimelineResponse:
        """Return Timeline entries for an existing Asset."""
        asset = AssetReferenceResolver(self._application).resolve(asset_reference)
        timeline = self._application.show_timeline(GetTimelineQuery(asset_id=asset.asset_id))
        return TimelineResponse(
            asset_id=asset.asset_id,
            entries=tuple(
                TimelineEntryResponse(
                    asset_id=entry.asset_id,
                    observation_id=entry.observation_id,
                    type=entry.observation_type,
                    value=entry.value,
                    unit=entry.unit,
                    source=entry.source,
                    timestamp=entry.timestamp,
                    quality=entry.quality,
                    sequence=entry.sequence,
                )
                for entry in timeline.entries
            ),
        )
