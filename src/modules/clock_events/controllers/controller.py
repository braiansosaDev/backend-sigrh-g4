from datetime import date
from fastapi import APIRouter, Query, status
from src.database.core import DatabaseSession
from src.modules.clock_events.schemas import schemas
from src.modules.clock_events.services import services
from typing import List, Optional

clock_events_router = APIRouter(prefix="/clock_events", tags=["Clock events"])

@clock_events_router.get(
    "/attendance-resume",
    response_model=List[schemas.ClockEventAttendanceSummary],
    status_code=status.HTTP_200_OK
)
async def read_attendance_resume(
    db: DatabaseSession,
    fecha: date = Query(...)
):
    """
    Devuelve resumen de asistencia por empleado activo para una fecha dada
    """
    return services.get_attendance_resume(db, fecha)


@clock_events_router.get(
    "/", response_model=List[schemas.ClockEventRead], status_code=status.HTTP_200_OK
)
async def read_clock_events(
    db: DatabaseSession,
    employee_id: Optional[int] = Query(None),
    fecha: Optional[date] = Query(None)
):
    return services.get_clock_events(db, employee_id=employee_id, fecha=fecha)

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
