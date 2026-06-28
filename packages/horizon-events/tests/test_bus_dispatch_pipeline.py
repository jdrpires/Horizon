from collections.abc import Mapping
from typing import cast

import pytest

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
from horizon_events.publishers import InMemoryEventPublisher
from horizon_events.subscribers import (
    CategoryFilter,
    EventNameFilter,
    EventSubscriber,
    TenantFilter,
)

from .test_envelope_metadata_serialization import make_envelope


def test_event_bus_publish_subscribe_unsubscribe_and_clear() -> None:
    received: list[str] = []
    bus = InMemoryEventBus()
    subscriber = EventSubscriber(
        name="example-handler",
        handler=lambda envelope: received.append(envelope.event_name.value),
        filters=(EventNameFilter("example.created"),),
    )

    subscription = bus.subscribe(subscriber)
    bus.publish(make_envelope())
    bus.unsubscribe(subscription)
    bus.publish(make_envelope())
    bus.clear()

    assert received == ["example.created"]
    assert bus.subscriptions == ()


def test_event_bus_publish_many_preserves_order() -> None:
    received: list[int] = []
    bus = InMemoryEventBus()
    bus.subscribe(
        EventSubscriber(
            name="collector",
            handler=lambda envelope: received.append(int(str(envelope.event["value"]))),
        )
    )
    first = make_envelope("example.first")
    second = make_envelope("example.second")

    bus.publish_many((first, second))

    assert received == [1, 1]


def test_subscriber_filters_can_combine_name_category_and_tenant() -> None:
    received: list[str] = []
    bus = InMemoryEventBus()
    bus.subscribe(
        EventSubscriber(
            name="filtered",
            handler=lambda envelope: received.append(envelope.metadata.aggregate_id),
            filters=(
                EventNameFilter("example.created"),
                CategoryFilter("example"),
                TenantFilter("tenant-a"),
            ),
        )
    )

    bus.publish(make_envelope())
    bus.publish(make_envelope("example.ignored"))

    assert received == ["aggregate-1"]


def test_dispatch_pipeline_runs_middlewares_and_handlers() -> None:
    logs: list[str] = []
    received: list[str] = []
    metrics = MetricsMiddleware()
    dispatcher = InMemoryEventDispatcher(
        middlewares=(
            LoggingMiddleware(logs.append),
            metrics,
            ValidationMiddleware(),
            TracingMiddleware(),
        )
    )
    bus = InMemoryEventBus(dispatcher)
    bus.subscribe(
        EventSubscriber(name="handler", handler=lambda envelope: received.append("handled"))
    )

    bus.publish(make_envelope())

    assert received == ["handled"]
    assert metrics.count == 1
    assert logs[0].startswith("example.created:")


def test_retry_middleware_retries_failed_dispatch() -> None:
    attempts = {"count": 0}

    def flaky_handler(_envelope: object) -> None:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RuntimeError("transient")

    dispatcher = InMemoryEventDispatcher(middlewares=(RetryMiddleware(attempts=2),))
    bus = InMemoryEventBus(dispatcher)
    bus.subscribe(EventSubscriber(name="flaky", handler=flaky_handler))

    bus.publish(make_envelope())

    assert attempts == {"count": 2}


def test_middlewares_validate_trace_version_and_retry_configuration() -> None:
    envelope_data = make_envelope().to_dict()
    envelope_data["version"] = 0
    with pytest.raises(ValueError):
        ValidationMiddleware().handle(EventEnvelope.from_dict(envelope_data), lambda envelope: None)

    trace_data = make_envelope().to_dict()
    metadata = dict(cast(Mapping[str, object], trace_data["metadata"]))
    metadata["trace_id"] = ""
    trace_data["metadata"] = metadata
    with pytest.raises(ValueError):
        TracingMiddleware().handle(EventEnvelope.from_dict(trace_data), lambda envelope: None)

    with pytest.raises(ValueError):
        RetryMiddleware(attempts=0)


def test_publisher_delegates_to_event_bus() -> None:
    received: list[str] = []
    bus = InMemoryEventBus()
    publisher = InMemoryEventPublisher(bus)
    bus.subscribe(EventSubscriber(name="handler", handler=lambda envelope: received.append("ok")))

    publisher.publish(make_envelope())
    publisher.publish_many((make_envelope(),))

    assert received == ["ok", "ok"]
