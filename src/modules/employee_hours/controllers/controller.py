from typing import List
from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.employee_hours.schemas import schemas
from src.modules.employee_hours.services import services

employee_hours_router = APIRouter(prefix="/employee_hours", tags=["Employee hours"])


@employee_hours_router.get(
    "/",
    response_model=List[schemas.EmployeeHoursResponse],
    status_code=status.HTTP_200_OK,
)
async def read_employee_hours(db: DatabaseSession):
    """
    docstring
    """
    return services.get_all_employee_hours(db)


@employee_hours_router.post(
    "/",
    response_model=schemas.EmployeeHoursResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee_hours(
    db: DatabaseSession, request: schemas.EmployeeHoursRequest
):
    """
    docstring
    """
    return services.post_employee_hours(db, request)


@employee_hours_router.patch(
    "/{employee_hours_id}",
    response_model=schemas.EmployeeHoursPatchResponse,
    status_code=status.HTTP_200_OK,
)
async def update_employee_hours(
    db: DatabaseSession, employee_hours_id: int, request: schemas.EmployeeHoursPatchRequest
):
    """
    docstring
    """
    return services.patch_employee_hours(db, employee_hours_id, request)


@employee_hours_router.delete(
    "/{employee_hours_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_hours(db: DatabaseSession, employee_hours_id: int):
    """
    docstring
    """
    return services.delete_employee_hours(db, employee_hours_id)
