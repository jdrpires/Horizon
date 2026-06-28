"""Exception type reserved for exceptional domain failures."""

from horizon_kernel.exceptions.errors import Error


class DomainException(Exception):
    """Exception carrying a structured domain error."""

    def __init__(self, error: Error) -> None:
        """Create the exception from a structured error."""
        super().__init__(error.message)
        self.error = error
