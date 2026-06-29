"""Application mediator."""

from __future__ import annotations

from horizon_application.mediator.dispatchers import CommandDispatcher, QueryDispatcher


class Mediator:
    """Routes commands and queries through their dispatchers."""

    def __init__(
        self,
        command_dispatcher: CommandDispatcher,
        query_dispatcher: QueryDispatcher,
    ) -> None:
        """Create a mediator."""
        self._command_dispatcher = command_dispatcher
        self._query_dispatcher = query_dispatcher

    def send(self, command: object) -> object:
        """Send a command."""
        return self._command_dispatcher.dispatch(command)

    def ask(self, query: object) -> object:
        """Send a query."""
        return self._query_dispatcher.dispatch(query)
