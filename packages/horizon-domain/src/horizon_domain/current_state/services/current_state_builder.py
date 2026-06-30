"""Current State builder."""

from __future__ import annotations

from horizon_domain.asset import AssetId
from horizon_domain.current_state.entities import CurrentStateSnapshot
from horizon_domain.current_state.projections import CurrentStateProjection
from horizon_domain.timeline import TimelineEntry


class CurrentStateBuilder:
    """Builds Current State from Timeline replay."""

    def build(
        self,
        *,
        asset_id: AssetId,
        entries: tuple[TimelineEntry, ...],
    ) -> CurrentStateSnapshot:
        """Build an immutable snapshot from Timeline entries."""
        projection = CurrentStateProjection.empty(asset_id)
        for entry in sorted(entries, key=lambda item: (item.timestamp.value, item.sequence)):
            projection = projection.apply(entry)
        return projection.snapshot()
