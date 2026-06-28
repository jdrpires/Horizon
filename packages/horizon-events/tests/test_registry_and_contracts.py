from horizon_events.contracts import (
    DeadLetterPublisher,
    DeadLetterStore,
    EventBus,
    EventDispatcher,
    EventPublisher,
    EventSerializer,
    EventStore,
    EventStream,
    SnapshotStore,
)
from horizon_events.dispatchers import InMemoryEventDispatcher
from horizon_events.envelopes import EventEnvelope
from horizon_events.event_bus import InMemoryEventBus
from horizon_events.publishers import InMemoryEventPublisher
from horizon_events.registry import EventRegistry
from horizon_events.serializers import DictionarySerializer

from .test_envelope_metadata_serialization import make_envelope


def test_registry_registers_event_schema_handler_and_category() -> None:
    registry = EventRegistry()
    handled: list[str] = []

    def handler(envelope: EventEnvelope) -> None:
        handled.append("handled")

    registration = registry.register(
        event_name="example.created",
        version=2,
        schema_version=1,
        schema={"type": "object"},
        category="example",
        handler=handler,
    )

    resolved = registry.resolve_handler(make_envelope())
    assert registration.category == "example"
    assert registry.get("example.created", 2) == registration
    assert registry.list() == (registration,)
    assert resolved is handler


def test_registry_decorator_registers_handler() -> None:
    registry = EventRegistry()

    @registry.handler(
        event_name="example.created",
        version=2,
        schema_version=1,
        schema={"type": "object"},
        category="example",
    )
    def handle(_envelope: EventEnvelope) -> None:
        return None

    registration = registry.get("example.created", 2)

    assert registration is not None
    assert registration.handler is handle
    registry.clear()
    assert registry.list() == ()


def test_implemented_classes_satisfy_public_protocols() -> None:
    bus: EventBus = InMemoryEventBus()
    dispatcher: EventDispatcher = InMemoryEventDispatcher()
    publisher: EventPublisher = InMemoryEventPublisher(InMemoryEventBus())
    serializer: EventSerializer = DictionarySerializer()

    assert bus is not None
    assert dispatcher is not None
    assert publisher is not None
    assert serializer is not None


class MemoryStore:
    def __init__(self) -> None:
        self.envelopes: list[EventEnvelope] = []

    def append(self, envelope: EventEnvelope) -> None:
        self.envelopes.append(envelope)

    def append_many(self, envelopes: tuple[EventEnvelope, ...]) -> None:
        self.envelopes.extend(envelopes)

    def read(self, stream_name: str) -> tuple[EventEnvelope, ...]:
        return tuple(self.envelopes)


class MemoryStream:
    def __init__(self) -> None:
        self.events: list[EventEnvelope] = []

    @property
    def name(self) -> str:
        return "stream"

    def append(self, envelope: EventEnvelope) -> None:
        self.events.append(envelope)

    def read(self) -> tuple[EventEnvelope, ...]:
        return tuple(self.events)


class MemorySnapshotStore:
    def __init__(self) -> None:
        self.snapshot: dict[str, object] | None = None

    def save(self, stream_name: str, version: int, snapshot: dict[str, object]) -> None:
        self.snapshot = {"stream_name": stream_name, "version": version, "snapshot": snapshot}

    def load(self, stream_name: str) -> dict[str, object] | None:
        return self.snapshot


class MemoryDeadLetter:
    def __init__(self) -> None:
        self.failed: list[tuple[EventEnvelope, str]] = []

    def publish_failed(self, envelope: EventEnvelope, reason: str) -> None:
        self.failed.append((envelope, reason))

    def append_failed(self, envelope: EventEnvelope, reason: str) -> None:
        self.failed.append((envelope, reason))


def test_future_infrastructure_contracts_are_protocol_compatible() -> None:
    store: EventStore = MemoryStore()
    stream: EventStream = MemoryStream()
    snapshots: SnapshotStore = MemorySnapshotStore()
    dead_letter_publisher: DeadLetterPublisher = MemoryDeadLetter()
    dead_letter_store: DeadLetterStore = MemoryDeadLetter()
    envelope = make_envelope()

    store.append(envelope)
    stream.append(envelope)
    snapshots.save("stream", 1, {"state": "ok"})
    dead_letter_publisher.publish_failed(envelope, "failed")
    dead_letter_store.append_failed(envelope, "failed")

    assert store.read("stream") == (envelope,)
    assert stream.read() == (envelope,)
    assert snapshots.load("stream") == {
        "stream_name": "stream",
        "version": 1,
        "snapshot": {"state": "ok"},
    }
