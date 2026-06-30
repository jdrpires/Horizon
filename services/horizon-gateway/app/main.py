"""Horizon Live Ingestion Gateway application."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.observations import router as observations_router
from app.config import GatewaySettings, get_settings
from app.dependencies import build_container


def create_app(settings: GatewaySettings | None = None) -> FastAPI:
    """Create the Gateway FastAPI application."""
    resolved_settings = settings or get_settings()
    api = FastAPI(
        title="Horizon Live Ingestion Gateway",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
    )
    api.state.container = build_container(resolved_settings)
    api.include_router(observations_router)

    @api.get("/health")
    def health() -> dict[str, str]:
        """Return local Gateway health."""
        return {"status": "ok", "service": "horizon-gateway"}

    return api


app = create_app()

