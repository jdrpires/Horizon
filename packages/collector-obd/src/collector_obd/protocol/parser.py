"""OBD response parser."""

from __future__ import annotations

from collector_obd.exceptions import ObdParseError
from collector_obd.protocol.models import ObdPid, ObdResponse


def parse_pid_response(pid: ObdPid, response: ObdResponse) -> float:
    """Parse a supported PID response into a numeric value."""
    bytes_ = _extract_hex_bytes(response.raw)
    prefix = _extract_hex_bytes(pid.response_prefix)
    if bytes_[: len(prefix)] != prefix:
        raise ObdParseError(response.command.value, response.raw, "unexpected response prefix")
    data = bytes_[len(prefix) :]
    if pid.command.value == "010C":
        return _rpm(data)
    if pid.command.value == "0105":
        return _coolant_temperature(data)
    if pid.command.value == "0142":
        return _control_module_voltage(data)
    raise ObdParseError(response.command.value, response.raw, "unsupported PID")


def _rpm(data: tuple[int, ...]) -> float:
    """Parse 010C engine RPM."""
    _require_length(data, 2, "010C")
    return ((data[0] * 256) + data[1]) / 4


def _coolant_temperature(data: tuple[int, ...]) -> float:
    """Parse 0105 coolant temperature in Celsius."""
    _require_length(data, 1, "0105")
    return data[0] - 40


def _control_module_voltage(data: tuple[int, ...]) -> float:
    """Parse 0142 control module voltage."""
    _require_length(data, 2, "0142")
    return ((data[0] * 256) + data[1]) / 1000


def _require_length(data: tuple[int, ...], expected: int, command: str) -> None:
    """Ensure enough PID data bytes are present."""
    if len(data) < expected:
        raise ObdParseError(command, " ".join(f"{byte:02X}" for byte in data), "missing data bytes")


def _extract_hex_bytes(raw: str) -> tuple[int, ...]:
    """Extract hex bytes from an ELM327 response."""
    normalized = (
        raw.replace("\r", " ")
        .replace("\n", " ")
        .replace(">", " ")
        .replace("SEARCHING...", " ")
        .replace("BUS INIT: OK", " ")
    )
    tokens = normalized.split()
    bytes_: list[int] = []
    for token in tokens:
        clean = token.strip().upper()
        if len(clean) % 2 != 0:
            continue
        if not clean:
            continue
        try:
            bytes_.extend(int(clean[index : index + 2], 16) for index in range(0, len(clean), 2))
        except ValueError:
            continue
    if not bytes_:
        raise ObdParseError("unknown", raw, "no hex bytes found")
    return tuple(bytes_)
