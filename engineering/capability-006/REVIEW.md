# Capability-006 Review

Status: Draft

## Review Scope

Review the Collector Framework as an isolated ingestion capability.

## Architectural Checks

- Collector does not implement OBD.
- Collector does not implement Bluetooth.
- Collector does not implement hardware.
- Collector does not alter Domain.
- Collector does not alter Application.
- Collector does not alter Storage.
- Collector does not alter Timeline.
- Collector does not alter Current State.
- Collector does not alter Experience.
- Collector normalizes external keys through the Observation Catalog.
- Collector publishes Canonical Observations through a boundary.

## Review Notes

Pending Chief Software Architect review.
