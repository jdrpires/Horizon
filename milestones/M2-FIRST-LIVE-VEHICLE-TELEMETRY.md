# Milestone M2

Title: First End-to-End Live Vehicle Telemetry

Status: Recorded

## Objective

Record the first successful end-to-end live telemetry flow from a real vehicle into Horizon memory.

M2 proves that Horizon can receive continuous observations from physical hardware, preserve its architectural boundaries, update Timeline, and project Current State without reducing Horizon Core to a telemetry, Bluetooth, OBD, or mobile-specific system.

## Milestone Description

Horizon executed a complete live hardware test using a Citroën C3, an ELM327 Bluetooth adapter, a Realme Android device running Horizon Mobile, Cloudflare Tunnel, and the Horizon Gateway.

The test validated continuous live observation ingestion over several minutes. The mobile client selected and preserved the correct Asset UUID, sent canonical observations to the Gateway, and allowed Horizon to update Current State and Timeline.

The previously observed mobile state failure was resolved. During the validated run, there were no more calls using `asset_id: null`, no `GET /assets/null`, and no `422 Unprocessable Entity` responses caused by missing Asset identity.

## Validated Architecture

```text
Citroën C3
  |
  v
ELM327 Bluetooth
  |
  v
Android Realme
  |
  v
Horizon Mobile
  |
  v
Cloudflare Tunnel
  |
  v
Horizon Gateway
  |
  v
Collector Framework
  |
  v
Application
  |
  v
Storage
  |
  v
Timeline
  |
  v
Current State
```

## Complete Flow

1. The Citroën C3 produced live OBD-II readings.
2. The ELM327 Bluetooth adapter exposed the readings to Android.
3. Horizon Mobile maintained the Bluetooth session and selected Asset state.
4. Horizon Mobile sent canonical observation payloads through the Gateway.
5. Cloudflare Tunnel exposed the Gateway boundary for field validation.
6. The Gateway accepted live observations.
7. The Collector Framework preserved the ingestion boundary.
8. Application services registered observations.
9. Storage persisted the facts.
10. Timeline grew chronologically.
11. Current State reflected the latest known projection.

## Hardware Used

- Vehicle: Citroën C3 Feel 1.6 AT
- Mobile device: Realme Android
- Adapter: ELM327 Bluetooth
- Client: Horizon Mobile
- Network bridge: Cloudflare Tunnel
- Gateway: Horizon Live Ingestion Gateway

## Results

- Continuous telemetry was observed over several minutes.
- `GET /health` returned `200 OK`.
- `GET /assets` returned `200 OK`.
- `POST /observations` returned `202 Accepted`.
- `GET /current-state` returned `200 OK`.
- `GET /timeline` returned `200 OK`.
- Timeline was updated with live observations.
- Current State was updated from live observations.
- Mobile State Synchronization preserved the selected Asset UUID.
- Bluetooth Session Engine kept the ELM327 session stable enough for the field run.

The test did not produce:

- `asset_id: null`
- `GET /assets/null`
- `422 Unprocessable Entity`

## Evidence Logs

Summarized evidence from the field validation:

```text
GET /health -> 200 OK
GET /assets -> 200 OK
POST /observations -> 202 Accepted
GET /assets/{asset_id}/current-state -> 200 OK
GET /assets/{asset_id}/timeline -> 200 OK

[Asset] Selected asset_id=3662b190-0a62-4e76-829f-86d500d4552c
[Gateway] POST asset_id=3662b190-0a62-4e76-829f-86d500d4552c
[Publisher] Published observations count=...
```

## Lessons Learned

- Asset UUID is not a detail; it is the continuity key for live memory.
- Mobile state must be explicit, restorable, and visible during field validation.
- Bluetooth stability must be treated as a session problem, not as individual command attempts.
- Cloudflare Tunnel is useful for validating real mobile-to-Gateway flows without changing Horizon architecture.
- The Collector Framework boundary remained intact during real hardware ingestion.
- Horizon Mobile is now a client of Horizon, not only an OBD bridge.
- Hardware tests expose state and runtime failures that unit tests alone will not reveal.

## Next Steps

M2 completes the first live vehicle telemetry milestone. The next architectural generation should continue toward:

- Generation 2
- Memory Engine
- Knowledge Engine
- Living Digital Twin Runtime

These future capabilities must derive intelligence from memory. They must not bypass Observation, Timeline, Current State, Asset identity, or explainability.
