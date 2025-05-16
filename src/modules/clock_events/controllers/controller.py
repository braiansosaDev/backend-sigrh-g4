from fastapi import APIRouter
import logging

logger = logging.getLogger("uvicorn.error")
clock_events_router = APIRouter(prefix="/clock_events", tags=["Clock events"])


@clock_events_router.get("/")
async def read_clock_events():
    """
    docstring
    """
    pass


@clock_events_router.post("/")
async def create_clock_event():
    """
    docstring
    """
    pass


@clock_events_router.patch("/{clock_event_id}")
async def update_clock_event(clock_event_id: int):
    """
    docstring
    """
    pass


@clock_events_router.delete("/{clock_event_id}")
async def delete_clock_event(clock_event_id: int):
    """
    docstring
    """
    pass
