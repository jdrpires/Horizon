"""Shared primitives for the Horizon Event Platform."""

from horizon_events.shared.types import EventId, EventName
from horizon_events.shared.versioning import EventVersion, SchemaVersion, VersionCompatibility

__all__ = [
    "EventId",
    "EventName",
    "EventVersion",
    "SchemaVersion",
    "VersionCompatibility",
]
