# Android Test Plan

Status: Draft

## Preconditions

- Realme Android device.
- ELM327 Bluetooth adapter.
- Vehicle with OBD-II port.
- Android Studio installed on development machine.
- USB debugging enabled on the Realme device.

## Pair ELM327

1. Plug ELM327 into the vehicle OBD-II port.
2. Turn ignition to accessory mode or start the vehicle.
3. On Realme, open Bluetooth settings.
4. Pair with the ELM327 adapter.
5. Use the adapter PIN if requested, commonly `1234` or `0000`.
6. Confirm the device appears in paired devices.

## Install App

1. Open `apps/android-obd-bridge` in Android Studio.
2. Let Gradle sync.
3. Connect the Realme device over USB.
4. Select the Realme device as the run target.
5. Run the `app` configuration.

## Execute Test

1. Open Horizon OBD Bridge.
2. Grant Bluetooth permission when prompted.
3. Tap `Listar pareados`.
4. Select the ELM327 device.
5. Tap `Conectar`.
6. Wait for `Status: conectado`.
7. Tap `Iniciar leitura`.
8. Confirm RPM, temperature, voltage, and last reading update.
9. Inspect Logcat for tag `HorizonObdBridge`.
10. Confirm JSON payload contains `engine.rpm`, `engine.temperature`, and `electrical.battery_voltage`.

## Expected Payload

```json
{
  "source": "android-obd-elm327",
  "asset_id": null,
  "observations": [
    {
      "definition_id": "engine.rpm",
      "value": 900,
      "unit": "rpm",
      "timestamp": "...",
      "quality": "good"
    }
  ]
}
```

## Known Limitations

- No automatic retry strategy.
- No background service.
- No persistent queue.
- No Horizon API submission yet.
- `HttpSink` is a placeholder.
- Reading is manual, one-shot per tap.
- ELM327 clone firmware quality may vary.
