# Lessons Learned

Status: Living Historical Record

## Asset UUID Is A Continuity Requirement

The live field test showed that Asset identity cannot be treated as UI state or a friendly name. The Asset UUID is the continuity key that binds observations, Timeline, Current State, and future Twin memory.

## Bluetooth Stability Is Session Design

ELM327 stability depends on maintaining a coherent Bluetooth session: one selected MAC address, one socket lifecycle, controlled initialization, serialized commands, and explicit reconnection rules.

## Session State Must Be Explicit

Mobile runtime state must be restorable, visible, and testable. Hidden state drift produced `asset_id: null`, `GET /assets/null`, and `422` failures even while the Gateway was correct.

## Collector Boundaries Matter

The Collector Framework protected Horizon Core from Bluetooth, OBD, Android, hardware, and transport concerns. Real hardware validation confirmed that this boundary is not theoretical.

## Gateway Boundary Matters

The Gateway should receive, validate, and forward canonical observations. It should not become domain logic, hardware logic, or a public API by accident.

## Horizon Mobile Is A Client

Horizon Mobile is no longer only a bridge. It is the first official Horizon client for the state of an Asset. Its purpose is to help the user follow the Asset, not inspect raw PIDs.

## Hardware Tests Reveal Runtime Truth

Unit tests protect behavior, but real hardware reveals timing, identity, Bluetooth, network, and state synchronization failures. Field validation is now part of Horizon's evidence culture.

## Cloudflare Tunnel Is A Useful Validation Tool

Cloudflare Tunnel allowed real mobile-to-Gateway validation without changing Horizon Core or introducing production infrastructure. It is a field validation tool, not an architectural dependency.

## Memory First Survived Real Telemetry

The end-to-end flow proved that real telemetry can enter Horizon as observations, then become Timeline and Current State, without becoming knowledge prematurely.
