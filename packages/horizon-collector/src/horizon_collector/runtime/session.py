"""Collector session model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from horizon_collector.collector.models import CollectorSessionState, utc_now


@dataclass(slots=True)
class CollectorSession:
    """Execution context for one collector run."""

    collector_name: str
    session_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None
    state: CollectorSessionState = CollectorSessionState.CREATED

    def start(self) -> None:
        """Mark the session as running."""
        self.state = CollectorSessionState.RUNNING

    def complete(self) -> None:
        """Mark the session as completed."""
        self.completed_at = utc_now()
        self.state = CollectorSessionState.COMPLETED

    def fail(self) -> None:
        """Mark the session as failed."""
        self.completed_at = utc_now()
        self.state = CollectorSessionState.FAILED
