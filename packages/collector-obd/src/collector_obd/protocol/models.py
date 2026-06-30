"""OBD protocol contracts and value models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ObdCommand:
    """One ELM327 command."""

    value: str
    description: str

    def __post_init__(self) -> None:
        """Validate command shape."""
        if not self.value.strip():
            raise ValueError("OBD command value cannot be blank.")
        if not self.description.strip():
            raise ValueError("OBD command description cannot be blank.")


@dataclass(frozen=True, slots=True)
class ObdResponse:
    """Raw response returned by an OBD transport."""

    command: ObdCommand
    raw: str

    def __post_init__(self) -> None:
        """Validate response shape."""
        if not self.raw.strip():
            raise ValueError("OBD response cannot be blank.")


@dataclass(frozen=True, slots=True)
class ObdPid:
    """Supported OBD PID definition."""

    command: ObdCommand
    response_prefix: str
    external_key: str
    catalog_key: str
    unit: str

    def __post_init__(self) -> None:
        """Validate PID shape."""
        for field_name, value in {
            "response_prefix": self.response_prefix,
            "external_key": self.external_key,
            "catalog_key": self.catalog_key,
            "unit": self.unit,
        }.items():
            if not value.strip():
                raise ValueError(f"{field_name} cannot be blank.")


@dataclass(slots=True)
class ObdSession:
    """Execution context for one ELM327 probe session."""

    session_id: str = ""
    started_at: datetime | None = None
    initialized: bool = False

    def __post_init__(self) -> None:
        """Initialize defaults."""
        if not self.session_id:
            self.session_id = str(uuid4())
        if self.started_at is None:
            self.started_at = datetime.now(UTC)


class ObdTransport(Protocol):
    """Transport boundary for ELM327 communication."""

    def connect(self) -> None:
        """Open the transport."""
        ...

    def close(self) -> None:
        """Close the transport."""
        ...

    def send(self, command: ObdCommand) -> ObdResponse:
        """Send one command and return the response."""
        ...
