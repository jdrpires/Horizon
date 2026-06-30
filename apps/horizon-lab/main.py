"""Horizon in-memory lab."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for source_path in (
    ROOT / "packages" / "horizon-application" / "src",
    ROOT / "packages" / "horizon-domain" / "src",
    ROOT / "packages" / "horizon-events" / "src",
    ROOT / "packages" / "horizon-experience" / "src",
    ROOT / "packages" / "horizon-kernel" / "src",
    ROOT / "packages" / "horizon-storage" / "src",
):
    sys.path.insert(0, str(source_path))

from horizon_application import (  # noqa: E402
    ApplicationService,
    GetCurrentStateQuery,
    GetTimelineQuery,
    InMemoryTimelineRepository,
    RegisterAssetCommand,
    RegisterObservationCommand,
)
from horizon_experience import (  # noqa: E402
    UserCancelled,
    choose_from_list,
    print_current_state,
    print_menu,
    print_timeline,
    prompt_float,
    prompt_optional_datetime,
    prompt_text,
)
from horizon_experience.formatters import friendly_unit, friendly_value  # noqa: E402
from horizon_experience.rendering import error, info, section, success  # noqa: E402
from horizon_storage import JsonStorageBootstrap  # noqa: E402


def main() -> None:
    """Run the terminal Horizon Lab."""
    bootstrap = JsonStorageBootstrap(_storage_path()).bootstrap()
    timeline_repository = InMemoryTimelineRepository()
    for observation in bootstrap.observation_repository.list():
        timeline_repository.append_observation(observation)
    service = ApplicationService.create_with_repositories(
        repository=bootstrap.asset_repository,
        observation_repository=bootstrap.observation_repository,
        timeline_repository=timeline_repository,
    )
    print_startup(bootstrap.assets_loaded, bootstrap.observations_loaded, bootstrap.storage_kind)
    while True:
        print_menu()
        option = _read_menu_option()
        if option == "1":
            register_asset(service)
        elif option == "2":
            register_observation(service)
        elif option == "3":
            show_timeline(service)
        elif option == "4":
            show_current_state(service)
        elif option == "5":
            print("Até logo.")
            return
        else:
            error("Escolha uma opção válida.")


def print_startup(assets_loaded: int, observations_loaded: int, storage_kind: str) -> None:
    """Print Horizon Lab startup storage summary."""
    section("HORIZON LAB")
    print(f"Assets carregados: {assets_loaded}")
    print(f"Observações carregadas: {observations_loaded}")
    print("Dados locais prontos.")
    info("Digite 'c' em qualquer formulário para cancelar e voltar ao menu.")


def register_asset(service: ApplicationService) -> None:
    """Prompt for Asset fields and register it."""
    section("Cadastrar Asset")
    try:
        name = prompt_text("Nome do Asset")
        category = prompt_text("Tipo do Asset")
        owner_id = prompt_text("Proprietário")
        result = service.register_asset(
            RegisterAssetCommand(name=name, category=category, owner_id=owner_id)
        )
    except UserCancelled:
        info("Cadastro cancelado.")
        return
    except Exception as exc:
        error(_friendly_failure(exc, "Não foi possível cadastrar o Asset."))
        return
    success(f"Asset cadastrado: {result.asset.name}.")


def register_observation(service: ApplicationService) -> None:
    """Prompt for Observation fields and register it."""
    section("Registrar Observação")
    assets = service.list_assets()
    if not assets:
        info("Cadastre um Asset antes de registrar uma observação.")
        return
    try:
        asset = choose_from_list("Escolha o Asset", assets, lambda item: item.name)
        observation_type = prompt_text("Tipo da Observação")
        value = prompt_float("Valor")
        unit = prompt_text("Unidade")
        source = prompt_text("Origem")
        timestamp = prompt_optional_datetime("Data/Hora (opcional)")
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
    except UserCancelled:
        info("Registro cancelado.")
        return
    except Exception as exc:
        error(_friendly_failure(exc, "Não foi possível registrar a observação."))
        return
    value = friendly_value(result.observation.value)
    unit = friendly_unit(result.observation.unit)
    success(f"Observação registrada: {value} {unit}.")


def show_timeline(service: ApplicationService) -> None:
    """Print Timeline entries."""
    result = service.show_timeline(GetTimelineQuery())
    print_timeline(result.entries)


def show_current_state(service: ApplicationService) -> None:
    """Print Current State for a selected Asset."""
    section("Estado Atual")
    assets = service.list_assets()
    if not assets:
        info("Cadastre um Asset antes de visualizar o Current State.")
        return
    try:
        asset = choose_from_list("Escolha o Asset", assets, lambda item: item.name)
    except UserCancelled:
        info("Consulta cancelada.")
        return
    snapshot = service.get_current_state(GetCurrentStateQuery(asset_id=asset.asset_id))
    print_current_state(asset.name, asset.status, snapshot)


def _read_menu_option() -> str:
    """Read the main menu option without crashing on closed input."""
    try:
        return input("Escolha uma opção: ").strip()
    except EOFError:
        return "5"


def _friendly_failure(exc: Exception, fallback: str) -> str:
    """Map internal failures to user-facing messages."""
    message = str(exc)
    if "observation.type.unknown" in message or "known observation type" in message:
        return "Tipo da Observação não reconhecido."
    if "timestamp" in message and "future" in message:
        return "Data/Hora não pode estar no futuro."
    if "must be finite" in message:
        return "Valor precisa ser um número válido."
    return fallback


def _storage_path() -> Path:
    """Return the configured Horizon Lab storage path."""
    configured = os.environ.get("HORIZON_STORAGE_PATH")
    return Path(configured) if configured else ROOT / "storage"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Até logo.")
