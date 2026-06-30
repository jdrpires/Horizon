"""Supported OBD PID registry."""

from __future__ import annotations

from collector_obd.protocol.commands import CONTROL_MODULE_VOLTAGE, COOLANT_TEMPERATURE, RPM
from collector_obd.protocol.models import ObdPid

RPM_PID = ObdPid(
    command=RPM,
    response_prefix="41 0C",
    external_key="engine.rpm",
    catalog_key="engine.rpm",
    unit="rpm",
)

COOLANT_TEMPERATURE_PID = ObdPid(
    command=COOLANT_TEMPERATURE,
    response_prefix="41 05",
    external_key="engine.coolant.temperature",
    catalog_key="engine.temperature",
    unit="celsius",
)

CONTROL_MODULE_VOLTAGE_PID = ObdPid(
    command=CONTROL_MODULE_VOLTAGE,
    response_prefix="41 42",
    external_key="electrical.battery.voltage",
    catalog_key="electrical.battery_voltage",
    unit="volt",
)


def supported_pids() -> tuple[ObdPid, ...]:
    """Return supported PIDs in probe order."""
    return (RPM_PID, COOLANT_TEMPERATURE_PID, CONTROL_MODULE_VOLTAGE_PID)


def pid_by_command(command: str) -> ObdPid:
    """Return a supported PID by command value."""
    clean = command.strip().upper()
    for pid in supported_pids():
        if pid.command.value == clean:
            return pid
    raise ValueError(f"unsupported OBD PID command: {command}")
