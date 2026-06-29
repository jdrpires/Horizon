"""Asset command and query handlers."""

from horizon_application.commands import RegisterAssetCommand, RegisterObservationCommand
from horizon_application.contracts import AssetRepository, ObservationRepository
from horizon_application.dto import (
    AssetDTO,
    ObservationDTO,
    RegisterAssetResultDTO,
    RegisterObservationResultDTO,
)
from horizon_application.queries import ListAssetsQuery, ListObservationsQuery
from horizon_application.use_cases import RegisterAssetUseCase, RegisterObservationUseCase


class RegisterAssetCommandHandler:
    """Command handler for RegisterAssetCommand."""

    def __init__(self, use_case: RegisterAssetUseCase) -> None:
        """Create a handler."""
        self._use_case = use_case

    def handle(self, command: RegisterAssetCommand) -> RegisterAssetResultDTO:
        """Handle the command."""
        return self._use_case.execute(command)


class ListAssetsQueryHandler:
    """Query handler for ListAssetsQuery."""

    def __init__(self, repository: AssetRepository) -> None:
        """Create a handler."""
        self._repository = repository

    def handle(self, _query: ListAssetsQuery) -> tuple[AssetDTO, ...]:
        """Handle the query."""
        return tuple(AssetDTO.from_asset(asset) for asset in self._repository.list())


class RegisterObservationCommandHandler:
    """Command handler for RegisterObservationCommand."""

    def __init__(self, use_case: RegisterObservationUseCase) -> None:
        """Create a handler."""
        self._use_case = use_case

    def handle(self, command: RegisterObservationCommand) -> RegisterObservationResultDTO:
        """Handle the command."""
        return self._use_case.execute(command)


class ListObservationsQueryHandler:
    """Query handler for ListObservationsQuery."""

    def __init__(self, repository: ObservationRepository) -> None:
        """Create a handler."""
        self._repository = repository

    def handle(self, _query: ListObservationsQuery) -> tuple[ObservationDTO, ...]:
        """Handle the query."""
        return tuple(
            ObservationDTO.from_observation(observation) for observation in self._repository.list()
        )
