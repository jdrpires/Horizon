# Mobile State Synchronization

Status: Draft

## Objective

Define a single source of truth for Horizon Mobile runtime state during field collection.

This document covers only the mobile application boundary. Horizon Core, Gateway, Domain, Application, Storage, Collector Framework, Observation Catalog, APIs, and the Bluetooth Session Engine remain unchanged.

## State Model

`SessionState` centralizes:

- `gatewayUrl`
- `selectedAssetId`
- `selectedAssetName`
- `selectedAssetExternalReference`
- `selectedBluetoothDeviceName`
- `selectedBluetoothDeviceAddress`
- `bluetoothStatus`
- `gatewayStatus`
- `readingStatus`
- `lastObservation`
- `lastError`

Screens read from this state instead of rebuilding decisions from independent local fields.

## Asset Binding

`AssetSelectionManager` remains responsible for persisted Asset identity.

`AssetAutoBinder` applies the field-test rule:

- `GET /assets` returns 0 Assets: no selection, friendly message.
- `GET /assets` returns 1 Asset: auto-select and persist UUID.
- `GET /assets` returns multiple Assets: require explicit user selection.

## Gateway Health

Gateway status is represented by:

- `UNKNOWN`
- `CHECKING`
- `OK`
- `ERROR`

The `Testar Horizon` action updates `SessionState`. The app may also run the health check on startup when a Gateway URL is configured.

## Live Collection Guard

`Iniciar leitura` is blocked when:

- Gateway URL is missing.
- Asset UUID is missing.
- Bluetooth is not connected.
- ELM327 has not been initialized.

No `POST /observations` is attempted without a selected Asset UUID.

## Diagnostic Panel

The Connection screen shows:

- Bluetooth
- ELM327
- Gateway
- Asset
- Current State
- Timeline
- Publisher

Each item displays a simple status: `OK`, `Pendente`, or `Erro`.

## Logging

Expected Logcat messages:

- `[Session] Session restored`
- `[Asset] Assets loaded`
- `[Asset] Asset auto-selected`
- `[Asset] Asset selected`
- `[Asset] Asset changed`
- `[Asset] Selected asset_id=...`
- `[Gateway] GET /assets`
- `[Gateway] GET current-state asset_id=...`
- `[Gateway] GET timeline asset_id=...`
- `[Gateway] POST asset_id=...`
- `[Gateway] 422 body=...`
- `[Publisher] Skipped POST because asset_id is null`
- `[Publisher] Published observations count=...`

## Expected Outcome

The app must never call:

- `GET /assets/null/current-state`
- `GET /assets/null/timeline`

The app must never send:

- `"asset_id": null`
- Asset name as `asset_id`
- `external_reference` as `asset_id`

Only the selected Asset UUID is valid for live calls.
