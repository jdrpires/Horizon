# Capability-012 Review

Status: Draft

## Scope Review

Allowed scope:

- `apps/horizon-mobile/`
- `engineering/capability-012/`
- Capability-010 UX notes

No functional code outside Horizon Mobile was changed.

## Architectural Review

The Bluetooth Session Engine preserves the Horizon boundary:

- Android handles Bluetooth.
- ELM327 is treated as an external data source.
- Horizon Gateway receives canonical observations.
- Horizon Core remains unaware of RFCOMM, Bluetooth, PIDs, or device hardware.

## Implementation Review

The session now has explicit ownership of:

- selected device by MAC address;
- socket lifecycle;
- ELM327 initialization;
- PID polling order;
- reconnection behavior;
- observable diagnostics for the UI.

## Tests Added

- Initial state.
- MAC selection.
- No automatic MAC switching.
- ELM327 initialization order.
- PID polling order.
- Timeout/read failure reconnection using same MAC.
- Stop reading closes the socket.
- Connection errors do not crash the app flow.
- Publisher receives canonical observations.

## Risks

- Field behavior still depends on ELM327 clone quality.
- Long-running Android foreground/background behavior is not yet hardened.
- Current reading loop is Activity-owned and should eventually move to a lifecycle-aware component.
- Gateway delivery still has no offline queue.

## Recommendation

Perform the C3 field test before closing the capability. If the connection remains unstable, collect Logcat output tagged `HorizonBluetooth` before introducing additional architectural changes.
