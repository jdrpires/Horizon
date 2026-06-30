"""Android Bluetooth transport boundary.

This spike does not implement native Android Bluetooth access. Real Bluetooth
requires an Android runtime or bridge with explicit permissions, paired device
selection, socket lifecycle, and user-controlled operational constraints.
"""

from __future__ import annotations

from dataclasses import dataclass

from collector_obd.exceptions import AndroidBluetoothUnavailableError
from collector_obd.protocol.models import ObdCommand, ObdResponse


@dataclass(slots=True)
class AndroidBluetoothTransport:
    """Documented placeholder for a future Android Bluetooth transport."""

    device_address: str
    channel: int = 1

    def connect(self) -> None:
        """Reject local execution until an approved Android Bluetooth bridge exists."""
        raise AndroidBluetoothUnavailableError(
            "Android Bluetooth transport requires a native Android execution environment or an "
            "approved bridge. This spike only defines the boundary and documents the flow."
        )

    def close(self) -> None:
        """No-op close for the placeholder boundary."""

    def send(self, command: ObdCommand) -> ObdResponse:
        """Reject sending commands until the native Android transport is approved."""
        raise AndroidBluetoothUnavailableError(
            f"cannot send {command.value}: Android Bluetooth transport is not implemented."
        )
