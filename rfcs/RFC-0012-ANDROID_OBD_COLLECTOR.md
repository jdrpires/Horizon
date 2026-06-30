# RFC-0012: Android OBD Collector

Status: Accepted

## Summary

Introduce an experimental Android/ELM327 OBD collector adapter as the first real-device-oriented source for Horizon observations.

This capability does not alter Horizon Core. ELM327 Bluetooth is treated strictly as an external source feeding the existing Collector Framework.

## Context

Capability-006 established the generic Collector Framework. The next controlled step is to prove that a transport-specific source can sit outside Horizon Core, read external values, map them through the Observation Catalog, and produce Canonical Observations.

The first source is an ELM327 OBD adapter paired to an Android/Realme device. Bluetooth and OBD remain outside Core.

## Goals

- Create `packages/collector-obd`.
- Define OBD contracts and models.
- Support basic ELM327 initialization commands.
- Support selected OBD PIDs for RPM, coolant temperature, and control module voltage.
- Map OBD PIDs to Observation Catalog definitions.
- Provide `MockObdTransport` for deterministic local validation.
- Provide `AndroidBluetoothTransport` as a documented boundary placeholder.
- Provide `tools/android_obd_probe.py` for mock probing and future Android transport execution.

## Non-Goals

- Build a mobile application.
- Implement production Bluetooth.
- Implement a dashboard.
- Implement Lyra.
- Implement Living Digital Twin behavior.
- Implement API behavior.
- Persist observations automatically.
- Change Horizon Core.
- Change Domain, Application, Storage, Timeline, Current State, Experience, Observation Catalog, or Collector Framework.

## Architecture

```text
ELM327 Bluetooth
  |
  v
Android OBD Collector
  |
  v
Collector Framework
  |
  v
Observation Catalog
  |
  v
Canonical Observation
  |
  v
Horizon Boundary
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

- `010C`: engine RPM.
- `0105`: coolant temperature.
- `0142`: control module voltage.

## PID Mapping

- `010C` -> `engine.rpm`
- `0105` -> `engine.temperature`
- `0142` -> `electrical.battery_voltage`

## Android Bluetooth Boundary

The repository does not include a native Android Bluetooth runtime in this capability.

The Android transport boundary exists as an explicit interface. Real Bluetooth execution requires an approved Android runtime, bridge, or app shell. The project must not improvise local Bluetooth behavior that leaks transport concerns into Horizon Core.

## Validation

The capability is valid when the mock transport can:

- Simulate RPM.
- Simulate coolant temperature.
- Simulate battery/control module voltage.
- Map values to Canonical Observations.
- Publish through the Collector Framework.
