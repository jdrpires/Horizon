from pathlib import Path


def test_required_foundation_paths_exist() -> None:
    root = Path(__file__).resolve().parents[1]

    required_paths = [
        "README.md",
        "LICENSE",
        "docker-compose.yml",
        "pyproject.toml",
        "docs/ENGINEERING_PLAYBOOK.md",
        "services/api/src/horizon_api/main.py",
        "packages/kernel/domain/events",
        "packages/kernel/domain/value_objects",
        "infra/docker/postgres/init.sql",
    ]

    for required_path in required_paths:
        assert (root / required_path).exists()
