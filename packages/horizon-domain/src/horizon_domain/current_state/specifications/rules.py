"""Current State specifications."""

from __future__ import annotations

from horizon_domain.current_state.entities import CurrentStateSnapshot


def is_snapshot_immutable(snapshot: CurrentStateSnapshot) -> bool:
    """Return whether snapshot values are represented immutably."""
    return isinstance(snapshot.values, tuple)
