"""Current State queries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetCurrentStateQuery:
    """Query Current State for one Asset."""

    asset_id: str
