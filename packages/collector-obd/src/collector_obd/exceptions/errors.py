"""OBD collector errors."""

from __future__ import annotations


class ObdCollectorError(Exception):
    """Base error for OBD collector failures."""


class ObdTransportError(ObdCollectorError):
    """Raised when the OBD transport fails."""


class AndroidBluetoothUnavailableError(ObdTransportError):
    """Raised when Android Bluetooth transport is not available in this environment."""


class ObdParseError(ObdCollectorError):
    """Raised when an OBD response cannot be parsed."""

    def __init__(self, command: str, raw: str, reason: str) -> None:
        """Create the error."""
        super().__init__(f"could not parse OBD response for {command}: {reason}. raw={raw!r}")
