from collections.abc import MutableMapping
from datetime import UTC, datetime
from typing import cast

import pytest

from horizon_events.envelopes import EventEnvelope
from horizon_events.exceptions import EventSerializationError
from horizon_events.metadata import EventMetadata
from horizon_events.serializers import DictionarySerializer


def make_metadata() -> EventMetadata:
    return EventMetadata.create(
        aggregate_id="aggregate-1",
        producer="tests",
        source="unit",
        environment="test",
        occurred_at=datetime(2026, 1, 1, tzinfo=UTC),
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        tags={"kind": "example"},
    )


def make_envelope(event_name: str = "example.created") -> EventEnvelope:
    return EventEnvelope.create(
        event_name=event_name,
        event={"value": 1},
        metadata=make_metadata(),
        headers={"category": "example"},
        tenant="tenant-a",
        version=2,
        schema_version=3,
    )


def test_metadata_contains_required_identity_origin_and_trace_fields() -> None:
    metadata = make_metadata()

    assert metadata.aggregate_id == "aggregate-1"
    assert metadata.producer == "tests"
    assert metadata.source == "unit"
    assert metadata.environment == "test"
    assert metadata.user_id is None
    assert metadata.tags == {"kind": "example"}
    with pytest.raises(TypeError):
        cast(MutableMapping[str, str], metadata.tags)["kind"] = "other"


def test_metadata_roundtrips_through_primitives() -> None:
    metadata = make_metadata()

    restored = EventMetadata.from_dict(metadata.to_dict())

    assert restored == metadata


def test_metadata_validates_required_fields_and_timezone() -> None:
    with pytest.raises(ValueError):
        EventMetadata.create(
            aggregate_id="",
            producer="tests",
            source="unit",
            environment="test",
        )
    with pytest.raises(ValueError):
        EventMetadata.create(
            aggregate_id="aggregate-1",
            producer="",
            source="unit",
            environment="test",
        )
    with pytest.raises(ValueError):
        EventMetadata.create(
            aggregate_id="aggregate-1",
            producer="tests",
            source="",
            environment="test",
        )
    with pytest.raises(ValueError):
        EventMetadata.create(
            aggregate_id="aggregate-1",
            producer="tests",
            source="unit",
            environment="test",
            occurred_at=datetime(2026, 1, 1),
        )


def test_envelope_contains_transport_fields_and_is_immutable() -> None:
    envelope = make_envelope()

    assert envelope.event_name.value == "example.created"
    assert envelope.event == {"value": 1}
    assert envelope.headers == {"category": "example"}
    assert envelope.trace["trace_id"] == envelope.metadata.trace_id
    assert envelope.correlation["correlation_id"] == envelope.metadata.correlation_id
    assert envelope.causation["causation_id"] == envelope.metadata.causation_id
    assert envelope.tenant == "tenant-a"
    assert envelope.version.value == 2
    assert envelope.schema_version.value == 3
    with pytest.raises(TypeError):
        cast(MutableMapping[str, object], envelope.event)["value"] = 2


def test_envelope_deserialization_requires_event_and_metadata_mappings() -> None:
    with pytest.raises(ValueError):
        EventEnvelope.from_dict({"event_name": "example.created", "event": {}, "version": 1})


def test_dictionary_serializer_roundtrips_envelopes_without_json_dependency() -> None:
    serializer = DictionarySerializer()
    envelope = make_envelope()

    serialized = serializer.serialize(envelope)
    restored = serializer.deserialize(serialized)

    assert restored == envelope


def test_dictionary_serializer_wraps_invalid_payloads() -> None:
    serializer = DictionarySerializer()

    with pytest.raises(EventSerializationError):
        serializer.deserialize({"event_name": "broken"})
