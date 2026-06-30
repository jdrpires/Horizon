"""Catalog exception types."""

from __future__ import annotations


class CatalogError(Exception):
    """Base error for Horizon catalogs."""


class DefinitionNotFoundError(CatalogError):
    """Raised when an Observation definition cannot be found."""
