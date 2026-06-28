"""In-memory event registry for names, versions, schemas, handlers, and categories."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from horizon_events.envelopes import EventEnvelope
from horizon_events.shared import EventName, EventVersion, SchemaVersion
from horizon_events.subscribers import EventHandler


@dataclass(frozen=True, slots=True)
class EventRegistration:
    """Registered event descriptor."""

    event_name: EventName
    version: EventVersion
    schema_version: SchemaVersion
    schema: Mapping[str, object]
    handler: EventHandler | None
    category: str

    @property
    def key(self) -> tuple[str, int]:
        """Return registry key."""
        return (self.event_name.value, self.version.value)


class EventRegistry:
    """Registry of platform event definitions."""

    def __init__(self) -> None:
        """Create an empty registry."""
        self._registrations: dict[tuple[str, int], EventRegistration] = {}

    def register(
        self,
        *,
        event_name: str,
        version: int,
        schema_version: int,
        schema: Mapping[str, object],
        category: str,
        handler: EventHandler | None = None,
    ) -> EventRegistration:
        """Register an event definition."""
        registration = EventRegistration(
            event_name=EventName(event_name),
            version=EventVersion(version),
            schema_version=SchemaVersion(schema_version),
            schema=dict(schema),
            handler=handler,
            category=category,
        )
        self._registrations[registration.key] = registration
        return registration

    def handler(
        self,
        *,
        event_name: str,
        version: int,
        schema_version: int,
        schema: Mapping[str, object],
        category: str,
    ) -> Callable[[EventHandler], EventHandler]:
        """Decorate and register an event handler."""

        def decorator(handler: EventHandler) -> EventHandler:
            self.register(
                event_name=event_name,
                version=version,
                schema_version=schema_version,
                schema=schema,
                category=category,
                handler=handler,
            )
            return handler

        return decorator

    def get(self, event_name: str, version: int) -> EventRegistration | None:
        """Return a registration when present."""
        return self._registrations.get((event_name, version))

    def resolve_handler(self, envelope: EventEnvelope) -> EventHandler | None:
        """Return a registered handler for an envelope when present."""
        registration = self.get(envelope.event_name.value, envelope.version.value)
        if registration is None:
            return None
        return registration.handler

    def list(self) -> tuple[EventRegistration, ...]:
        """Return all registrations."""
        return tuple(self._registrations.values())

    def clear(self) -> None:
        """Clear all registrations."""
        self._registrations.clear()
