# Capability-010 UX Decisions

Status: Draft

## Direction

Horizon Mobile should feel like a companion for the Asset state, not a scanner.

The first version uses plain Android Views and Material-style platform components to avoid introducing UI dependencies before the mobile client boundary stabilizes.

## Decisions

- The app name is Horizon Mobile.
- The first screen is Home, centered on the Asset.
- The Current State screen groups readings by user meaning.
- RPM is presented as engine operation.
- Voltage is presented as electrical system state.
- Timeline is presented as memory of readings.
- Connection details are present but not the primary experience.
- Settings are local and explicit.
- Bluetooth device selection is explicit and sticky by MAC address.
- Paired Bluetooth devices are listed only on user request.
- The selected ELM327 remains fixed until the user taps `Trocar dispositivo`.
- Connection UI shows selected device, MAC address, Bluetooth state, last reading, reconnect attempts, and readable errors.

## Bluetooth Session Stability Fix

The field test showed that frequent Bluetooth list refresh and first-device fallback made the live session unstable.

The UX now treats ELM327 selection as an explicit setup action:

1. User taps `Listar dispositivos`.
2. User chooses the ELM327.
3. User taps `Selecionar dispositivo`.
4. Horizon Mobile stores the device name and MAC address.
5. Connection and reconnection use only that MAC address.
6. The app updates readings without refreshing the paired-device list.

The user can change devices only through `Trocar dispositivo`, which clears the persisted Bluetooth selection and asks for a new explicit selection.

## Rejected Directions

- No gauges.
- No speedometer UI.
- No dashboard framing.
- No diagnostic status claims.
- No AI, chat, recommendations, or generated conclusions.
- No automatic first-device selection.
- No automatic device switching during a reading session.

## Language

- "Leitura" is preferred over technical observation language in the UI.
- "Conectado ao Horizon" is preferred over Gateway-specific success language.
- Technical OBD/PID language remains internal to the integration code.
