# Capability-006 Result

Status: Draft

## Summary

Implemented the first generic Collector/Ingestion Framework for Horizon.

The framework receives raw external observations, maps them through the Observation Catalog, produces Canonical Observations, and publishes them through an abstract publisher.

## Delivered

- `horizon-collector` package.
- Collector contracts.
- Collector Runtime.
- Collector Session.
- Collector Registry.
- Catalog-backed Observation Mapper.
- Observation Publisher contract.
- In-memory publisher for tests and demos.
- Fake Collector.
- Tests for registry, mapper, publisher, runtime, fake collector, and full pipeline.

## Explicitly Not Delivered

- OBD.
- Bluetooth.
- CAN.
- MQTT.
- REST.
- CSV.
- Serial.
- TCP.
- UDP.
- Hardware.
- Dashboard.
- API.
- Domain changes.
- Application changes.
- Storage changes.
- Timeline changes.
- Current State changes.
- Experience changes.

## Validation

- `python3 -m compileall packages/horizon-collector/src packages/horizon-collector/tests`: passed.
- Smoke pipeline with `PYTHONPATH=packages/horizon-collector/src:packages/horizon-catalog/src`: passed.
- Pipeline output:
  - `engine.rpm` -> `900.0`
  - `engine.temperature` -> `91.0`
  - `electrical.battery_voltage` -> `14.18`
- `python3 -m pytest packages/horizon-collector/tests -q`: blocked because local `python3` has no `pytest` module.
- `.venv` validation: blocked because `.venv` does not exist in this workspace.
- Global `poetry`, `ruff`, `black`, and `mypy`: unavailable in this environment.
