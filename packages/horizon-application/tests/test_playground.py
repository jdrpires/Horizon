"""Horizon Lab smoke tests."""

import importlib.util
from pathlib import Path


def test_horizon_lab_module_exports_main() -> None:
    horizon_lab = Path("apps/horizon-lab/main.py").resolve()
    spec = importlib.util.spec_from_file_location("horizon_lab_main", horizon_lab)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(module.main)
