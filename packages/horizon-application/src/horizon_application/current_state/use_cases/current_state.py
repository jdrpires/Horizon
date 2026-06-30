"""Current State use cases."""

from __future__ import annotations

from horizon_application.current_state.dto import CurrentStateSnapshotDTO
from horizon_application.current_state.queries import GetCurrentStateQuery
from horizon_domain import AssetId
from horizon_domain.current_state import CurrentStateService
from horizon_domain.timeline import TimelineRepository


class GetCurrentStateUseCase:
    """Build Current State from Timeline."""

    def __init__(
        self,
        *,
        timeline_repository: TimelineRepository,
        current_state_service: CurrentStateService,
    ) -> None:
        """Create the use case."""
        self._timeline_repository = timeline_repository
        self._current_state_service = current_state_service

    def execute(self, request: GetCurrentStateQuery) -> CurrentStateSnapshotDTO:
        """Return the Current State snapshot for an Asset."""
        asset_id = AssetId.from_string(request.asset_id)
        entries = self._timeline_repository.get_timeline(asset_id)
        snapshot = self._current_state_service.snapshot(asset_id=asset_id, entries=entries)
        return CurrentStateSnapshotDTO.from_snapshot(snapshot)
