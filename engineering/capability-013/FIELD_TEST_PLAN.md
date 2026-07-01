# Capability-013 Field Test Plan

Status: Draft

## Objective

Validate that Horizon Mobile uses the selected Asset UUID for all Gateway calls during live C3 collection.

## Preconditions

- Horizon Gateway running and reachable from Realme.
- C3 Asset exists in Gateway with UUID:
  `3662b190-0a62-4e76-829f-86d500d4552c`
- ELM327 paired with Realme.
- Horizon Mobile installed.

## Steps

1. Open Horizon Mobile.
2. Configure Gateway URL.
3. Open `Assets`.
4. Tap `Buscar Assets no Horizon`.
5. Select the Citroen C3.
6. Tap `Usar Asset selecionado`.
7. Close Horizon Mobile.
8. Open Horizon Mobile again.
9. Confirm the C3 is restored as selected.
10. Open `Estado` and tap `Buscar estado`.
11. Confirm Gateway logs show `GET /assets/3662b190-0a62-4e76-829f-86d500d4552c/current-state`.
12. Open `Timeline` and tap `Buscar Timeline`.
13. Confirm Gateway logs show `GET /assets/3662b190-0a62-4e76-829f-86d500d4552c/timeline`.
14. Connect ELM327.
15. Start reading.
16. Confirm Gateway logs show `POST /observations` with `asset_id=3662b190-0a62-4e76-829f-86d500d4552c`.

## Failure Conditions

The test fails if any of these appear:

- `GET /assets/null/current-state`
- `GET /assets/null/timeline`
- `asset_id: null`
- `422 Unprocessable Entity` caused by missing `asset_id`

## Evidence To Capture

- Screenshot of selected Asset.
- Logcat showing `[Asset] Asset restored`.
- Logcat showing `[Gateway] POST asset_id=...`.
- Gateway logs for Current State and Timeline.
