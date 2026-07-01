# Capability-010 Review

Status: Draft

## Review Scope

Review Horizon Mobile as the first official mobile client for Horizon.

## Architectural Checks

- Horizon Core unchanged.
- Domain unchanged.
- Application behavior unchanged.
- Storage behavior unchanged.
- Observation Catalog unchanged.
- Collector Framework unchanged.
- Bluetooth remains in Android.
- ELM327 remains in Android integration code.
- Gateway exposes query composition only.
- Mobile UI does not implement domain rules.
- Current State is presented as projection, not intelligence.

## Bluetooth Session Stability Fix

Status: Implemented, pending field review

Review scope:

- The selected ELM327 is persisted by name and MAC address.
- Horizon Mobile no longer selects the first paired device automatically.
- Pairing list refresh happens only when the user taps `Listar dispositivos`.
- Reading uses the active RFCOMM socket and does not recreate the socket per PID read.
- Reconnection attempts target the same selected MAC address.
- No fallback to another Bluetooth device is allowed without explicit user action.
- Bluetooth session states are explicit: `DISCONNECTED`, `CONNECTING`, `CONNECTED`, `RECONNECTING`, `READING`, and `ERROR`.

Validation:

- Unit tests cover preserved selection, stable MAC after list changes, same-device read loop, same-MAC reconnect after read failure, and no reconnect to a different device.
- Android unit tests passed with `./gradlew testDebugUnitTest`.

## Review Notes

Pending Chief Software Architect review.
