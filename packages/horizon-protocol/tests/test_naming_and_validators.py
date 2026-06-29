"""Naming and validation tests."""

import pytest

from horizon_protocol import MessageKind, NamingConvention
from horizon_protocol.validators import (
    validate_category_name,
    validate_identifier_name,
    validate_message_name,
    validate_protocol_version,
    validate_schema_version,
)


@pytest.mark.parametrize(
    ("kind", "name"),
    [
        (MessageKind.COMMAND, "CreateAsset"),
        (MessageKind.COMMAND, "RegisterMaintenance"),
        (MessageKind.COMMAND, "StartJourney"),
        (MessageKind.COMMAND, "FinishJourney"),
        (MessageKind.QUERY, "GetAsset"),
        (MessageKind.QUERY, "ListJourneys"),
        (MessageKind.QUERY, "FindInsights"),
        (MessageKind.EVENT, "JourneyStarted"),
        (MessageKind.EVENT, "JourneyFinished"),
        (MessageKind.EVENT, "InsightGenerated"),
        (MessageKind.EVENT, "MaintenanceScheduled"),
    ],
)
def test_official_message_names_are_valid(kind: MessageKind, name: str) -> None:
    assert validate_message_name(kind, name) == name


@pytest.mark.parametrize(
    ("kind", "name", "reason"),
    [
        (MessageKind.COMMAND, "AssetCreated", "approved verb"),
        (MessageKind.QUERY, "CreateAsset", "read verb"),
        (MessageKind.EVENT, "StartJourney", "past-tense suffix"),
        (MessageKind.EVENT, "journey_started", "PascalCase"),
    ],
)
def test_inconsistent_message_names_are_rejected(
    kind: MessageKind,
    name: str,
    reason: str,
) -> None:
    with pytest.raises(ValueError, match=reason):
        validate_message_name(kind, name)


def test_identifier_and_category_names_follow_protocol_conventions() -> None:
    assert validate_identifier_name("AssetId") == "AssetId"
    assert validate_category_name("journey.lifecycle") == "journey.lifecycle"
    assert validate_category_name("maintenance-planning") == "maintenance-planning"

    with pytest.raises(ValueError, match="end with Id"):
        validate_identifier_name("Asset")
    with pytest.raises(ValueError, match="lowercase"):
        validate_category_name("JourneyLifecycle")


def test_pascal_case_validator_rejects_spaces_and_underscores() -> None:
    assert NamingConvention.ensure_pascal_case("ProtocolMessage") == "ProtocolMessage"
    with pytest.raises(ValueError, match="PascalCase"):
        NamingConvention.ensure_pascal_case("Protocol Message")


def test_version_validators_parse_semantic_versions() -> None:
    assert validate_protocol_version("1.2.3").to_string() == "1.2.3"
    assert validate_schema_version("2.4").to_string() == "2.4.0"

    with pytest.raises(ValueError, match="major.minor"):
        validate_protocol_version("1")
