"""Horizon Lab menus."""

from __future__ import annotations

from horizon_experience.rendering import divider


def print_menu() -> None:
    """Print the main Horizon Lab menu."""
    divider()
    print("HORIZON LAB")
    print("1 Cadastrar Asset")
    print("2 Registrar Observação")
    print("3 Ver Linha do Tempo")
    print("4 Ver Estado Atual")
    print("5 Sair")
    divider()
