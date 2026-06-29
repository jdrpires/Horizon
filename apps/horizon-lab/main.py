"""Horizon in-memory lab."""

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
    GetTimelineQuery,
    RegisterAssetCommand,
    RegisterObservationCommand,
    ReplayTimelineQuery,
)
from horizon_events import EventEnvelope, EventSubscriber  # noqa: E402


def main() -> None:
    """Run the terminal Horizon Lab."""
    seen_events: list[EventEnvelope] = []
    service = ApplicationService.create_in_memory(event_subscribers=(_console_subscriber(),))
    service.event_bus.subscribe(EventSubscriber(name="horizon-lab-memory", handler=seen_events.append))
    while True:
        print_menu()
        option = input("Select an option: ").strip()
        if option == "1":
            register_asset(service)
        elif option == "2":
            register_observation(service)
        elif option == "3":
            show_timeline(service)
        elif option == "4":
            replay_timeline(service)
        elif option == "5":
            show_domain_events(seen_events)
        elif option == "6":
            print("Bye.")
            return
        else:
            print("Invalid option.")


def print_menu() -> None:
    """Print the Horizon Lab menu."""
    print("====================================")
    print("HORIZON LAB")
    print("1 Register Asset")
    print("2 Register Observation")
    print("3 Show Timeline")
    print("4 Replay Timeline")
    print("5 List Events")
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


def show_timeline(service: ApplicationService) -> None:
    """Print Timeline entries."""
    query = _timeline_query()
    result = service.show_timeline(query)
    if not result.entries:
        print("No Timeline entries.")
        return
    for entry in result.entries:
        print(json.dumps(entry.to_dict(), indent=2, sort_keys=True))


def replay_timeline(service: ApplicationService) -> None:
    """Replay Timeline entries."""
    query = _replay_query()
    result = service.replay_timeline(query)
    if not result.entries:
        print("No Timeline entries to replay.")
        return
    for entry in result.entries:
        print(
            f"{entry.timestamp} {entry.observation_type}={entry.value} "
            f"{entry.unit} asset={entry.asset_id}"
        )


def show_domain_events(events: list[EventEnvelope]) -> None:
    """Print all domain events seen by the Horizon Lab event bus."""
    if not events:
        print("No Domain Events published.")
        return
    for envelope in events:
        print(json.dumps(dict(envelope.event), indent=2, sort_keys=True))


def _console_subscriber() -> EventSubscriber:
    """Create a console subscriber for lab events."""

    def handle(envelope: EventEnvelope) -> None:
        print(f"[event-bus] {envelope.event_name.value}")

    return EventSubscriber(name="horizon-lab-console", handler=handle)


def _timeline_query() -> GetTimelineQuery:
    """Prompt for optional Timeline filters."""
    asset_id = input("Asset ID optional: ").strip() or None
    observation_type = input("Type optional: ").strip() or None
    start_at = input("Start timestamp optional: ").strip() or None
    end_at = input("End timestamp optional: ").strip() or None
    cursor_at = input("Cursor timestamp optional: ").strip() or None
    return GetTimelineQuery(
        asset_id=asset_id,
        observation_type=observation_type,
        start_at=start_at,
        end_at=end_at,
        cursor_at=cursor_at,
    )


def _replay_query() -> ReplayTimelineQuery:
    """Prompt for optional replay filters."""
    asset_id = input("Asset ID optional: ").strip() or None
    observation_type = input("Type optional: ").strip() or None
    start_at = input("Start timestamp optional: ").strip() or None
    end_at = input("End timestamp optional: ").strip() or None
    return ReplayTimelineQuery(
        asset_id=asset_id,
        observation_type=observation_type,
        start_at=start_at,
        end_at=end_at,
    )


if __name__ == "__main__":
    main()
