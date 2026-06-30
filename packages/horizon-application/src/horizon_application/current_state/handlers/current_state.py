"""Current State handlers."""

from horizon_application.current_state.dto import CurrentStateSnapshotDTO
from horizon_application.current_state.queries import GetCurrentStateQuery
from horizon_application.current_state.use_cases import GetCurrentStateUseCase


class GetCurrentStateQueryHandler:
    """Handler for Current State queries."""

    def __init__(self, use_case: GetCurrentStateUseCase) -> None:
        """Create the handler."""
        self._use_case = use_case

    def handle(self, query: GetCurrentStateQuery) -> CurrentStateSnapshotDTO:
        """Handle the query."""
        return self._use_case.execute(query)
