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
5. If the C3 is the only Asset, confirm it is auto-selected.
6. If multiple Assets are listed, select the Citroen C3.
7. Tap `Usar Asset selecionado` when manual selection is required.
8. Close Horizon Mobile.
9. Open Horizon Mobile again.
10. Confirm the C3 is restored as selected.
11. Tap `Testar Horizon`.
12. Confirm Gateway status is `OK`.
13. Open `Estado` and tap `Buscar estado`.
14. Confirm Gateway logs show `GET /assets/3662b190-0a62-4e76-829f-86d500d4552c/current-state`.
15. Open `Timeline` and tap `Buscar Timeline`.
16. Confirm Gateway logs show `GET /assets/3662b190-0a62-4e76-829f-86d500d4552c/timeline`.
17. Open `Conexao`.
18. Confirm diagnostic panel shows Asset `OK`.
19. Connect ELM327.
20. Start reading.
21. Confirm Gateway logs show `POST /observations` with `asset_id=3662b190-0a62-4e76-829f-86d500d4552c`.

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
- Connection screen diagnostic panel.
- Logcat showing `[Publisher] Published observations count=...`.
