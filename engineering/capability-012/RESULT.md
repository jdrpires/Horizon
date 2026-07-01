# Capability-012 Result

Status: Draft

## Summary

Capability-012 introduced a Bluetooth Session Engine in Horizon Mobile to stabilize ELM327 RFCOMM communication.

The implementation keeps Bluetooth inside the mobile boundary and preserves the Horizon architecture. The Core, Gateway, Domain, Application, Storage, Catalog, Collector Framework, and APIs were not changed.

## Implemented

- `BluetoothSessionEngine`
- `BluetoothConnectionManager`
- `RfcommSocketSession`
- `Elm327Protocol`
- `PidPollingLoop`
- `ObservationPublisher`
- Logcat logger with tag `HorizonBluetooth`
- Explicit session states
- Same-MAC reconnection
- Backoff reconnection
- UI connection diagnostics
- Unit tests for the new engine

## Session Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Horizon Mobile UI
    participant Engine as BluetoothSessionEngine
    participant ELM as ELM327
    participant Gateway as Horizon Gateway

    User->>UI: Select ELM327 by MAC
    UI->>Engine: Connect
    Engine->>ELM: ATZ / ATE0 / ATL0 / ATS0 / ATH0 / ATSP0
    ELM-->>Engine: Valid responses
    UI->>Engine: Start reading
    loop Reading cycle
        Engine->>ELM: 010C
        ELM-->>Engine: RPM response
        Engine->>ELM: 0105
        ELM-->>Engine: Temperature response
        Engine->>ELM: 0142
        ELM-->>Engine: Voltage response
        Engine->>Gateway: POST /observations
    end
```

## Validation

- `./gradlew testDebugUnitTest`: Passed.
- `./gradlew assembleDebug`: Passed.

## APK

Generated at:

`apps/horizon-mobile/app/build/outputs/apk/debug/app-debug.apk`

## Notes

The engine treats Bluetooth read failures separately from Gateway publication failures. A Gateway error does not force a Bluetooth reconnect.
