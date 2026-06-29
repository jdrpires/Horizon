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

from horizon_application import (  # noqa: E402
    ApplicationService,
    RegisterAssetCommand,
    RegisterObservationCommand,
)
from horizon_events import EventEnvelope, EventSubscriber  # noqa: E402


def main() -> None:
    """Run the terminal playground."""
    seen_events: list[EventEnvelope] = []
    service = ApplicationService.create_in_memory(event_subscribers=(_console_subscriber(),))
    service.event_bus.subscribe(EventSubscriber(name="playground-memory", handler=seen_events.append))
    while True:
        print_menu()
        option = input("Select an option: ").strip()
        if option == "1":
            register_asset(service)
        elif option == "2":
            register_observation(service)
        elif option == "3":
            list_assets(service)
        elif option == "4":
            list_observations(service)
        elif option == "5":
            show_domain_events(seen_events)
        elif option == "6":
            print("Bye.")
            return
        else:
            print("Invalid option.")


def print_menu() -> None:
    """Print the playground menu."""
    print("====================================")
    print("HORIZON PLAYGROUND")
    print("1 Register Asset")
    print("2 Register Observation")
    print("3 List Assets")
    print("4 List Observations")
    print("5 Show Domain Events")
    print("6 Exit")
    print("====================================")


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


def register_observation(service: ApplicationService) -> None:
    """Prompt for Observation fields and register it."""
    assets = service.list_assets()
    if not assets:
        print("Register an Asset before registering an Observation.")
        return
    for index, asset in enumerate(assets, start=1):
        print(f"{index} - {asset.name} ({asset.asset_id})")
    selected = int(input("Select Asset: ").strip())
    asset = assets[selected - 1]
    observation_type = input("Type: ").strip()
    value = float(input("Value: ").strip())
    unit = input("Unit: ").strip()
    source = input("Source: ").strip()
    timestamp = input("Timestamp ISO optional: ").strip() or None
    result = service.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type=observation_type,
            value=value,
            unit=unit,
            source=source,
            timestamp=timestamp,
        )
    )
    print("Observation created:")
    print(json.dumps(result.observation.to_dict(), indent=2, sort_keys=True))
    print("Aggregate:")
    print(json.dumps(result.observation.to_dict(), indent=2, sort_keys=True))
    print("Domain Events produced:")
    for event in result.events:
        print(json.dumps(event.data["event"], indent=2, sort_keys=True))
    print("Event Envelopes:")
    for event in result.events:
        print(json.dumps(event.data, indent=2, sort_keys=True))


def list_observations(service: ApplicationService) -> None:
    """Print registered Observations."""
    observations = service.list_observations()
    if not observations:
        print("No Observations registered.")
        return
    for observation in observations:
        print(json.dumps(observation.to_dict(), indent=2, sort_keys=True))


def show_domain_events(events: list[EventEnvelope]) -> None:
    """Print all domain events seen by the playground event bus."""
    if not events:
        print("No Domain Events published.")
        return
    for envelope in events:
        print(json.dumps(dict(envelope.event), indent=2, sort_keys=True))


def _console_subscriber() -> EventSubscriber:
    """Create a console subscriber for playground events."""

    def handle(envelope: EventEnvelope) -> None:
        print(f"[event-bus] {envelope.event_name.value}")

    return EventSubscriber(name="playground-console", handler=handle)


if __name__ == "__main__":
    main()
