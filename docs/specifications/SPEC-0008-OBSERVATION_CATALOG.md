# SPEC-0008: Observation Catalog

Status: Accepted

## Objective

Define the first official Observation Catalog for Horizon.

The catalog is a reusable capability and does not alter Domain, Application, Storage, Timeline, Replay, Current State, Event Bus, Protocol, Persistence, Twin, AI, Collector, or API behavior.

## Model

`ObservationDefinition` contains:

- `id`
- `label`
- `category`
- `unit`
- `value_type`
- `default_source`
- `description`
- `aliases`
- `enabled`
- `display_order`

The implementation also supports `enum_values` for enum validation.

## Value Types

- `number`
- `text`
- `boolean`
- `enum`
- `datetime`

## Vehicle Profile

Categories:

- Motor
- Elétrica
- Combustível
- Transmissão
- Movimento
- Localização

Definitions include RPM, engine temperature, oil pressure, battery voltage, alternator voltage, fuel type, fuel level, consumption, gear, speed, odometer, latitude, longitude, and altitude.

## Horizon Lab Flow

```text
Registrar Observação
Selecionar Asset
Selecionar Categoria
Selecionar Observação
Informar Valor
Observação registrada
```

Horizon Lab must not ask users to type Observation type, unit, source, or timestamp.

## Runtime Compatibility

Only `number` definitions are registered by Horizon Lab in Sprint-012.

For `text`, `boolean`, `enum`, and `datetime`, Horizon Lab shows:

```text
🚧 Este tipo de observação já existe no Catálogo, mas ainda não é suportado pelo Runtime atual.
```

## Invariants

- Catalog definitions are immutable.
- Lookup by ID and alias must be deterministic.
- Category listing must follow display order.
- Catalog package must not depend on Domain or Experience.
- Non-numeric values must not be converted into numbers.
