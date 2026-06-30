# Android OBD Bridge

Minimal Android/Kotlin bridge for reading ELM327 OBD-II values on a Realme device.

## What It Does

- Lists paired Bluetooth devices.
- Connects to ELM327 through classic RFCOMM.
- Initializes the adapter.
- Reads RPM, coolant temperature, and control module voltage.
- Converts readings into Horizon-compatible JSON payloads.
- Emits payloads to Logcat.

## What It Does Not Do

- It does not persist in Horizon.
- It does not call a real Horizon API.
- It does not implement domain logic.
- It does not change Horizon Core.
- It does not run as a background collector.

## Run

Open this directory in Android Studio:

```text
apps/android-obd-bridge
```

Pair the ELM327 adapter on the Realme device before opening the app.

## Logcat

Filter by:

```text
HorizonObdBridge
```

Payloads are emitted by `LogcatSink`.
