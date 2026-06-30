# SPEC-0013: Horizon Mobile

Status: Accepted

## Objective

Define Horizon Mobile, the first official mobile client for following an Asset through Horizon.

The app reads supported ELM327 values, sends readings to the Horizon Gateway, fetches Current State and Timeline, and presents them without scanner or diagnostic language.

## Package

```text
apps/
  horizon-mobile/
    app/
      src/
        main/
          java/com/codesynergy/horizon/mobile/
            bluetooth/
            elm327/
            model/
            network/
            settings/
            sink/
            ui/
        test/
```

## Screens

- Home.
- Assets.
- Current State.
- Timeline.
- Connection.
- Settings.

## Home

Home shows:

- Asset name.
- Asset status.
- Last update.
- Connection quality.
- Connect action.
- Follow Asset action.

## Current State

Current State shows user-facing groups:

- Motor.
- RPM.
- Temperature.
- Electrical system.
- Last update.

It must not present Current State as intelligence or diagnosis. It is a projection from Timeline.

## Timeline

Timeline shows readings in chronological form:

- Time.
- Reading name.
- Value.
- Source.

## Connection

Connection shows:

- Bluetooth status.
- Horizon status.
- Last sync.
- Sent packets.
- Received packets.
- Latency.

## Settings

Settings stores locally:

- Horizon URL.
- Asset ID or external reference.
- Reading frequency: `1 Hz`, `2 Hz`, `5 Hz`.

## Gateway Endpoints

The app consumes:

```text
GET /assets
GET /assets/{id}/current-state
GET /assets/{id}/timeline
POST /observations
```

## UX Rules

- Use "Leitura" instead of technical Observation framing in the mobile UI.
- Use "Sistema elétrico" instead of voltage-first framing.
- Use "Conectado ao Horizon" instead of Gateway success language.
- Do not use gauges, speedometers, charts, dashboards, or diagnostic framing.
- Do not show PIDs as the main experience.

## Acceptance Criteria

- App is renamed to Horizon Mobile.
- Git history is preserved through `git mv` where possible.
- Android build succeeds.
- Android unit tests pass.
- Gateway query endpoints work.
- Settings persist locally.
- Current State and Timeline can be fetched from Horizon.
- The app keeps ELM327 reading and Observation submission.

