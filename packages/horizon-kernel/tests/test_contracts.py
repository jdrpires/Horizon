from datetime import UTC, datetime
from typing import cast

from horizon_kernel.contracts import EventDispatcher, Repository, Specification
from horizon_kernel.entities import Entity
from horizon_kernel.events import DomainEvent
from horizon_kernel.ids import UniqueId


class AlwaysSatisfied:
    def is_satisfied_by(self, candidate: Entity) -> bool:
        return candidate.id is not None


class InMemoryRepository:
    def __init__(self) -> None:
        self.entities: dict[UniqueId, Entity] = {}

    def get(self, id: UniqueId) -> Entity | None:
        return self.entities.get(id)

    def save(self, entity: Entity) -> None:
        self.entities[entity.id] = entity

    def delete(self, entity: Entity) -> None:
        self.entities.pop(entity.id, None)


class CollectingDispatcher:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def dispatch(self, event: DomainEvent) -> None:
        self.events.append(event)

    def dispatch_all(self, events: tuple[DomainEvent, ...]) -> None:
        self.events.extend(events)


def test_specification_protocol_accepts_compatible_object() -> None:
    specification: Specification[Entity] = AlwaysSatisfied()
    entity = Entity()

    assert specification.is_satisfied_by(entity)


def test_repository_protocol_accepts_compatible_object() -> None:
    repository: Repository[Entity] = InMemoryRepository()
    entity = Entity()

    repository.save(entity)

    assert repository.get(entity.id) == entity
    repository.delete(entity)
    assert repository.get(entity.id) is None


def test_event_dispatcher_protocol_accepts_compatible_object() -> None:
    dispatcher: EventDispatcher = CollectingDispatcher()
    event = DomainEvent.create(
        aggregate_id=UniqueId.new(),
        correlation_id=UniqueId.new(),
        causation_id=UniqueId.new(),
        occurred_at=datetime(2026, 1, 1, tzinfo=UTC),
        version=1,
    )

    dispatcher.dispatch(event)
    dispatcher.dispatch_all((event,))

    assert cast(CollectingDispatcher, dispatcher).events == [event, event]
