"""Plain terminal rendering helpers."""

from __future__ import annotations

WIDTH = 44


def divider() -> None:
    """Print a visual divider."""
    print("━" * WIDTH)


def section(title: str) -> None:
    """Print a section title."""
    divider()
    print(title)
    divider()


def success(message: str) -> None:
    """Print a success message."""
    print(f"OK {message}")


def error(message: str) -> None:
    """Print an error message."""
    print(f"Erro: {message}")


def info(message: str) -> None:
    """Print an informational message."""
    print(message)
