# ADR-0013: Android OBD Bridge Boundary

Status: Accepted

## Context

ELM327 Bluetooth execution belongs to the Android runtime, not Horizon Core.

Horizon needs a real-device bridge that can interact with Android paired devices, permissions, and RFCOMM sockets while preserving the established Collector boundary.

## Decision

Create `apps/android-obd-bridge` as an external Android/Kotlin application.

The bridge owns Android Bluetooth interaction, ELM327 command execution, PID parsing, UI state, and JSON payload emission. It does not import or alter Horizon Core code. It does not implement domain rules.

The active sink is `LogcatSink`. `HttpSink` exists only as a placeholder until a Horizon ingestion endpoint is approved.

## Consequences

- Android-specific Bluetooth concerns remain outside Core.
- OBD values are converted into Horizon-compatible JSON without persistence.
- The app can be tested on a Realme device with a paired ELM327 adapter.
- Future API ingestion work has a clear contract to consume.
- Production Bluetooth hardening remains future work.
