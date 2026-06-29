"""Compatibility relationships for protocol and schema versions."""

from enum import StrEnum


class Compatibility(StrEnum):
    """Compatibility relationship between two versions."""

    SAME = "same"
    BACKWARD_COMPATIBLE = "backward_compatible"
    FUTURE_COMPATIBLE = "future_compatible"
    INCOMPATIBLE = "incompatible"
