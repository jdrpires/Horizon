"""Timeline presenter."""

from __future__ import annotations

from typing import Protocol

from horizon_experience.formatters import (
    friendly_observation_type,
    friendly_source,
    friendly_time,
    friendly_unit,
    friendly_value,
)
from horizon_experience.rendering import divider


class TimelineEntryView(Protocol):
    """View contract for a Timeline entry."""

    observation_type: str
    value: float
    unit: str
    source: str
    timestamp: str


def print_timeline(entries: tuple[TimelineEntryView, ...]) -> None:
    """Print Timeline entries in a user-friendly form."""
    if not entries:
        print("Nenhuma observação registrada ainda.")
        return
    divider()
    print("Linha do tempo")
    divider()
    for entry in reversed(entries):
        print(friendly_time(entry.timestamp))
        print(friendly_observation_type(entry.observation_type))
        print(f"{friendly_value(entry.value)} {friendly_unit(entry.unit)}")
        print(friendly_source(entry.source))
        print("-" * 21)
