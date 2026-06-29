# ADR-0004: Asset is the Root Aggregate of Horizon

Status: Accepted

## Context

Horizon is a connected-asset intelligence platform. The Engineering Playbook states that the domain is sovereign and that architecture decisions must support the long-term product vision.

The project now needs its first concrete domain aggregate. The obvious automotive term would be `Vehicle`, but that would constrain the platform language before product domains are fully defined.

`ADR-0002` is already assigned to Horizon Kernel Purity, so this Asset decision is recorded as `ADR-0004` to preserve accepted ADR history.

## Decision

Model `Asset` as the root aggregate of Horizon.

Do not model the root aggregate as `Vehicle`.

Asset owns only universal lifecycle, identity, ownership, classification, and configuration concerns. It does not know telemetry, GPS, RPM, fuel, engine, tires, temperature, Digital Twin, Knowledge Engine, API, persistence, or infrastructure details.

## Consequences

- Future domains can reference Asset without becoming automotive-specific.
- Vehicle-specific behavior can be introduced later as a separate domain or specialization.
- Asset remains small and stable.
- Horizon can support non-vehicle connected assets without renaming its root domain language.
- Domain Events become the canonical record of important Asset lifecycle changes.
