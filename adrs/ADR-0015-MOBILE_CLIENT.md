# ADR-0015: Mobile Client

Status: Accepted

## Context

The Android OBD Bridge proved that Android can safely own Bluetooth/ELM327 execution while Horizon Core remains independent from hardware and transport details.

The Live Ingestion Gateway now allows Android to send readings into Horizon and query projections back.

The project needs its first official client without converting Horizon into a telemetry dashboard or OBD scanner.

## Decision

Rename `apps/android-obd-bridge` to `apps/horizon-mobile` using `git mv`.

Horizon Mobile remains an external Android/Kotlin app. It owns Android UI, Bluetooth selection, ELM327 reads, local settings, and HTTP communication with the Gateway.

The Gateway receives additional read-only endpoints for Assets, Current State, and Timeline. These endpoints compose existing Application behavior and do not alter Domain, Storage, Timeline, Current State, Catalog, or Collector Framework semantics.

## Consequences

- The mobile app becomes the first official Horizon client.
- The app presents the Asset state rather than raw OBD details.
- Historical Android OBD Bridge documents remain valid as prior capability history.
- Horizon Core remains free of Android, Bluetooth, ELM327, and UI concerns.
- The Gateway becomes the local boundary for both ingestion and projection queries.
- Real screenshots and full field demonstration require a Realme/ELM327 runtime.

