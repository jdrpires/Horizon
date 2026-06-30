"""Mock OBD transport for deterministic local testing."""

from __future__ import annotations

from collector_obd.exceptions import ObdTransportError
from collector_obd.protocol.commands import (
    AT_ECHO_OFF,
    AT_HEADERS_OFF,
    AT_LINEFEEDS_OFF,
    AT_PROTOCOL_AUTO,
    AT_SPACES_OFF,
    ATZ,
    CONTROL_MODULE_VOLTAGE,
    COOLANT_TEMPERATURE,
    RPM,
)
from collector_obd.protocol.models import ObdCommand, ObdResponse


class MockObdTransport:
    """Deterministic ELM327 transport used by tests and the local probe."""

    def __init__(self, responses: dict[str, str] | None = None) -> None:
        """Create a mock transport."""
        self._responses = default_responses() | (responses or {})
        self._connected = False
        self.sent_commands: list[str] = []

    @property
    def connected(self) -> bool:
        """Return whether the transport is connected."""
        return self._connected

    def connect(self) -> None:
        """Open the mock transport."""
        self._connected = True

    def close(self) -> None:
        """Close the mock transport."""
        self._connected = False

    def send(self, command: ObdCommand) -> ObdResponse:
        """Return a configured response for one command."""
        if not self._connected:
            raise ObdTransportError("mock OBD transport is not connected")
        value = command.value.upper()
        self.sent_commands.append(value)
        try:
            raw = self._responses[value]
        except KeyError as exc:
            raise ObdTransportError(f"mock OBD response not configured for {value}") from exc
        return ObdResponse(command=command, raw=raw)


def default_responses() -> dict[str, str]:
    """Return deterministic ELM327 responses for supported commands."""
    return {
        ATZ.value: "ELM327 v1.5\r>",
        AT_ECHO_OFF.value: "OK\r>",
        AT_LINEFEEDS_OFF.value: "OK\r>",
        AT_SPACES_OFF.value: "OK\r>",
        AT_HEADERS_OFF.value: "OK\r>",
        AT_PROTOCOL_AUTO.value: "OK\r>",
        RPM.value: "41 0C 0E 10\r>",
        COOLANT_TEMPERATURE.value: "41 05 83\r>",
        CONTROL_MODULE_VOLTAGE.value: "41 42 37 64\r>",
    }
