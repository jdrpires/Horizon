from fastapi import FastAPI

from horizon_api.config import get_settings


settings = get_settings()

app = FastAPI(
    title="Project Horizon API",
    version="0.1.0",
    docs_url="/docs" if settings.env == "local" else None,
    redoc_url=None,
)
