# SPEC-0003: Observation

Status: Accepted

## Objective

Define Observation as a factual measurement recorded for an Asset at a specific instant.

Observation represents a fact. It does not represent knowledge, insight, recommendation, telemetry consolidation, Digital Twin state, or Collector behavior.

## Responsibilities

- Reference an existing Asset.
- Capture observation type, value, unit, source, timestamp, and quality.
- Validate measurement shape.
- Emit `ObservationRegistered`.
- Support the in-memory playground vertical slice.

## Value Objects

- `ObservationId`
- `ObservationType`
- `ObservationValue`
- `ObservationUnit`
- `ObservationSource`
- `ObservationTimestamp`
- `ObservationQuality`

## Command

- `RegisterObservation`

## Event

- `ObservationRegistered`

## Invariants

- Observation must reference an Asset.
- Type must be known.
- Value must be finite.
- Unit cannot be blank.
- Source cannot be blank.
- Timestamp must be timezone-aware.
- Timestamp cannot be in the future.

## Flow

```mermaid
flowchart TD
    P["Playground"] --> A["Select Asset"]
    A --> C["RegisterObservationCommand"]
    C --> H["Command Handler"]
    H --> U["RegisterObservationUseCase"]
    U --> R["Asset Repository"]
    R --> O["Observation Aggregate"]
    O --> E["ObservationRegistered"]
    E --> X["EventEnvelope"]
    X --> B["InMemoryEventBus"]
    B --> S["Console Subscriber"]
```

## Events

```mermaid
sequenceDiagram
    participant User
    participant Playground
    participant Application
    participant Observation
    participant EventBus
    User->>Playground: Register Observation
    Playground->>Application: RegisterObservationCommand
    Application->>Observation: RegisterObservation
    Observation-->>Application: ObservationRegistered
    Application->>EventBus: EventEnvelope
    EventBus-->>Playground: Console output
```

## Application Layer

```mermaid
flowchart LR
    M["Mediator"] --> D["Command Dispatcher"]
    D --> V["Validation Pipeline"]
    V --> L["Logging Pipeline"]
    L --> H["RegisterObservationCommandHandler"]
    H --> U["RegisterObservationUseCase"]
```
