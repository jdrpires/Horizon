"""Android/Realme operating notes for the OBD spike."""

from __future__ import annotations


def android_pairing_steps() -> tuple[str, ...]:
    """Return manual pairing steps for Realme and ELM327."""
    return (
        "Plug the ELM327 adapter into the vehicle OBD-II port.",
        "Turn the vehicle ignition to accessory or engine-on mode.",
        "On the Realme device, open Bluetooth settings.",
        "Pair with the ELM327 device using the adapter PIN, commonly 1234 or 0000.",
        "Confirm the paired device name and address before running the probe.",
    )


def android_probe_limitations() -> tuple[str, ...]:
    """Return current Bluetooth limitations."""
    return (
        "This repository does not include a native Android Bluetooth runtime.",
        "The Python probe supports mock transport locally.",
        "Real Bluetooth execution requires an approved Android bridge or native app shell.",
        "No observations are persisted automatically by the probe.",
    )
