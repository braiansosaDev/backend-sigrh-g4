from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.payroll_calculator import schemas
from src.modules.payroll_calculator import service

payroll_router = APIRouter(prefix="/payroll", tags=["Payroll Calculation"])


@payroll_router.post(
    "/", response_model=list[schemas.PayrollResponse], status_code=status.HTTP_200_OK
)
async def calculate_salary(db: DatabaseSession, request: schemas.PayrollRequest):
    return service.calculate_salary(db, request)
