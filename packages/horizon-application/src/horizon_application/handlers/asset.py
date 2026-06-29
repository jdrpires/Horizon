"""Asset command and query handlers."""

from horizon_application.commands import RegisterAssetCommand
from horizon_application.contracts import AssetRepository
from horizon_application.dto import AssetDTO, RegisterAssetResultDTO
from horizon_application.queries import ListAssetsQuery
from horizon_application.use_cases import RegisterAssetUseCase


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
