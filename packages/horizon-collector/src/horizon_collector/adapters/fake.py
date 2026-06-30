"""Fake collector used to prove ingestion without hardware."""

from __future__ import annotations

from datetime import UTC, datetime

from horizon_collector.collector import RawObservation
from horizon_collector.runtime.session import CollectorSession


class FakeCollector:
    """Collector that emits deterministic vehicle-like observations."""

    name = "fake"

    def collect(self, session: CollectorSession) -> tuple[RawObservation, ...]:
        """Emit raw observations without Bluetooth, OBD, CAN, or hardware."""
        observed_at = datetime.now(UTC)
        return (
            RawObservation(
                key="engine.rpm",
                value=900,
                observed_at=observed_at,
                source=self.name,
                metadata={"session_id": session.session_id},
            ),
            RawObservation(
                key="engine.coolant.temperature",
                value=91,
                observed_at=observed_at,
                source=self.name,
                metadata={"session_id": session.session_id},
            ),
            RawObservation(
                key="electrical.battery.voltage",
                value=14.18,
                observed_at=observed_at,
                source=self.name,
                metadata={"session_id": session.session_id},
            ),
        )
