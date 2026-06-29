"""Registries for official Horizon Protocol names and descriptors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from horizon_protocol.commands import CommandDescriptor
from horizon_protocol.events import EventReferenceDescriptor
from horizon_protocol.identifiers import ProtocolIdentifier
from horizon_protocol.naming import NamingConvention
from horizon_protocol.queries import QueryDescriptor
from horizon_protocol.schemas import SchemaDescriptor
from horizon_protocol.shared import ProtocolValidationError

T = TypeVar("T")


class Registry(Generic[T]):
    """Small immutable-value registry keyed by official names."""

    def __init__(self) -> None:
        """Create an empty registry."""
        self._items: dict[str, T] = {}

    def _add(self, name: str, value: T) -> T:
        """Add a value when the key is not already registered."""
        if name in self._items:
            raise ProtocolValidationError(f"{name} is already registered.")
        self._items[name] = value
        return value

    def get(self, name: str) -> T | None:
        """Return a registered item by name."""
        return self._items.get(name)

    def require(self, name: str) -> T:
        """Return a registered item or raise a protocol error."""
        item = self.get(name)
        if item is None:
            raise ProtocolValidationError(f"{name} is not registered.")
        return item

    def list(self) -> tuple[T, ...]:
        """Return all registered items."""
        return tuple(self._items.values())

    def names(self) -> tuple[str, ...]:
        """Return all registered names."""
        return tuple(self._items.keys())

    def clear(self) -> None:
        """Clear all registered items."""
        self._items.clear()


class CommandRegistry(Registry[CommandDescriptor]):
    """Registry of command descriptors."""

    def register(self, descriptor: CommandDescriptor) -> CommandDescriptor:
        """Register a command descriptor."""
        NamingConvention.ensure_command(descriptor.name)
        return self._add(descriptor.name, descriptor)


class QueryRegistry(Registry[QueryDescriptor]):
    """Registry of query descriptors."""

    def register(self, descriptor: QueryDescriptor) -> QueryDescriptor:
        """Register a query descriptor."""
        NamingConvention.ensure_query(descriptor.name)
        return self._add(descriptor.name, descriptor)


class EventRegistry(Registry[EventReferenceDescriptor]):
    """Registry of event reference descriptors."""

    def register(self, descriptor: EventReferenceDescriptor) -> EventReferenceDescriptor:
        """Register an event reference descriptor."""
        NamingConvention.ensure_event(descriptor.name)
        return self._add(descriptor.name, descriptor)


class SchemaRegistry(Registry[SchemaDescriptor]):
    """Registry of schema descriptors."""

    def register(self, descriptor: SchemaDescriptor) -> SchemaDescriptor:
        """Register a schema descriptor."""
        NamingConvention.ensure_pascal_case(descriptor.name)
        return self._add(descriptor.name, descriptor)


@dataclass(frozen=True, slots=True)
class IdentifierRegistration:
    """Registered protocol identifier type."""

    name: str
    identifier_type: type[ProtocolIdentifier]


class IdentifierRegistry(Registry[IdentifierRegistration]):
    """Registry of identifier types."""

    def register(
        self,
        name: str,
        identifier_type: type[ProtocolIdentifier],
    ) -> IdentifierRegistration:
        """Register an identifier type."""
        NamingConvention.ensure_identifier_name(name)
        if not issubclass(identifier_type, ProtocolIdentifier):
            raise ProtocolValidationError("Identifier type must extend ProtocolIdentifier.")
        return self._add(name, IdentifierRegistration(name, identifier_type))


class CategoryRegistry(Registry[str]):
    """Registry of official categories."""

    def register(self, name: str) -> str:
        """Register a category."""
        NamingConvention.ensure_category(name)
        return self._add(name, name)
