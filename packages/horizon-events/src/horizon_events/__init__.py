"""Horizon Event Platform public API."""

from horizon_events.context import CorrelationContext, current_context, use_context
from horizon_events.dispatchers import (
    InMemoryEventDispatcher,
    LoggingMiddleware,
    MetricsMiddleware,
    RetryMiddleware,
    TracingMiddleware,
    ValidationMiddleware,
)
from horizon_events.envelopes import EventEnvelope
from horizon_events.event_bus import InMemoryEventBus
from horizon_events.metadata import EventMetadata
from horizon_events.publishers import InMemoryEventPublisher
from horizon_events.registry import EventRegistration, EventRegistry
from horizon_events.serializers import DictionarySerializer
from horizon_events.shared import (
    EventId,
    EventName,
    EventVersion,
    SchemaVersion,
    VersionCompatibility,
)
from horizon_events.subscribers import (
    CategoryFilter,
    EventNameFilter,
    EventSubscriber,
    Subscription,
    TenantFilter,
)

__all__ = [
    "CategoryFilter",
    "CorrelationContext",
    "DictionarySerializer",
    "EventEnvelope",
    "EventId",
    "EventMetadata",
    "EventName",
    "EventNameFilter",
    "EventRegistration",
    "EventRegistry",
    "EventSubscriber",
    "EventVersion",
    "InMemoryEventBus",
    "InMemoryEventDispatcher",
    "InMemoryEventPublisher",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "RetryMiddleware",
    "SchemaVersion",
    "Subscription",
    "TenantFilter",
    "TracingMiddleware",
    "ValidationMiddleware",
    "VersionCompatibility",
    "current_context",
    "use_context",
]
