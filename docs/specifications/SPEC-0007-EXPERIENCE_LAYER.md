# SPEC-0007: Experience Layer

Status: Accepted

## Objective

Define the first Horizon Experience Layer for user-facing Horizon Lab interaction.

This specification does not alter business rules, domain behavior, application use cases, storage, Timeline, Current State, Replay, Event Bus, Protocol, or persistence semantics.

## Responsibilities

- Render Horizon Lab menus with user-oriented language.
- Prompt with friendly labels.
- Validate terminal input before commands are sent to the Application Layer.
- Keep invalid input from raising `IndexError`, `ValueError`, or `KeyError` to the terminal.
- Allow retry or cancellation.
- Hide UUIDs, aggregates, domain events, event envelopes, trace, correlation, and metadata.
- Present Timeline as readable chronological entries.
- Present Current State as readable latest values.

## Components

- `presenters`
- `formatters`
- `validators`
- `menus`
- `prompts`
- `rendering`
- `exceptions`

`developer_mode` and `profiles` are placeholders only in Sprint-011. They are not implemented as product behavior.

## Language Changes

| Technical label | User label |
| --- | --- |
| Identification | Nome do Asset |
| Classification | Tipo do Asset |
| Owner | Proprietário |
| Type | Tipo da Observação |
| Value | Valor |
| Unit | Unidade |
| Source | Origem |
| Timestamp ISO optional | Data/Hora (opcional) |

## Validation

Invalid inputs must show a helpful error and keep the application running.

Users may type `c`, `cancelar`, `voltar`, or `sair` in forms to return to the menu.

## Current State Presentation

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Citroën C3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status
Registrado

RPM
900 rpm

Temperatura
91 °C

Última atualização
30/06/2026 19:42
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Timeline Presentation

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Linha do tempo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
30/06/2026 19:41
RPM
900 rpm
Manual
---------------------
```

## Non-Goals

- Rich.
- Experience Profiles.
- Developer Mode.
- Living Digital Twin.
- AI.
- Business rules.
- Persistence changes.
