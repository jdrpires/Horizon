# Changelog

## Unreleased

- Rename Android OBD Bridge to Horizon Mobile and add client screens for Assets, Current State, Timeline, Connection, and Settings.
- Add Capability-009 Live Ingestion Gateway for local `POST /observations`.
- Update Android OBD Bridge with configurable HTTP sink for Gateway ingestion.
- Record Milestone M1: First Live Observation with Citroën C3, ELM327, and Android OBD Bridge.
- Add Capability-008 Android OBD Bridge app.
- Add Capability-007 Android/ELM327 OBD Collector Spike.
- Add Capability-006 Collector Framework for generic observation ingestion.
- Add Sprint-012 Observation Catalog capability.
- Add Vehicle Observation catalog and catalog-driven Horizon Lab Observation flow.
- Add Sprint-011 Experience Layer for user-friendly Horizon Lab interaction.
- Hide technical Horizon Lab details from normal user output.
- Add validation loops for Horizon Lab terminal input.
- Add Sprint-010 JSON persistence layer for Asset and Observation facts.
- Rebuild Timeline and Current State from persisted Observations on Horizon Lab startup.
- Add `horizon-storage` package with JSON adapter, serializers, repositories, and bootstrap.
- Add permanent document governance and Living Digital Twin foundation documents.
- Add Sprint-009 Current State Engine documentation and implementation.
- Add in-memory Current State projection from Timeline replay.
- Add Sprint-008 Temporal Memory Engine documentation and implementation.
- Add in-memory Timeline query, filters, cursor navigation, and replay.
- Rename Playground to Horizon Lab for in-memory exploration.
- Add Sprint-007 Observation vertical slice.
- Add Observation domain documentation, aggregate, application flow, and playground support.
- Add in-memory Observation registration, listing, domain event publication, and EventEnvelope display.
