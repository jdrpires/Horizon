"""Timeline use cases."""

from __future__ import annotations

from datetime import UTC, datetime

from horizon_application.timeline.dto import (
    ReplayTimelineResultDTO,
    TimelineEntryDTO,
    TimelineResultDTO,
)
from horizon_application.timeline.queries import GetTimelineQuery, ReplayTimelineQuery
from horizon_domain import AssetId
from horizon_domain.observation import ObservationTimestamp, ObservationType
from horizon_domain.timeline import ReplayEngine, TimelineCursor, TimelineQuery, TimelineRepository


class GetTimelineUseCase:
    """Query Timeline entries."""

    def __init__(self, repository: TimelineRepository) -> None:
        """Create the use case."""
        self._repository = repository

    def execute(self, request: GetTimelineQuery) -> TimelineResultDTO:
        """Execute a Timeline query."""
        entries = self._repository.query(_to_domain_query(request))
        return TimelineResultDTO(tuple(TimelineEntryDTO.from_entry(entry) for entry in entries))


class ReplayTimelineUseCase:
    """Replay Timeline entries."""

    def __init__(self, repository: TimelineRepository, replay_engine: ReplayEngine) -> None:
        """Create the use case."""
        self._repository = repository
        self._replay_engine = replay_engine

    def execute(self, request: ReplayTimelineQuery) -> ReplayTimelineResultDTO:
        """Execute a deterministic Timeline replay."""
        query = GetTimelineQuery(
            asset_id=request.asset_id,
            observation_type=request.observation_type,
            start_at=request.start_at,
            end_at=request.end_at,
        )
        entries = self._replay_engine.replay(self._repository.query(_to_domain_query(query)))
        return ReplayTimelineResultDTO(
            tuple(TimelineEntryDTO.from_entry(entry) for entry in entries)
        )


def _to_domain_query(request: GetTimelineQuery) -> TimelineQuery:
    """Map an application query to a domain Timeline query."""
    return TimelineQuery(
        asset_id=None if request.asset_id is None else AssetId.from_string(request.asset_id),
        observation_type=None
        if request.observation_type is None
        else ObservationType(request.observation_type),
        start_at=None if request.start_at is None else ObservationTimestamp(_parse_datetime(request.start_at)),
        end_at=None if request.end_at is None else ObservationTimestamp(_parse_datetime(request.end_at)),
        cursor=None if request.cursor_at is None else TimelineCursor(_parse_datetime(request.cursor_at)),
    )


def _parse_datetime(value: str) -> datetime:
    """Parse an ISO datetime and assume UTC when timezone is omitted."""
    parsed = datetime.fromisoformat(value.strip())
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed
