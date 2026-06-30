"""Storage exception types."""

from __future__ import annotations


class StorageError(Exception):
    """Base error for Horizon storage adapters."""


class StorageCorruptionError(StorageError):
    """Raised when a storage file cannot be decoded or validated."""
