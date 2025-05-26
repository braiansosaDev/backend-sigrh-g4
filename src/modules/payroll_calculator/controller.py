from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.payroll_calculator import schemas
from src.modules.payroll_calculator import service

payroll_router = APIRouter(prefix="/payroll", tags=["Payroll Calculation"])


@payroll_router.post(
    "/calculate",
    response_model=list[schemas.PayrollResponse],  # No devolver esto
    status_code=status.HTTP_200_OK,
)
async def calculate_hours(db: DatabaseSession, request: schemas.PayrollRequest):
    return service.calculate_hours(db, request)


@payroll_router.post(
    "/hours",
    response_model=list[schemas.PayrollResponse],
    status_code=status.HTTP_200_OK,
)
async def get_hours_by_date_range(db: DatabaseSession, request: schemas.PayrollRequest):
    return service.get_hours_by_date_range(db, request)
