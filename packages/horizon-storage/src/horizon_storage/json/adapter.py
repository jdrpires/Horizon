"""Readable JSON storage adapter."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from horizon_storage.exceptions import StorageCorruptionError

ASSETS_FILE: Final = "assets.json"
OBSERVATIONS_FILE: Final = "observations.json"
METADATA_FILE: Final = "metadata.json"


class JsonStorageAdapter:
    """Adapter that persists Horizon facts as formatted JSON files."""

    def __init__(self, root: Path | str) -> None:
        """Create the adapter for a storage directory."""
        self.root = Path(root)

    def ensure_storage(self) -> None:
        """Create storage directory and initial files when absent."""
        self.root.mkdir(parents=True, exist_ok=True)
        if not self._path(ASSETS_FILE).exists():
            self.write_json(ASSETS_FILE, [])
        if not self._path(OBSERVATIONS_FILE).exists():
            self.write_json(OBSERVATIONS_FILE, [])
        if not self._path(METADATA_FILE).exists():
            self.write_json(
                METADATA_FILE,
                {"storage_version": 1, "created_at": "", "last_update": ""},
            )

    def read_json(self, filename: str) -> object:
        """Read a JSON document from storage."""
        try:
            with self._path(filename).open(encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise StorageCorruptionError(f"{filename} contains invalid JSON.") from exc

    def write_json(self, filename: str, payload: object) -> None:
        """Write a formatted JSON document and touch metadata."""
        self.root.mkdir(parents=True, exist_ok=True)
        self._path(filename).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if filename != METADATA_FILE and self._path(METADATA_FILE).exists():
            self._touch_metadata()

    def _touch_metadata(self) -> None:
        """Update storage metadata after a data write."""
        metadata = self.read_json(METADATA_FILE)
        if not isinstance(metadata, dict):
            raise StorageCorruptionError("metadata.json must contain an object.")
        metadata["last_update"] = datetime.now(UTC).isoformat()
        self._path(METADATA_FILE).write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _path(self, filename: str) -> Path:
        """Return an absolute file path inside the storage directory."""
        return self.root / filename
