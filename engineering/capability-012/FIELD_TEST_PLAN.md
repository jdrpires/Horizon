# Capability-012 Field Test Plan

Status: Draft

## Objective

Validate that Horizon Mobile keeps a stable Bluetooth RFCOMM session with the ELM327 adapter in the Citroen C3.

## Preconditions

- ELM327 paired with the Realme device.
- Horizon Mobile installed.
- Horizon Gateway reachable from the phone.
- Asset reference configured in Horizon Mobile.
- C3 ignition on or engine running.

## Steps

1. Open Horizon Mobile.
2. Go to `Conexao`.
3. Tap `Listar dispositivos`.
4. Select the ELM327 device.
5. Tap `Selecionar dispositivo`.
6. Confirm that the selected name and MAC address remain visible.
7. Tap `Conectar`.
8. Confirm state moves through `CONNECTING`, `INITIALIZING`, and `CONNECTED`.
9. Tap `Iniciar leitura`.
10. Keep the app reading for at least 5 minutes.
11. Confirm RPM, temperature, and voltage continue updating.
12. Confirm the paired-device list does not refresh during reading.
13. Confirm the selected MAC address does not change.
14. Temporarily interrupt the Bluetooth connection if possible.
15. Confirm reconnection attempts use the same MAC address.
16. Confirm Gateway receives `POST /observations`.
17. Open Current State and Timeline to confirm new readings.

## Evidence To Capture

- Screenshot of selected device and MAC address.
- Screenshot of `READING` state.
- Screenshot of last command and last response.
- Screenshot of reconnect attempts if a disconnect occurs.
- Gateway logs showing observation ingestion.
- Approximate duration of stable reading.

## Acceptance Criteria

- The app does not switch to another Bluetooth device.
- The app does not reopen a socket per PID.
- The app reads continuously for at least 5 minutes.
- If the socket fails, reconnection targets the same MAC address.
- The UI remains responsive when stopping the reading.

## Known Field Risks

- Some ELM327 clones close RFCOMM sockets after inactivity or malformed commands.
- Android battery optimization can affect long-running Bluetooth sessions.
- Vehicle ECU readiness can affect PID availability.
- Gateway network latency may delay Current State refresh but should not force Bluetooth reconnection.
