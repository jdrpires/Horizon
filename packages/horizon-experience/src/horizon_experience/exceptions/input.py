"""Input exceptions for Horizon Experience."""

from __future__ import annotations


class UserCancelled(Exception):
    """Raised when a user cancels an interactive prompt."""
