import pytest

from horizon_events.context import CorrelationContext, current_context, use_context
from horizon_events.metadata import EventMetadata
from horizon_events.shared import EventName, EventVersion, SchemaVersion, VersionCompatibility


def test_context_vars_propagate_correlation_values_to_metadata() -> None:
    context = CorrelationContext(
        correlation_id="corr-1",
        trace_id="trace-1",
        causation_id="cause-1",
        request_id="request-1",
    )

    with use_context(context):
        metadata = EventMetadata.from_current_context(
            aggregate_id="aggregate-1",
            producer="tests",
            source="unit",
            environment="test",
        )

    assert metadata.correlation_id == "corr-1"
    assert metadata.trace_id == "trace-1"
    assert metadata.causation_id == "cause-1"
    assert metadata.request_id == "request-1"


def test_current_context_creates_context_when_absent() -> None:
    context = current_context()

    assert context.correlation_id
    assert context.trace_id
    assert context.causation_id
    assert context.request_id


def test_event_and_schema_versions_express_compatibility() -> None:
    current = EventVersion(2)
    previous = EventVersion(1)
    schema = SchemaVersion(3)

    assert current.is_compatible_with(previous) == VersionCompatibility.BACKWARD_COMPATIBLE
    assert previous.is_compatible_with(current) == VersionCompatibility.FORWARD_ONLY
    assert schema.is_compatible_with(SchemaVersion(3)) == VersionCompatibility.SAME


def test_versions_and_names_validate_invariants() -> None:
    assert str(EventName("example.created")) == "example.created"
    with pytest.raises(ValueError):
        EventName("")
    with pytest.raises(ValueError):
        EventVersion(0)
    with pytest.raises(ValueError):
        SchemaVersion(0)
