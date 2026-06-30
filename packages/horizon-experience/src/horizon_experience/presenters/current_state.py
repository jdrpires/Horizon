"""Current State presenter."""

from __future__ import annotations

from typing import Protocol

from horizon_experience.formatters import (
    friendly_observation_type,
    friendly_time,
    friendly_unit,
    friendly_value,
)
from horizon_experience.rendering import divider


class CurrentStateValueView(Protocol):
    """View contract for one Current State value."""

    observation_type: str
    value: float
    unit: str


class CurrentStateSnapshotView(Protocol):
    """View contract for a Current State snapshot."""

    values: tuple[CurrentStateValueView, ...]
    last_updated_at: str | None


def print_current_state(asset_name: str, status: str, snapshot: CurrentStateSnapshotView) -> None:
    """Print Current State in a human-friendly form."""
    divider()
    print(asset_name)
    divider()
    print("Status")
    print(_friendly_status(status))
    print()
    if not snapshot.values:
        print("Nenhuma observação registrada ainda.")
    for item in snapshot.values:
        print(friendly_observation_type(item.observation_type))
        print(f"{friendly_value(item.value)} {friendly_unit(item.unit)}")
        print()
    print("Última atualização")
    print(friendly_time(snapshot.last_updated_at))
    divider()


def _friendly_status(value: str) -> str:
    """Return a user-facing status label."""
    return {
        "registered": "Registrado",
        "active": "Ativo",
        "inactive": "Inativo",
        "archived": "Arquivado",
    }.get(value, value.title())
