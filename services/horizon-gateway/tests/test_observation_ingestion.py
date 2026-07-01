"""Live ingestion gateway tests."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.config import GatewaySettings
from app.main import create_app
from horizon_application import (
    ApplicationService,
    GetCurrentStateQuery,
    InMemoryTimelineRepository,
    RegisterAssetCommand,
)
from horizon_storage import JsonStorageBootstrap


def test_post_observations_ingests_payload_and_updates_storage_timeline_and_state(
    tmp_path: Path,
) -> None:
    asset_id = _seed_asset(tmp_path)
    client = _client(tmp_path)

    response = client.post(
        "/observations",
        json={
            "source": "android-obd-elm327",
            "asset_id": asset_id,
            "observations": [
                {
                    "definition_id": "engine.rpm",
                    "value": 805,
                    "unit": "rpm",
                    "timestamp": "2026-06-30T20:00:00+00:00",
                    "quality": "good",
                },
                {
                    "definition_id": "engine.temperature",
                    "value": 76,
                    "unit": "celsius",
                    "timestamp": "2026-06-30T20:00:02+00:00",
                    "quality": "good",
                },
                {
                    "definition_id": "electrical.battery_voltage",
                    "value": 12.31,
                    "unit": "volt",
                    "timestamp": "2026-06-30T20:00:04+00:00",
                    "quality": "good",
                },
            ],
        },
    )

    assert response.status_code == 202
    body = response.json()
    assert body["accepted"] == 3
    assert body["event_count"] == 3
    assert body["timeline_entries"] == 3
    assert body["current_state_values"] == 3

    service = _service_from_storage(tmp_path)
    timeline = service.show_timeline()
    current_state = service.get_current_state(GetCurrentStateQuery(asset_id=asset_id))

    assert [entry.observation_type for entry in timeline.entries] == [
        "rpm",
        "temperature",
        "voltage",
    ]
    assert current_state.observation_count == 3


def test_gateway_query_endpoints_return_assets_current_state_and_timeline(tmp_path: Path) -> None:
    asset_id = _seed_asset(tmp_path, external_reference="citroen-c3")
    client = _client(tmp_path)

    ingest_response = client.post(
        "/observations",
        json={
            "source": "android-obd-elm327",
            "asset_id": "citroen-c3",
            "observations": [
                {
                    "definition_id": "engine.rpm",
                    "value": 805,
                    "unit": "rpm",
                    "timestamp": "2026-06-30T20:00:00+00:00",
                    "quality": "good",
                }
            ],
        },
    )

    assets_response = client.get("/assets")
    state_response = client.get(f"/assets/{asset_id}/current-state")
    timeline_response = client.get("/assets/citroen-c3/timeline")

    assert ingest_response.status_code == 202
    assert assets_response.status_code == 200
    assert state_response.status_code == 200
    assert timeline_response.status_code == 200
    assert assets_response.json()["assets"][0]["external_reference"] == "citroen-c3"
    assert state_response.json()["values"][0]["type"] == "rpm"
    assert timeline_response.json()["entries"][0]["type"] == "rpm"


def test_gateway_query_endpoints_reject_unknown_asset(tmp_path: Path) -> None:
    client = _client(tmp_path)

    state_response = client.get("/assets/unknown/current-state")
    timeline_response = client.get("/assets/unknown/timeline")

    assert state_response.status_code == 404
    assert timeline_response.status_code == 404


def test_post_observations_resolves_existing_asset_external_reference(tmp_path: Path) -> None:
    _seed_asset(tmp_path, external_reference="citroen-c3")
    client = _client(tmp_path)

    response = client.post(
        "/observations",
        json={
            "source": "android-obd-elm327",
            "asset_id": "citroen-c3",
            "observations": [
                {
                    "definition_id": "engine.rpm",
                    "value": 900,
                    "unit": "rpm",
                    "timestamp": "2026-06-30T20:00:00+00:00",
                    "quality": "good",
                }
            ],
        },
    )

    assert response.status_code == 202
    assert response.json()["accepted"] == 1


def test_post_observations_rejects_unknown_catalog_definition(tmp_path: Path) -> None:
    asset_id = _seed_asset(tmp_path)
    client = _client(tmp_path)

    response = client.post(
        "/observations",
        json={
            "source": "android-obd-elm327",
            "asset_id": asset_id,
            "observations": [
                {
                    "definition_id": "missing.signal",
                    "value": 1,
                    "unit": "rpm",
                    "timestamp": "2026-06-30T20:00:00+00:00",
                    "quality": "good",
                }
            ],
        },
    )

    assert response.status_code == 422
    assert "definition_id not found" in response.json()["detail"]


def test_post_observations_rejects_unknown_asset_reference(tmp_path: Path) -> None:
    client = _client(tmp_path)

    response = client.post(
        "/observations",
        json={
            "source": "android-obd-elm327",
            "asset_id": "unknown-asset",
            "observations": [
                {
                    "definition_id": "engine.rpm",
                    "value": 805,
                    "unit": "rpm",
                    "timestamp": "2026-06-30T20:00:00+00:00",
                    "quality": "good",
                }
            ],
        },
    )

    assert response.status_code == 422
    assert "existing Asset" in response.json()["detail"]


def test_post_observations_rejects_unit_mismatch(tmp_path: Path) -> None:
    asset_id = _seed_asset(tmp_path)
    client = _client(tmp_path)

    response = client.post(
        "/observations",
        json={
            "source": "android-obd-elm327",
            "asset_id": asset_id,
            "observations": [
                {
                    "definition_id": "engine.rpm",
                    "value": 805,
                    "unit": "celsius",
                    "timestamp": "2026-06-30T20:00:00+00:00",
                    "quality": "good",
                }
            ],
        },
    )

    assert response.status_code == 422
    assert "unit mismatch" in response.json()["detail"]


def _client(root: Path) -> TestClient:
    app = create_app(GatewaySettings(storage_path=root))
    return TestClient(app)


def _seed_asset(root: Path, external_reference: str | None = None) -> str:
    service = _service_from_storage(root)
    result = service.register_asset(
        RegisterAssetCommand(
            name="Citroen C3",
            category="vehicle",
            owner_id="jean",
            external_reference=external_reference,
        )
    )
    return result.asset.asset_id


def _service_from_storage(root: Path) -> ApplicationService:
    bootstrap = JsonStorageBootstrap(root).bootstrap()
    timeline_repository = InMemoryTimelineRepository()
    for observation in bootstrap.observation_repository.list():
        timeline_repository.append_observation(observation)
    return ApplicationService.create_with_repositories(
        repository=bootstrap.asset_repository,
        observation_repository=bootstrap.observation_repository,
        timeline_repository=timeline_repository,
    )
