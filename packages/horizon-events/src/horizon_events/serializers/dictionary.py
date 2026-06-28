"""Dictionary serializer for event envelopes."""

from horizon_events.envelopes import EventEnvelope
from horizon_events.exceptions import EventSerializationError


class DictionarySerializer:
    """Serializer that converts envelopes to and from dictionaries."""

    def serialize(self, envelope: EventEnvelope) -> dict[str, object]:
        """Serialize an envelope to primitive dictionary data."""
        return envelope.to_dict()

    def deserialize(self, data: dict[str, object]) -> EventEnvelope:
        """Deserialize an envelope from primitive dictionary data."""
        try:
            return EventEnvelope.from_dict(data)
        except (KeyError, TypeError, ValueError) as exc:
            raise EventSerializationError(str(exc)) from exc
