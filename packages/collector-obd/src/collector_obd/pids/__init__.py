"""Supported OBD PIDs."""

from collector_obd.pids.registry import (
    CONTROL_MODULE_VOLTAGE_PID,
    COOLANT_TEMPERATURE_PID,
    RPM_PID,
    pid_by_command,
    supported_pids,
)

__all__ = [
    "CONTROL_MODULE_VOLTAGE_PID",
    "COOLANT_TEMPERATURE_PID",
    "RPM_PID",
    "pid_by_command",
    "supported_pids",
]
