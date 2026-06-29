"""Timeline application queries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetTimelineQuery:
    """Query Timeline entries."""

    asset_id: str | None = None
    observation_type: str | None = None
    start_at: str | None = None
    end_at: str | None = None
    cursor_at: str | None = None


@dataclass(frozen=True, slots=True)
class ReplayTimelineQuery:
    """Replay Timeline entries."""

    asset_id: str | None = None
    observation_type: str | None = None
    start_at: str | None = None
    end_at: str | None = None
