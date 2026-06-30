"""Observation ingestion endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from horizon_collector.exceptions import ObservationMappingError
from horizon_kernel import DomainException

from app.dependencies import get_ingestion_service
from app.schemas import ObservationIngestionRequest, ObservationIngestionResponse
from app.services import LiveIngestionService

router = APIRouter()


@router.post(
    "/observations",
    response_model=ObservationIngestionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def ingest_observations(
    payload: ObservationIngestionRequest,
    service: LiveIngestionService = Depends(get_ingestion_service),
) -> ObservationIngestionResponse:
    """Receive collector Observations and forward them into Horizon."""
    try:
        return service.ingest(payload)
    except ObservationMappingError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
