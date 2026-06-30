# RFC-0015: Horizon Mobile

Status: Accepted

## Summary

Evolve the Android OBD Bridge into Horizon Mobile, the first official Horizon client for following the state of an Asset.

Horizon Mobile is not a telemetry screen, not an OBD scanner, and not a diagnostic app. It is an external client that reads from an approved external source, sends factual readings to Horizon, and presents the Asset's Current State and Timeline in human language.

## Context

Capability-008 created the Android OBD Bridge as a minimal Bluetooth/ELM327 bridge. Capability-009 introduced the Live Ingestion Gateway and gave external collectors a local `POST /observations` boundary.

The next step is to close the loop:

```text
Android reads a physical Asset
  |
  v
Gateway ingests Observations
  |
  v
Horizon updates Timeline and Current State
  |
  v
Android presents the Asset state
```

## Goals

- Rename Android OBD Bridge to Horizon Mobile.
- Preserve Git history where possible.
- Keep ELM327 reading behavior.
- Keep Observation submission to Horizon.
- Add Horizon query consumption.
- Show Assets.
- Show Current State.
- Show Timeline.
- Show connection quality.
- Store Horizon URL, Asset reference, and reading frequency locally.
- Replace technical language with user-facing language.

## Non-Goals

- Implement AI.
- Implement chat.
- Implement Living Digital Twin runtime behavior.
- Implement Knowledge.
- Implement diagnostics.
- Implement a web dashboard.
- Implement notifications.
- Implement authentication.
- Change Horizon Core.
- Change Domain, Application, Storage, Catalog, Collector Framework, Timeline, or Current State semantics.

## User Experience Direction

The user should feel they are accompanying the state of the vehicle.

The app must not lead with PIDs, raw OBD vocabulary, gauges, scanner language, or diagnostic framing.

Horizon Mobile presents:

- Asset identity.
- Latest state.
- Timeline memory.
- Connection quality.
- Local settings.

## Gateway Queries

Horizon Mobile consumes:

- `GET /assets`
- `GET /assets/{id}/current-state`
- `GET /assets/{id}/timeline`
- `POST /observations`

These endpoints remain local Gateway boundaries, not a public API commitment.

## Compatibility

Horizon Mobile remains outside Horizon Core.

Bluetooth, ELM327, Android permissions, and mobile UI behavior stay inside the mobile app boundary. Horizon Core continues to receive only canonical Observation payloads and expose projections through the Gateway.

## Validation

The capability is valid when:

- Horizon Mobile builds.
- Existing ELM327 parsing tests pass.
- Gateway endpoint URL normalization is tested.
- Gateway query endpoints are smoke-tested.
- Android can still send readings.
- Current State and Timeline can be fetched from Horizon.

