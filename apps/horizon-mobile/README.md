# Horizon Mobile

Minimal Android/Kotlin Horizon client for following the state of an Asset through Horizon.

## What It Does

- Connects to ELM327 through classic Bluetooth RFCOMM.
- Reads the supported vehicle signals.
- Sends Horizon-compatible readings to the Live Ingestion Gateway.
- Fetches Assets from Horizon.
- Fetches Current State from Horizon.
- Fetches Timeline from Horizon.
- Presents the Asset state in user-facing language.
- Stores Horizon URL, Asset reference, and reading frequency locally.

## What It Does Not Do

- It does not implement domain logic.
- It does not change Horizon Core.
- It does not implement AI.
- It does not implement diagnostics.
- It does not behave as an OBD scanner.
- It does not run as a background service.

## Run

Open this directory in Android Studio:

```text
apps/horizon-mobile
```

Pair the ELM327 adapter on the Realme device before opening the app.

## Horizon Gateway

Run the local Gateway:

```bash
cd services/horizon-gateway
uvicorn app.main:app --reload
```

In Horizon Mobile, configure:

- Horizon URL: `http://<machine-ip>:8000`
- Asset ID or external reference.
- Reading frequency: `1 Hz`, `2 Hz`, or `5 Hz`.

Payloads are still emitted to Logcat for local verification.
