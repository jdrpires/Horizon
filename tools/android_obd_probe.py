#!/usr/bin/env python3
"""Experimental Android OBD probe.

The default transport is `mock`, which runs fully locally. The
`android-bluetooth` transport is intentionally a documented placeholder until a
native Android Bluetooth bridge is approved.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT / "packages" / "collector-obd" / "src",
    ROOT / "packages" / "horizon-collector" / "src",
    ROOT / "packages" / "horizon-catalog" / "src",
):
    sys.path.insert(0, str(path))

from collector_obd import AndroidBluetoothTransport, Elm327Adapter, MockObdTransport
from collector_obd.android import android_pairing_steps, android_probe_limitations
from collector_obd.mapping import ObdObservationMapper
from horizon_catalog import load_vehicle_catalog
from horizon_collector.adapters import InMemoryObservationPublisher
from horizon_collector.registry import CollectorRegistry
from horizon_collector.runtime import InMemoryCollectorRuntime


def main() -> int:
    """Run the experimental OBD probe."""
    args = _parse_args()
    if args.show_android_notes:
        _print_android_notes()
        return 0

    transport = _build_transport(args)
    collector = Elm327Adapter(transport)
    registry = CollectorRegistry()
    registry.register(collector)
    publisher = InMemoryObservationPublisher()
    runtime = InMemoryCollectorRuntime(
        registry=registry,
        mapper=ObdObservationMapper(catalog=load_vehicle_catalog()),
        publisher=publisher,
    )

    try:
        observations = runtime.run_once(collector.name)
    finally:
        collector.close()

    for observation in observations:
        print(
            f"{observation.definition.id} "
            f"({observation.observation_type}) = {observation.value} {observation.unit} "
            f"source={observation.source}"
        )
    print(f"published={len(publisher.published)}")
    return 0


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Experimental Android OBD probe")
    parser.add_argument(
        "--transport",
        choices=("mock", "android-bluetooth"),
        default="mock",
        help="Transport to use. Only mock runs locally today.",
    )
    parser.add_argument(
        "--device-address",
        default="",
        help="Paired ELM327 Bluetooth MAC/address for future Android transport.",
    )
    parser.add_argument(
        "--show-android-notes",
        action="store_true",
        help="Print Realme/Android pairing notes and exit.",
    )
    return parser.parse_args()


def _build_transport(args: argparse.Namespace) -> MockObdTransport | AndroidBluetoothTransport:
    """Create the requested transport."""
    if args.transport == "mock":
        return MockObdTransport()
    if not args.device_address.strip():
        raise SystemExit("--device-address is required for android-bluetooth transport.")
    return AndroidBluetoothTransport(device_address=args.device_address)


def _print_android_notes() -> None:
    """Print Android/Realme notes."""
    print("Android/Realme pairing steps:")
    for step in android_pairing_steps():
        print(f"- {step}")
    print("\nCurrent limitations:")
    for limitation in android_probe_limitations():
        print(f"- {limitation}")


if __name__ == "__main__":
    raise SystemExit(main())
