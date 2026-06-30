# Capability-008 Result

Status: Draft

## Summary

Created the minimal Android OBD Bridge app in Kotlin.

The app lists paired Bluetooth devices, connects to ELM327 through classic RFCOMM, initializes the adapter, reads selected PIDs, converts responses into Horizon-compatible observation payload JSON, displays readings, and emits payloads to Logcat.

## Delivered

- `apps/android-obd-bridge`.
- Kotlin Android project.
- Classic Bluetooth RFCOMM boundary.
- ELM327 initialization command sequence.
- PID parser.
- PID-to-observation mapper.
- Minimal UI.
- `ObdObservationSink`.
- `LogcatSink`.
- `HttpSink` placeholder.
- Unit-testable parser and payload encoder.
- Android/Realme test plan.

## Commands

- `ATZ`
- `ATE0`
- `ATL0`
- `ATS0`
- `ATH0`
- `ATSP0`
- `010C`
- `0105`
- `0142`

## Payload

The bridge emits:

```json
{
  "source": "android-obd-elm327",
  "asset_id": null,
  "observations": []
}
```

## Validation

- `git diff --check`: passed.
- Scope check: no changes in Horizon Core packages.
- `gradle -v`: unavailable in this environment.
- `kotlinc -version`: unavailable in this environment.
- Android build/test execution must be performed in Android Studio or an environment with Android SDK, Gradle, and Kotlin installed.

## Local Scope Confirmation

No changes were made to:

- Domain.
- Application.
- Storage.
- Timeline.
- Current State.
- Experience.
- Catalog.
- Collector Framework.

## Build Notes

Open `apps/android-obd-bridge` in Android Studio and run:

```text
Gradle sync
app:testDebugUnitTest
app:installDebug
```

The local Codex environment does not include Android SDK or Gradle.
