"""Value object tests for Asset."""

from dataclasses import FrozenInstanceError

import pytest

from horizon_domain import (
    AssetClassification,
    AssetConfiguration,
    AssetId,
    AssetIdentity,
    AssetStatus,
    Ownership,
)
from horizon_domain.asset.specifications import can_activate
from horizon_kernel import DomainException


def test_asset_id_serializes_and_is_immutable() -> None:
    asset_id = AssetId.new()

    assert AssetId.from_string(asset_id.to_string()) == asset_id
    assert AssetId.from_dict(asset_id.to_dict()) == asset_id
    with pytest.raises(FrozenInstanceError):
        setattr(asset_id, "value", AssetId.new().value)


def test_identity_classification_and_ownership_validate_blank_values() -> None:
    with pytest.raises(DomainException, match="identity.name cannot be blank"):
        AssetIdentity(" ")
    with pytest.raises(DomainException, match="classification.category cannot be blank"):
        AssetClassification(" ")
    with pytest.raises(DomainException, match="ownership.owner_id cannot be blank"):
        Ownership(" ")


def test_value_objects_round_trip_to_dict() -> None:
    identity = AssetIdentity.from_dict(AssetIdentity("Asset", "external").to_dict())
    classification = AssetClassification.from_dict(AssetClassification("generic.asset", "device").to_dict())
    ownership = Ownership.from_dict(Ownership("owner", "tenant").to_dict())
    configuration = AssetConfiguration.from_dict(AssetConfiguration({"mode": "managed"}).to_dict())

    assert identity.external_reference == "external"
    assert classification.kind == "device"
    assert ownership.tenant_id == "tenant"
    assert configuration.values["mode"] == "managed"


def test_configuration_rejects_other_domain_concepts() -> None:
    for forbidden_key in ("temperature", "rpm", "fuel", "gps", "engine", "tires"):
        with pytest.raises(DomainException, match="belongs to another domain"):
            AssetConfiguration({forbidden_key: "not-here"})


def test_configuration_is_immutable_mapping() -> None:
    configuration = AssetConfiguration({"mode": "managed"})

    with pytest.raises(TypeError):
        configuration.values["mode"] = "manual"  # type: ignore[index]


def test_lifecycle_specification_allows_only_registered_and_inactive() -> None:
    assert can_activate(AssetStatus.REGISTERED)
    assert can_activate(AssetStatus.INACTIVE)
    assert not can_activate(AssetStatus.ACTIVE)
    assert not can_activate(AssetStatus.ARCHIVED)
