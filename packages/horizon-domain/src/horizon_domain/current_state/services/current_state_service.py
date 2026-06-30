"""Current State domain service."""

from __future__ import annotations

from horizon_domain.asset import AssetId
from horizon_domain.current_state.entities import CurrentStateSnapshot
from horizon_domain.current_state.services.current_state_builder import CurrentStateBuilder
from horizon_domain.timeline import TimelineEntry


class CurrentStateService:
    """Builds Current State snapshots from Timeline entries."""

    def __init__(self, builder: CurrentStateBuilder | None = None) -> None:
        """Create the service."""
        self._builder = builder or CurrentStateBuilder()

    def snapshot(
        self,
        *,
        asset_id: AssetId,
        entries: tuple[TimelineEntry, ...],
    ) -> CurrentStateSnapshot:
        """Return the Current State snapshot."""
        return self._builder.build(asset_id=asset_id, entries=entries)
