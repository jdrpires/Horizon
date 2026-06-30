"""Gateway dependency composition."""

from app.dependencies.container import GatewayContainer, build_container, get_ingestion_service

__all__ = ["GatewayContainer", "build_container", "get_ingestion_service"]

