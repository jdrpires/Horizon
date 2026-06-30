# Field Test 001: Citroën C3 Live OBD Reading

Status: Recorded

## Context

This field test records the first live physical Asset observation performed by Horizon tooling.

The test used:

- Citroën C3
- ELM327 Bluetooth adapter
- Android/Realme device
- Android OBD Bridge

The goal was to confirm that the Android OBD Bridge could connect to a physical ELM327 adapter, read basic OBD-II PIDs, parse the responses, and present observation values without changing Horizon Core.

## Observed Result

The Android OBD Bridge completed the reading and reported:

- RPM: `805 rpm`
- Engine temperature: `76 °C`
- Voltage: `12.31 V`
- Status: `leitura concluída`
- Timestamp: generated during the reading

## Architectural Boundary

The field test preserved the intended architecture:

```text
ELM327 Bluetooth
  ↓
Android OBD Bridge
  ↓
HTTP JSON or local output
  ↓
Future Horizon ingestion boundary
  ↓
Collector Framework
  ↓
Observation Catalog
  ↓
Canonical Observation
```

Bluetooth remained outside Horizon Core.

Android acted as the Bridge.

Horizon Core was not changed to accommodate Bluetooth, Android, ELM327, or OBD-specific behavior.

## Learnings

- The Android Bridge strategy is viable for the first physical integration path.
- The ELM327 adapter responded to the basic PIDs used by the bridge.
- The parser worked for the observed values.
- The next required capability is a Horizon ingestion boundary capable of receiving the Android Bridge JSON payload.

## Next Milestone

Milestone M2: Live Ingestion

Objective:

```text
Android OBD Bridge
  ↓
POST /observations
  ↓
Horizon Gateway
  ↓
Collector Framework
  ↓
Timeline
  ↓
Current State
  ↓
Storage
```
