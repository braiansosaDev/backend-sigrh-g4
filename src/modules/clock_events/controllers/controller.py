from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.clock_events.schemas import schemas
from src.modules.clock_events.services import services
from typing import List

clock_events_router = APIRouter(prefix="/clock_events", tags=["Clock events"])


@clock_events_router.get(
    "/", response_model=List[schemas.ClockEventResponse], status_code=status.HTTP_200_OK
)
async def read_clock_events(db: DatabaseSession):
    """
    docstring
    """
    return services.get_clock_events(db)


@clock_events_router.post(
    "/", response_model=schemas.ClockEventResponse, status_code=status.HTTP_201_CREATED
)
async def create_clock_event(db: DatabaseSession, request: schemas.ClockEventRequest):
    """
    docstring
    """
    return services.post_clock_event(db, request)


@clock_events_router.patch(
    "/{clock_event_id}",
    response_model=schemas.ClockEventResponse,
    status_code=status.HTTP_200_OK,
)
async def update_clock_event(
    db: DatabaseSession, clock_event_id: int, request: schemas.ClockEventRequest
):
    """
    docstring
    """
    return services.patch_clock_event(db, clock_event_id, request)


@clock_events_router.delete("/{clock_event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clock_event(db: DatabaseSession, clock_event_id: int):
    """
    docstring
    """
    return services.delete_clock_event(db, clock_event_id)
