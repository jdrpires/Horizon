"""Timeline handlers."""

from horizon_application.timeline.dto import ReplayTimelineResultDTO, TimelineResultDTO
from horizon_application.timeline.queries import GetTimelineQuery, ReplayTimelineQuery
from horizon_application.timeline.use_cases import GetTimelineUseCase, ReplayTimelineUseCase


class GetTimelineQueryHandler:
    """Handler for Timeline queries."""

    def __init__(self, use_case: GetTimelineUseCase) -> None:
        """Create the handler."""
        self._use_case = use_case

    def handle(self, query: GetTimelineQuery) -> TimelineResultDTO:
        """Handle the query."""
        return self._use_case.execute(query)


class ReplayTimelineQueryHandler:
    """Handler for Timeline replay queries."""

    def __init__(self, use_case: ReplayTimelineUseCase) -> None:
        """Create the handler."""
        self._use_case = use_case

    def handle(self, query: ReplayTimelineQuery) -> ReplayTimelineResultDTO:
        """Handle the query."""
        return self._use_case.execute(query)
