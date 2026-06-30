"""ELM327 commands supported by the spike."""

from __future__ import annotations

from collector_obd.protocol.models import ObdCommand

ATZ = ObdCommand("ATZ", "Reset ELM327 adapter")
AT_ECHO_OFF = ObdCommand("ATE0", "Disable command echo")
AT_LINEFEEDS_OFF = ObdCommand("ATL0", "Disable linefeeds")
AT_SPACES_OFF = ObdCommand("ATS0", "Disable spaces")
AT_HEADERS_OFF = ObdCommand("ATH0", "Disable headers")
AT_PROTOCOL_AUTO = ObdCommand("ATSP0", "Use automatic protocol selection")

RPM = ObdCommand("010C", "Read engine RPM")
COOLANT_TEMPERATURE = ObdCommand("0105", "Read coolant temperature")
CONTROL_MODULE_VOLTAGE = ObdCommand("0142", "Read control module voltage")


def initialization_commands() -> tuple[ObdCommand, ...]:
    """Return the basic ELM327 initialization sequence."""
    return (
        ATZ,
        AT_ECHO_OFF,
        AT_LINEFEEDS_OFF,
        AT_SPACES_OFF,
        AT_HEADERS_OFF,
        AT_PROTOCOL_AUTO,
    )


def pid_commands() -> tuple[ObdCommand, ...]:
    """Return supported OBD PID commands."""
    return (RPM, COOLANT_TEMPERATURE, CONTROL_MODULE_VOLTAGE)
