"""Asset query endpoints for Horizon clients."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_query_service
from app.schemas import AssetListResponse, CurrentStateResponse, TimelineResponse
from app.services import HorizonQueryService

router = APIRouter()


@router.get("/assets", response_model=AssetListResponse)
def list_assets(
    service: HorizonQueryService = Depends(get_query_service),
) -> AssetListResponse:
    """Return known Assets for client selection."""
    return service.list_assets()


@router.get("/assets/{asset_id}/current-state", response_model=CurrentStateResponse)
def get_current_state(
    asset_id: str,
    service: HorizonQueryService = Depends(get_query_service),
) -> CurrentStateResponse:
    """Return Current State for one Asset."""
    try:
        return service.get_current_state(asset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/assets/{asset_id}/timeline", response_model=TimelineResponse)
def get_timeline(
    asset_id: str,
    service: HorizonQueryService = Depends(get_query_service),
) -> TimelineResponse:
    """Return Timeline entries for one Asset."""
    try:
        return service.get_timeline(asset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
