"""Protocol exceptions."""


class ProtocolError(Exception):
    """Base error for protocol violations."""


class ProtocolValidationError(ProtocolError, ValueError):
    """Raised when a protocol value does not follow the official convention."""
