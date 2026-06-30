# Capability-009 Result

Status: Draft

## Summary

Implemented the Horizon Live Ingestion Gateway and updated Android OBD Bridge to send payloads through an optional real HTTP sink.

The Gateway receives collector payloads at `POST /observations`, validates them against the Observation Catalog, maps entries through the Collector Framework, and publishes Canonical Observations into the existing Application, Storage, Timeline, and Current State pipeline.

## Delivered

- `services/horizon-gateway`.
- FastAPI app factory.
- `POST /observations`.
- Local health check for Android connection testing.
- Pydantic request and response schemas.
- Catalog validation.
- Collector Framework mapping.
- Application publisher.
- JSON Storage persistence through existing repositories.
- Timeline and Current State summary after ingestion.
- Android `HttpSink` real implementation.
- Android Gateway URL configuration.
- Android Asset reference configuration.
- Android Logcat mode preserved.

## Validation

- `python3 -m compileall services/horizon-gateway/app services/horizon-gateway/tests`: passed.
- Functional `TestClient` smoke test: passed with `202 Accepted`, three Observations, three events, three Timeline entries, and three Current State values.
- Functional rejection smoke test: passed with `422 Unprocessable Entity` for unknown Observation definition.
- `python3 -m pytest services/horizon-gateway/tests -q`: blocked because local `python3` does not have `pytest` installed.
- `python3 -m ruff check services/horizon-gateway/app services/horizon-gateway/tests`: blocked because local `python3` does not have `ruff` installed.
- `python3 -m black --check services/horizon-gateway/app services/horizon-gateway/tests`: blocked because local `python3` does not have `black` installed.
- `python3 -m mypy services/horizon-gateway/app services/horizon-gateway/tests`: blocked because local `python3` does not have `mypy` installed.
- `git diff --check`: passed.
- `ANDROID_HOME=/Users/jeanpires/Library/Android/sdk JAVA_HOME=/Applications/Android Studio.app/Contents/jbr/Contents/Home ./gradlew assembleDebug`: passed.
- `ANDROID_HOME=/Users/jeanpires/Library/Android/sdk JAVA_HOME=/Applications/Android Studio.app/Contents/jbr/Contents/Home ./gradlew testDebugUnitTest`: passed.

## Android Artifact

- Debug APK generated at `apps/android-obd-bridge/app/build/outputs/apk/debug/app-debug.apk`.
- APK remains a local build artifact and is not versioned.

## Scope Confirmation

No Horizon Core package was modified for business behavior.

No changes were made to:

- Domain rules.
- Application use case contracts.
- Storage architecture.
- Timeline architecture.
- Current State architecture.
- Collector Framework contracts.
- Observation Catalog definitions.
- Experience Layer behavior.

## Demonstration Status

Local Gateway smoke test was executed.

Real Android-to-Gateway live field demonstration remains pending because it requires the Realme device, ELM327, and local network execution outside this coding environment.
