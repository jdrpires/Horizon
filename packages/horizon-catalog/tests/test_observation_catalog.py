"""Observation catalog tests."""

from horizon_catalog import ValueType, load_vehicle_catalog, validate_value


def test_vehicle_catalog_loads_categories() -> None:
    catalog = load_vehicle_catalog()

    assert "Motor" in catalog.categories
    assert "Elétrica" in catalog.categories
    assert "Combustível" in catalog.categories
    assert "Transmissão" in catalog.categories
    assert "Movimento" in catalog.categories
    assert "Localização" in catalog.categories


def test_lookup_by_id_and_alias() -> None:
    catalog = load_vehicle_catalog()

    assert catalog.get("engine.rpm").label == "RPM do motor"
    assert catalog.find_by_alias("rpm").id == "engine.rpm"


def test_value_type_validation() -> None:
    catalog = load_vehicle_catalog()

    assert validate_value(catalog.get("engine.rpm"), "900") == 900.0
    assert validate_value(catalog.get("fuel.type"), "diesel") == "diesel"


def test_boolean_text_and_datetime_validation() -> None:
    from horizon_catalog.models import ObservationDefinition

    boolean_definition = ObservationDefinition(
        id="test.boolean",
        label="Boolean",
        category="Test",
        unit="state",
        value_type=ValueType.BOOLEAN,
        default_source="manual",
        description="Boolean test.",
    )
    text_definition = ObservationDefinition(
        id="test.text",
        label="Text",
        category="Test",
        unit="text",
        value_type=ValueType.TEXT,
        default_source="manual",
        description="Text test.",
    )
    datetime_definition = ObservationDefinition(
        id="test.datetime",
        label="Datetime",
        category="Test",
        unit="datetime",
        value_type=ValueType.DATETIME,
        default_source="manual",
        description="Datetime test.",
    )

    assert validate_value(boolean_definition, "sim") is True
    assert validate_value(text_definition, "manual") == "manual"
    assert validate_value(datetime_definition, "2026-01-01T08:10:00+00:00")
