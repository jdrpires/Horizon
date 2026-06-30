"""ELM327 collector adapter."""

from __future__ import annotations

from datetime import UTC, datetime

from horizon_collector.collector import RawObservation
from horizon_collector.runtime import CollectorSession

from collector_obd.pids import supported_pids
from collector_obd.protocol import initialization_commands, parse_pid_response
from collector_obd.protocol.models import ObdSession, ObdTransport


class Elm327Adapter:
    """Collector-compatible adapter for ELM327 OBD data."""

    name = "android-obd-elm327"

    def __init__(self, transport: ObdTransport) -> None:
        """Create the adapter."""
        self._transport = transport
        self._session = ObdSession()

    @property
    def obd_session(self) -> ObdSession:
        """Return the OBD session state."""
        return self._session

    def initialize(self) -> None:
        """Initialize the ELM327 adapter."""
        self._transport.connect()
        for command in initialization_commands():
            self._transport.send(command)
        self._session.initialized = True

    def close(self) -> None:
        """Close the underlying transport."""
        self._transport.close()

    def collect(self, session: CollectorSession) -> tuple[RawObservation, ...]:
        """Collect raw observations from supported OBD PIDs."""
        if not self._session.initialized:
            self.initialize()
        observed_at = datetime.now(UTC)
        observations: list[RawObservation] = []
        for pid in supported_pids():
            response = self._transport.send(pid.command)
            value = parse_pid_response(pid, response)
            observations.append(
                RawObservation(
                    key=pid.external_key,
                    value=value,
                    observed_at=observed_at,
                    source=self.name,
                    metadata={
                        "collector_session_id": session.session_id,
                        "obd_session_id": self._session.session_id,
                        "pid": pid.command.value,
                        "catalog_key": pid.catalog_key,
                        "unit": pid.unit,
                        "raw_response": response.raw,
                    },
                )
            )
        return tuple(observations)
