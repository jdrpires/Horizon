# Capability-010 Result

Status: Draft

## Summary

Renamed Android OBD Bridge to Horizon Mobile and added the first client experience for Assets, Current State, Timeline, Connection, and Settings.

The app continues reading ELM327 values, continues sending readings to Horizon, and now queries Horizon for the Asset state and Timeline.

## Structure Created

- `apps/horizon-mobile`.
- `apps/horizon-mobile/app/src/main/java/com/codesynergy/horizon/mobile/network`.
- `apps/horizon-mobile/app/src/main/java/com/codesynergy/horizon/mobile/settings`.
- `apps/horizon-mobile/app/src/main/java/com/codesynergy/horizon/mobile/model/HorizonModels.kt`.
- `services/horizon-gateway/app/api/assets.py`.
- `services/horizon-gateway/app/schemas/queries.py`.
- `services/horizon-gateway/app/services/queries.py`.

## Screens Implemented

- Home.
- Assets.
- Current State.
- Timeline.
- Connection.
- Settings.

## Endpoints Used

- `POST /observations`.
- `GET /assets`.
- `GET /assets/{id}/current-state`.
- `GET /assets/{id}/timeline`.
- `GET /health`.

## Validation

- Gate passed after branch creation.
- `python3 -m compileall services/horizon-gateway/app services/horizon-gateway/tests`: passed.
- Python line-length check for new Gateway files: passed.
- `git diff --check`: passed.
- Gateway query smoke test: passed.
- Android `assembleDebug`: passed.
- Android `testDebugUnitTest`: passed.
- `python3 -m pytest services/horizon-gateway/tests -q`: blocked because local `python3` does not have `pytest` installed.
- `python3 -m ruff check services/horizon-gateway/app services/horizon-gateway/tests`: blocked because local `python3` does not have `ruff` installed.
- `python3 -m black --check services/horizon-gateway/app services/horizon-gateway/tests`: blocked because local `python3` does not have `black` installed.
- `python3 -m mypy services/horizon-gateway/app services/horizon-gateway/tests`: blocked because local `python3` does not have `mypy` installed.

## Android Artifact

- Debug APK generated at `apps/horizon-mobile/app/build/outputs/apk/debug/app-debug.apk`.
- APK remains a local build artifact and is not versioned.

## Screenshots

Actual device or emulator screenshots were not produced in this environment because no running Android device/emulator was available through the workspace.

The APK was built successfully and is available locally as a debug artifact.

## Limitations

- Full C3 field demonstration requires Realme, ELM327, vehicle, and local network execution.
- No background service.
- No notifications.
- No authentication.
- No offline synchronization queue.
- Current UI is programmatic Android Views.
