"""Application queries for Assets."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListAssetsQuery:
    """List registered Assets."""
