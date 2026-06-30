# ADR-0012: OBD Collector Boundary

Status: Accepted

## Context

Horizon needs its first real-device-oriented collector experiment without compromising the Collector Framework boundary established in ADR-0011.

OBD, ELM327, Bluetooth, Android permissions, pairing, socket lifecycle, and device behavior are integration concerns. They must not enter Horizon Core, Domain, Application, Storage, Timeline, Current State, Experience, Observation Catalog, or the generic Collector Framework.

## Decision

Create `collector-obd` as a separate adapter package.

The package owns ELM327 commands, OBD PID parsing, OBD transport contracts, mock transport, Android Bluetooth placeholder, PID-to-catalog mapping, and the experimental probe script.

`collector-obd` may depend on `horizon-collector` and `horizon-catalog`. Horizon Core packages must not depend on `collector-obd`.

Bluetooth real execution is not implemented in this capability. It remains behind `AndroidBluetoothTransport` until an approved Android runtime or bridge is designed.

## Consequences

- OBD is treated as an external data source.
- Bluetooth remains outside Horizon Core.
- Mock execution can validate the ingestion path locally.
- Android/Realme limitations are documented without inventing unsupported runtime behavior.
- Future production Bluetooth work has a clean boundary and must receive its own decision if it introduces native runtime concerns.
