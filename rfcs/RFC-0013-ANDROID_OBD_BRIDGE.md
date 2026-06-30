# RFC-0013: Android OBD Bridge

Status: Accepted

## Summary

Introduce `apps/android-obd-bridge`, a minimal Android/Kotlin application that runs on a Realme device, connects to an ELM327 adapter through classic Bluetooth RFCOMM, reads selected OBD-II PIDs, and emits Horizon-compatible observation payloads.

The bridge is external to Horizon Core. It collects, converts, and emits JSON. It does not persist data in Horizon and does not implement a Horizon API.

## Context

Capability-007 proved OBD parsing and catalog mapping through a Python spike. Capability-008 moves the Bluetooth execution boundary into the correct runtime: Android.

The bridge exists because local Python cannot responsibly improvise Android Bluetooth behavior. Android owns Bluetooth permissions, paired-device selection, RFCOMM socket lifecycle, and user interaction.

## Goals

- Create a minimal Android/Kotlin app under `apps/android-obd-bridge`.
- List paired Bluetooth devices.
- Select an ELM327 adapter.
- Connect with classic Bluetooth RFCOMM.
- Initialize ELM327 with the approved command sequence.
- Read RPM, coolant temperature, and control module voltage.
- Convert values into Horizon observation payload JSON.
- Display connection status, values, and last reading time.
- Emit payloads through an `ObdObservationSink`.
- Provide `LogcatSink` and a documented `HttpSink` placeholder.

## Non-Goals

- Implement a web dashboard.
- Implement a Horizon API.
- Persist observations in Horizon.
- Change Horizon Core.
- Change Domain, Application, Storage, Timeline, Current State, Experience, Catalog, or Collector Framework.
- Implement domain logic on Android.
- Implement Living Digital Twin, Lyra, AI, or recommendations.

## Architecture

```text
ELM327 Bluetooth
  |
  v
Android OBD Bridge
  |
  v
HTTP JSON or local Logcat output
  |
  v
Future Horizon Ingestion Endpoint
  |
  v
Collector Framework
  |
  v
Observation Catalog
  |
  v
Canonical Observation
```

## Payload Shape

```json
{
  "source": "android-obd-elm327",
  "asset_id": null,
  "observations": [
    {
      "definition_id": "engine.rpm",
      "value": 900,
      "unit": "rpm",
      "timestamp": "2026-06-30T20:00:00Z",
      "quality": "good"
    }
  ]
}
```

## Supported Commands

Initialization:

- `ATZ`
- `ATE0`
- `ATL0`
- `ATS0`
- `ATH0`
- `ATSP0`

PIDs:

- `010C`: `engine.rpm`
- `0105`: `engine.temperature`
- `0142`: `electrical.battery_voltage`

## Compatibility

This RFC is additive. It creates an external app and does not change any Horizon Core package.

The bridge output is designed for a future ingestion endpoint. Until that endpoint exists, the app emits JSON to Logcat.
