"""OBD collector exceptions."""

from collector_obd.exceptions.errors import (
    AndroidBluetoothUnavailableError,
    ObdCollectorError,
    ObdParseError,
    ObdTransportError,
)

__all__ = [
    "AndroidBluetoothUnavailableError",
    "ObdCollectorError",
    "ObdParseError",
    "ObdTransportError",
]
