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

## Rejected Directions

- No gauges.
- No speedometer UI.
- No dashboard framing.
- No diagnostic status claims.
- No AI, chat, recommendations, or generated conclusions.

## Language

- "Leitura" is preferred over technical observation language in the UI.
- "Conectado ao Horizon" is preferred over Gateway-specific success language.
- Technical OBD/PID language remains internal to the integration code.

