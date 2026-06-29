"""Registry tests."""

import pytest

from horizon_protocol import (
    AssetId,
    CategoryRegistry,
    CommandDescriptor,
    CommandRegistry,
    EventReferenceDescriptor,
    EventRegistry,
    IdentifierRegistry,
    ProtocolVersion,
    QueryDescriptor,
    QueryRegistry,
    SchemaDescriptor,
    SchemaRegistry,
    SchemaVersion,
)


def test_command_query_event_and_schema_registries_store_valid_descriptors() -> None:
    protocol_version = ProtocolVersion(1, 0, 0)
    schema_version = SchemaVersion(1, 0, 0)
    commands = CommandRegistry()
    queries = QueryRegistry()
    events = EventRegistry()
    schemas = SchemaRegistry()

    command = commands.register(
        CommandDescriptor("CreateAsset", protocol_version, schema_version, "asset")
    )
    query = queries.register(QueryDescriptor("GetAsset", protocol_version, schema_version, "asset"))
    event = events.register(
        EventReferenceDescriptor("JourneyStarted", protocol_version, schema_version, "journey")
    )
    schema = schemas.register(SchemaDescriptor("AssetSnapshot", schema_version, {"asset_id": "uuid"}))

    assert commands.require("CreateAsset") == command
    assert queries.require("GetAsset") == query
    assert events.require("JourneyStarted") == event
    assert schemas.require("AssetSnapshot") == schema
    assert commands.names() == ("CreateAsset",)


def test_registries_reject_duplicates_and_unknown_required_items() -> None:
    registry = CategoryRegistry()

    registry.register("asset")
    with pytest.raises(ValueError, match="already registered"):
        registry.register("asset")
    with pytest.raises(ValueError, match="not registered"):
        registry.require("journey")


def test_identifier_and_category_registries_validate_names() -> None:
    identifiers = IdentifierRegistry()
    categories = CategoryRegistry()

    registration = identifiers.register("AssetId", AssetId)
    category = categories.register("journey.lifecycle")

    assert registration.identifier_type is AssetId
    assert category == "journey.lifecycle"

    with pytest.raises(ValueError, match="end with Id"):
        identifiers.register("Asset", AssetId)
    with pytest.raises(ValueError, match="lowercase"):
        categories.register("Journey")
