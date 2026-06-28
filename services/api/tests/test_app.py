from horizon_api.main import app


def test_app_metadata() -> None:
    assert app.title == "Project Horizon API"
    assert app.version == "0.1.0"
