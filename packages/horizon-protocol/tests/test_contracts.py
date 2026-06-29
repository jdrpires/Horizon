"""Contract value tests."""

from datetime import UTC, datetime

import pytest

from horizon_protocol import (
    AggregateReference,
    AssetId,
    CorrelationId,
    CorrelationReference,
    EntityReference,
    EventId,
    EnvelopeReference,
    MessageHeader,
    MessageKind,
    ModuleId,
    ProtocolMetadata,
    ProtocolVersion,
    SchemaVersion,
    TenantId,
    UserId,
)


def test_message_header_carries_protocol_versions_and_correlation() -> None:
    header = MessageHeader(
        message_name="CreateAsset",
        message_kind=MessageKind.COMMAND,
        protocol_version=ProtocolVersion(1, 0, 0),
        schema_version=SchemaVersion(1, 0, 0),
        correlation_id=CorrelationId.new(),
        metadata=ProtocolMetadata(
            tenant_id=TenantId.new(),
            user_id=UserId.new(),
            module_id=ModuleId.new(),
            attributes={"source": "test"},
        ),
    )

    assert header.message_name == "CreateAsset"
    assert header.occurred_at.tzinfo is UTC
    assert header.metadata.attributes == {"source": "test"}


def test_message_header_rejects_invalid_name_for_kind() -> None:
    with pytest.raises(ValueError, match="approved verb"):
        MessageHeader(
            message_name="JourneyStarted",
            message_kind=MessageKind.COMMAND,
            protocol_version=ProtocolVersion(1, 0, 0),
            schema_version=SchemaVersion(1, 0, 0),
            correlation_id=CorrelationId.new(),
        )


def test_message_header_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        MessageHeader(
            message_name="CreateAsset",
            message_kind=MessageKind.COMMAND,
            protocol_version=ProtocolVersion(1, 0, 0),
            schema_version=SchemaVersion(1, 0, 0),
            correlation_id=CorrelationId.new(),
            occurred_at=datetime(2026, 1, 1),
        )


def test_references_do_not_import_domain_models() -> None:
    asset_id = AssetId.new()
    event_id = EventId.new()
    schema_version = SchemaVersion(1, 0, 0)

    aggregate = AggregateReference("Asset", asset_id)
    entity = EntityReference("Asset", asset_id)
    envelope = EnvelopeReference(event_id, "JourneyStarted", schema_version)
    correlation = CorrelationReference(CorrelationId.new())

    assert aggregate.aggregate_id == asset_id
    assert entity.entity_type == "Asset"
    assert envelope.schema_version == schema_version
    assert correlation.causation_id is None
