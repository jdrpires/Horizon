from collections.abc import MutableMapping
from datetime import UTC, datetime
from typing import cast

import pytest

from horizon_kernel.aggregates import AggregateRoot
from horizon_kernel.entities import Entity
from horizon_kernel.events import DomainEvent
from horizon_kernel.exceptions import DomainException
from horizon_kernel.ids import UniqueId
from horizon_kernel.utils import FrozenClock


class PublishedEvents:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        self.events.append(event)

    def publish_all(self, events: tuple[DomainEvent, ...]) -> None:
        self.events.extend(events)


def test_entity_has_identity_lifecycle_version_and_metadata() -> None:
    instant = datetime(2026, 1, 1, tzinfo=UTC)
    entity = Entity(clock=FrozenClock(instant), metadata={"source": "test"})

    assert entity.id
    assert entity.created_at == instant
    assert entity.updated_at == instant
    assert entity.version == 1
    assert entity.metadata == {"source": "test"}

    entity.increment_version()
    entity.set_metadata("trace", "abc")
    entity.remove_metadata("source")

    assert entity.version == 2
    assert entity.metadata == {"trace": "abc"}


def test_entity_equality_uses_concrete_type_and_identity() -> None:
    identifier = UniqueId.new()
    instant = datetime(2026, 1, 1, tzinfo=UTC)
    first = Entity(id=identifier, clock=FrozenClock(instant))
    second = Entity(id=identifier, clock=FrozenClock(instant))

    assert first == second
    assert hash(first) == hash(second)


def test_entity_rehydrates_and_rejects_invalid_state() -> None:
    identifier = UniqueId.new()
    instant = datetime(2026, 1, 1, tzinfo=UTC)

    entity = Entity.rehydrate(
        id=identifier,
        created_at=instant,
        updated_at=instant,
        version=3,
        metadata={"key": "value"},
    )

    assert entity.id == identifier
    assert entity.version == 3
    with pytest.raises(DomainException):
        Entity(created_at=datetime(2026, 1, 1))
    with pytest.raises(DomainException):
        Entity(clock=FrozenClock(instant), version=0)


def test_domain_event_is_immutable_and_serializable() -> None:
    aggregate_id = UniqueId.new()
    instant = datetime(2026, 1, 1, tzinfo=UTC)
    event = DomainEvent.create(
        aggregate_id=aggregate_id,
        correlation_id=UniqueId.new(),
        causation_id=UniqueId.new(),
        occurred_at=instant,
        version=1,
        metadata={"source": "test"},
        payload={"name": "created"},
    )

    assert event.aggregate_id == aggregate_id
    assert event.to_dict()["occurred_at"] == instant.isoformat()
    with pytest.raises(TypeError):
        cast(MutableMapping[str, object], event.metadata)["source"] = "other"
    with pytest.raises(DomainException):
        DomainEvent.create(
            aggregate_id=aggregate_id,
            correlation_id=UniqueId.new(),
            causation_id=UniqueId.new(),
            occurred_at=datetime(2026, 1, 1),
            version=1,
        )


def test_aggregate_records_pulls_clears_and_publishes_events() -> None:
    instant = datetime(2026, 1, 1, tzinfo=UTC)
    aggregate = AggregateRoot(clock=FrozenClock(instant))
    event = DomainEvent.create(
        aggregate_id=aggregate.id,
        correlation_id=UniqueId.new(),
        causation_id=UniqueId.new(),
        occurred_at=instant,
        version=1,
    )

    aggregate.record_event(event)

    assert aggregate.domain_events == (event,)
    assert aggregate.pull_events() == (event,)
    assert not aggregate.domain_events

    publisher = PublishedEvents()
    aggregate.record_event(event)
    aggregate.publish_events(publisher)

    assert publisher.events == [event]
    assert not aggregate.domain_events
