"""JSON storage adapter tests."""

from __future__ import annotations

from pathlib import Path

from horizon_application import (
    ApplicationService,
    GetCurrentStateQuery,
    InMemoryTimelineRepository,
    RegisterAssetCommand,
    RegisterObservationCommand,
)
from horizon_storage import JsonStorageBootstrap, StorageCorruptionError


def test_first_execution_creates_storage_files(tmp_path: Path) -> None:
    result = JsonStorageBootstrap(tmp_path).bootstrap()

    assert result.assets_loaded == 0
    assert result.observations_loaded == 0
    assert result.storage_kind == "JSON"
    assert (tmp_path / "assets.json").read_text(encoding="utf-8") == "[]\n"
    assert (tmp_path / "observations.json").read_text(encoding="utf-8") == "[]\n"
    assert (tmp_path / "metadata.json").exists()


def test_save_and_load_asset_and_observation(tmp_path: Path) -> None:
    first = _service_from_storage(tmp_path)
    asset = first.register_asset(
        RegisterAssetCommand(name="Asset One", category="generic.asset", owner_id="tenant-a")
    ).asset
    observation = first.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="temperature",
            value=23.5,
            unit="celsius",
            source="manual",
            timestamp="2026-01-01T08:10:00+00:00",
        )
    ).observation

    second = _service_from_storage(tmp_path)

    assert second.list_assets()[0].asset_id == asset.asset_id
    assert second.list_observations()[0].observation_id == observation.observation_id


def test_bootstrap_rebuilds_timeline_and_current_state(tmp_path: Path) -> None:
    first = _service_from_storage(tmp_path)
    asset = first.register_asset(
        RegisterAssetCommand(name="Asset One", category="generic.asset", owner_id="tenant-a")
    ).asset
    first.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="rpm",
            value=900,
            unit="rpm",
            source="manual",
            timestamp="2026-01-01T08:10:00+00:00",
        )
    )
    first.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="rpm",
            value=2400,
            unit="rpm",
            source="manual",
            timestamp="2026-01-01T08:11:00+00:00",
        )
    )

    second = _service_from_storage(tmp_path)
    timeline = second.show_timeline()
    current_state = second.get_current_state(GetCurrentStateQuery(asset_id=asset.asset_id))

    assert [entry.value for entry in timeline.entries] == [900.0, 2400.0]
    assert current_state.observation_count == 2
    assert current_state.values[0].value == 2400.0


def test_corrupt_storage_raises_error(tmp_path: Path) -> None:
    JsonStorageBootstrap(tmp_path).bootstrap()
    (tmp_path / "assets.json").write_text("{broken", encoding="utf-8")

    try:
        JsonStorageBootstrap(tmp_path).bootstrap()
    except StorageCorruptionError as exc:
        assert "invalid JSON" in str(exc)
    else:
        raise AssertionError("corrupt storage was accepted")


def _service_from_storage(root: Path) -> ApplicationService:
    """Compose an ApplicationService from JSON storage."""
    bootstrap = JsonStorageBootstrap(root).bootstrap()
    timeline_repository = InMemoryTimelineRepository()
    for observation in bootstrap.observation_repository.list():
        timeline_repository.append_observation(observation)
    return ApplicationService.create_with_repositories(
        repository=bootstrap.asset_repository,
        observation_repository=bootstrap.observation_repository,
        timeline_repository=timeline_repository,
    )
