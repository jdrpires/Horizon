from uuid import UUID

from horizon_kernel.ids import UniqueId


def test_unique_id_can_be_generated_and_serialized() -> None:
    identifier = UniqueId.new()

    assert UUID(identifier.to_string()) == identifier.value


def test_unique_id_can_be_recreated_from_string() -> None:
    identifier = UniqueId.new()

    recreated = UniqueId.from_string(identifier.to_string())

    assert recreated == identifier
    assert str(recreated) == identifier.to_string()
