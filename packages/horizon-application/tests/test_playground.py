"""Playground smoke tests."""

import importlib.util
from pathlib import Path


def test_playground_module_exports_main() -> None:
    playground = Path("apps/playground/main.py").resolve()
    spec = importlib.util.spec_from_file_location("playground_main", playground)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(module.main)
