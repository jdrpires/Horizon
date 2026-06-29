"""Application error types."""


class ApplicationError(Exception):
    """Base application-layer error."""


class HandlerNotFoundError(ApplicationError):
    """Raised when no handler is registered for a request."""
