# Sprint-012 Architectural Decisions

## Observation Value Model

Sprint-012 implements the Observation Catalog without changing the current Observation runtime.

The catalog supports `number`, `text`, `boolean`, `enum`, and `datetime`, but Horizon Lab registers only definitions whose `value_type` is `number`.

Non-numeric catalog definitions are visible in the catalog and unavailable in the current runtime with this message:

```text
🚧 Este tipo de observação já existe no Catálogo, mas ainda não é suportado pelo Runtime atual.
```

The runtime evolution for typed Observation values will happen in a future capability named `Observation Value Model`.

This sprint explicitly does not:

- Encode enum values as numbers.
- Convert text into floats.
- Convert booleans into numbers.
- Change `Observation.value`.
- Change Domain, Application, Storage, Timeline, Current State, Replay, Event Bus, Protocol, or Persistence.
