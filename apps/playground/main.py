"""Horizon in-memory playground."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for source_path in (
    ROOT / "packages" / "horizon-application" / "src",
    ROOT / "packages" / "horizon-domain" / "src",
    ROOT / "packages" / "horizon-events" / "src",
    ROOT / "packages" / "horizon-kernel" / "src",
):
    sys.path.insert(0, str(source_path))

from horizon_application import ApplicationService, RegisterAssetCommand  # noqa: E402
from horizon_events import EventEnvelope, EventSubscriber  # noqa: E402


def main() -> None:
    """Run the terminal playground."""
    service = ApplicationService.create_in_memory(event_subscribers=(_console_subscriber(),))
    while True:
        print_menu()
        option = input("Select an option: ").strip()
        if option == "1":
            register_asset(service)
        elif option == "2":
            list_assets(service)
        elif option == "3":
            print("Bye.")
            return
        else:
            print("Invalid option.")


def print_menu() -> None:
    """Print the playground menu."""
    print("===================================")
    print("HORIZON PLAYGROUND")
    print("1 - Register Asset")
    print("2 - List Assets")
    print("3 - Exit")
    print("===================================")


def register_asset(service: ApplicationService) -> None:
    """Prompt for Asset fields and register it."""
    name = input("Identification: ").strip()
    category = input("Classification: ").strip()
    owner_id = input("Owner: ").strip()
    result = service.register_asset(
        RegisterAssetCommand(name=name, category=category, owner_id=owner_id)
    )
    print("Aggregate created:")
    print(json.dumps(result.asset.to_dict(), indent=2, sort_keys=True))
    print("Domain Events produced:")
    for event in result.events:
        domain_event = event.data["event"]
        print(json.dumps(domain_event, indent=2, sort_keys=True))
    print("Event Envelopes:")
    for event in result.events:
        print(json.dumps(event.data, indent=2, sort_keys=True))


def list_assets(service: ApplicationService) -> None:
    """Print registered Assets."""
    assets = service.list_assets()
    if not assets:
        print("No Assets registered.")
        return
    for asset in assets:
        print(json.dumps(asset.to_dict(), indent=2, sort_keys=True))


def _console_subscriber() -> EventSubscriber:
    """Create a console subscriber for playground events."""

    def handle(envelope: EventEnvelope) -> None:
        print(f"[event-bus] {envelope.event_name.value}")

    return EventSubscriber(name="playground-console", handler=handle)


if __name__ == "__main__":
    main()
