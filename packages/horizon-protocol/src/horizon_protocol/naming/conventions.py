"""Official Horizon Protocol naming conventions."""

from __future__ import annotations

import re
from dataclasses import dataclass

from horizon_protocol.shared import MessageKind, ProtocolValidationError

PASCAL_CASE_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*$")
CATEGORY_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$")
IDENTIFIER_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*Id$")

COMMAND_PREFIXES = (
    "Create",
    "Register",
    "Start",
    "Finish",
    "Schedule",
    "Cancel",
    "Update",
    "Delete",
    "Generate",
    "Request",
    "Record",
)
QUERY_PREFIXES = ("Get", "List", "Find", "Search", "Read", "Count")
EVENT_SUFFIXES = (
    "Created",
    "Registered",
    "Started",
    "Finished",
    "Generated",
    "Scheduled",
    "Cancelled",
    "Updated",
    "Deleted",
    "Recorded",
    "Observed",
)


@dataclass(frozen=True, slots=True)
class NamingConvention:
    """Validator for official Horizon names."""

    @staticmethod
    def ensure_pascal_case(value: str) -> str:
        """Validate a PascalCase protocol name."""
        if not PASCAL_CASE_PATTERN.fullmatch(value):
            raise ProtocolValidationError("Protocol names must use PascalCase.")
        return value

    @staticmethod
    def ensure_command(value: str) -> str:
        """Validate command name shape."""
        NamingConvention.ensure_pascal_case(value)
        if not value.startswith(COMMAND_PREFIXES):
            raise ProtocolValidationError("Command names must start with an approved verb.")
        return value

    @staticmethod
    def ensure_query(value: str) -> str:
        """Validate query name shape."""
        NamingConvention.ensure_pascal_case(value)
        if not value.startswith(QUERY_PREFIXES):
            raise ProtocolValidationError("Query names must start with an approved read verb.")
        return value

    @staticmethod
    def ensure_event(value: str) -> str:
        """Validate event name shape."""
        NamingConvention.ensure_pascal_case(value)
        if not value.endswith(EVENT_SUFFIXES):
            raise ProtocolValidationError("Event names must end with an approved past-tense suffix.")
        return value

    @staticmethod
    def ensure_identifier_name(value: str) -> str:
        """Validate identifier type name shape."""
        if not IDENTIFIER_PATTERN.fullmatch(value):
            raise ProtocolValidationError("Identifier names must use PascalCase and end with Id.")
        return value

    @staticmethod
    def ensure_category(value: str) -> str:
        """Validate registry category name shape."""
        if not CATEGORY_PATTERN.fullmatch(value):
            raise ProtocolValidationError("Category names must use lowercase dotted or kebab format.")
        return value

    @staticmethod
    def ensure_message(kind: MessageKind, value: str) -> str:
        """Validate a message name for its kind."""
        if kind is MessageKind.COMMAND:
            return NamingConvention.ensure_command(value)
        if kind is MessageKind.QUERY:
            return NamingConvention.ensure_query(value)
        return NamingConvention.ensure_event(value)
