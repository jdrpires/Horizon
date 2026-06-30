# Android OBD Notes

Status: Draft

## Realme Pairing Steps

1. Plug the ELM327 adapter into the vehicle OBD-II port.
2. Turn the vehicle ignition to accessory or engine-on mode.
3. On the Realme device, open Bluetooth settings.
4. Pair with the ELM327 adapter.
5. Try common PINs only if required by the adapter, usually `1234` or `0000`.
6. Record the paired device name and address.
7. Keep the adapter powered while probing.

## Local Mock Probe

Run:

```bash
python tools/android_obd_probe.py --transport mock
```

Expected output includes:

```text
engine.rpm
engine.temperature
electrical.battery_voltage
published=3
```

## Android Probe Notes

The command shape for future Android Bluetooth execution is:

```bash
python tools/android_obd_probe.py --transport android-bluetooth --device-address <ELM327_ADDRESS>
```

The current capability intentionally raises an explicit unavailable-transport error because there is no approved native Android Bluetooth runtime in this repository.

## Limitations

- No native Android Bluetooth bridge is implemented.
- No mobile app is created.
- No automatic persistence is performed.
- No Horizon Core package is changed.
- No dashboard, API, Twin, Lyra, or AI behavior is implemented.

## Next Technical Decisions

- Decide whether Bluetooth execution will happen in a native Android app, Termux/Python bridge, or another approved runtime.
- Define permission handling for Android Bluetooth.
- Define secure device selection and reconnection behavior.
- Define operational logging and correlation once real transport exists.
