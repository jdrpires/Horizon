# Capability-013 Result

Status: Draft

## Summary

Capability-013 introduces a single application state for the selected Asset in Horizon Mobile.

The field issue was caused by mobile state drift: assets were listed correctly, but the selected Asset UUID was not consistently persisted and reused by Current State, Timeline, and observation publishing.

No Horizon Core, Gateway, Domain, Application, Storage, Collector Framework, Observation Catalog, API, or Bluetooth Session Engine behavior was changed.

## Implemented

- `AssetSelectionManager`
- `SessionState`
- `AssetAutoBinder`
- `MobileSettingsAssetSelectionStore`
- `LogcatAssetSelectionLogger`
- Local persistence for:
  - `asset_id`
  - `name`
  - `external_reference`
- Startup restoration of the last selected Asset.
- Auto-selection when Gateway returns exactly one Asset.
- Read blocking when no Asset UUID exists.
- Read blocking when Gateway URL is missing.
- Read blocking when Bluetooth/ELM327 is not connected.
- Current State queries use the selected Asset UUID.
- Timeline queries use the selected Asset UUID.
- Observation publication uses the selected Asset UUID.
- Gateway 422 errors surface the Gateway response message.
- Connection screen diagnostic panel for Bluetooth, ELM327, Gateway, Asset, Current State, Timeline, and Publisher.
- Logcat records Asset and Gateway operations.

## Validation

- `./gradlew testDebugUnitTest`: Passed.
- `./gradlew assembleDebug`: Passed.
- `git diff --check`: Passed.

## APK

Generated at:

`apps/horizon-mobile/app/build/outputs/apk/debug/app-debug.apk`

## Expected Field Fix

The app must no longer produce:

- `GET /assets/null/current-state`
- `GET /assets/null/timeline`
- `POST /observations` with `asset_id: null`

All live calls must use the UUID selected through the Assets screen.
