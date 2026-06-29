"""Mediator and pipeline behavior tests."""

import pytest

from horizon_application import (
    CommandDispatcher,
    LoggingPipeline,
    Pipeline,
    RegisterAssetCommand,
    ValidationPipeline,
)
from horizon_application.exceptions import HandlerNotFoundError


class EchoHandler:
    """Test handler."""

    def handle(self, command: RegisterAssetCommand) -> str:
        """Handle a command."""
        return command.name


def test_command_dispatcher_runs_validation_logging_and_handler() -> None:
    logging = LoggingPipeline()
    dispatcher = CommandDispatcher(Pipeline((ValidationPipeline(), logging)))
    dispatcher.register(RegisterAssetCommand, EchoHandler())
    command = RegisterAssetCommand(name="Asset", category="generic.asset", owner_id="owner")

    result = dispatcher.dispatch(command)

    assert result == "Asset"
    assert logging.messages == ["handling:RegisterAssetCommand", "handled:RegisterAssetCommand"]


def test_validation_pipeline_rejects_invalid_command() -> None:
    dispatcher = CommandDispatcher(Pipeline((ValidationPipeline(),)))
    dispatcher.register(RegisterAssetCommand, EchoHandler())

    with pytest.raises(ValueError, match="name is required"):
        dispatcher.dispatch(RegisterAssetCommand(name=" ", category="generic.asset", owner_id="owner"))


def test_dispatcher_rejects_unknown_command() -> None:
    dispatcher = CommandDispatcher()

    with pytest.raises(HandlerNotFoundError, match="No handler registered"):
        dispatcher.dispatch(RegisterAssetCommand(name="Asset", category="generic.asset", owner_id="owner"))
