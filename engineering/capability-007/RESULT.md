# Capability-007 Result

Status: Draft

## Summary

Implemented an experimental Android/ELM327 OBD collector adapter as an external source package.

The capability validates the ingestion path with `MockObdTransport` and keeps real Bluetooth behind a documented boundary.

## Delivered

- `packages/collector-obd`.
- ELM327 command definitions.
- OBD PID definitions.
- OBD response parser.
- `ObdTransport` protocol.
- `MockObdTransport`.
- `AndroidBluetoothTransport` placeholder.
- `Elm327Adapter`.
- `ObdObservationMapper`.
- `tools/android_obd_probe.py`.
- Documentation for RFC, ADR, SPEC, notes, result, and review.

## Mock Result

The mock probe maps:

- `010C` -> `engine.rpm` -> `900.0 rpm`
- `0105` -> `engine.temperature` -> `91.0 celsius`
- `0142` -> `electrical.battery_voltage` -> `14.18 volt`

## Explicitly Not Delivered

- Production Bluetooth.
- Mobile application.
- Dashboard.
- Lyra.
- Living Digital Twin.
- API.
- Automatic persistence.
- Horizon Core changes.

## Validation

- `python3 -m compileall packages/collector-obd/src packages/collector-obd/tests tools/android_obd_probe.py`: passed.
- `PYTHONPATH=packages/collector-obd/src:packages/horizon-collector/src:packages/horizon-catalog/src python3 -m unittest discover packages/collector-obd/tests -v`: passed, 8 tests.
- `python3 tools/android_obd_probe.py --transport mock`: passed.
- `git diff --check`: passed.

Mock probe output:

```text
engine.rpm (rpm) = 900.0 rpm source=android-obd-elm327
engine.temperature (temperature) = 91.0 celsius source=android-obd-elm327
electrical.battery_voltage (voltage) = 14.18 volt source=android-obd-elm327
published=3
```

Environment limitations:

- Local Python is 3.12, while project target remains Python 3.13.
- Global `poetry`, `ruff`, `black`, and `mypy` are unavailable in this environment.
- Real Android Bluetooth execution is intentionally not implemented in this capability.
